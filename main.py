import sys
import argparse
import pymongo
import importlib
import pkgutil
import pathlib
import tldextract
from fuzzywuzzy import process
from datetime import datetime as dt

import config
import recon
import components
from component import Component

def validate_db(database):
    _targets = database["Targets"]
    _scopes  = database["Scopes"]

    target_list = _scopes.find(
        filter={
            'targets.in_scope': {
                '$exists': True, 
                '$ne': []
            }
        },
        projection={
            '_id': 0, 
            'name': 1
        }
    ).distinct('name')

    for target in target_list:
        # Remove duplicate targets
        # Get target Document
        result = _targets.find(
            filter={
                "target": target
            },
            projection={
                "_id": 1
            },
            sort=[("_time", pymongo.DESCENDING)]
        ).distinct("_id")
        # If there is more than one result, keep only latest targets
        # This cleans up the entire collection
        if len(result) > 1:
            _targets.aggregate([
                {
                    '$sort': {
                        '_time': -1
                    }
                }, {
                    '$group': {
                        '_id': 'target', 
                        'doc': {
                            '$first': '$$ROOT'
                        }
                    }
                }, {
                    '$replaceRoot': {
                        'newRoot': '$doc'
                    }
                }, {
                    '$out': 'Targets'
                }
            ])

    return 0

def run_session():
    return 0

def search_scopes(search_term, database):
    return 0

def update_scopes(database):
    return 0

def process_targets(target_list, database):
    
    # Reference Collections
    _targets = database["Targets"]
    _sessions = database["Sessions"]
    _domains = database["Domains"]
    _scopes = database["Scopes"]

    # Create component list
    # load subclasses from modules in components/ directory
    # use components dir from components package
    # import all the submodules
    # then gather a list of the names
    component_list = []
    package_dir = pathlib.Path(components.__file__).resolve().parent
    for (_, module_name, _) in pkgutil.iter_modules([package_dir]):
        importlib.import_module(f"components.{module_name}")
    for each in Component.__subclasses__():
        component_list.append((each.__module__, each.__name__))

    if "AllAvailableTargets" in target_list:
        # query mongo for list of all targets with scope
        target_list = _scopes.find(
            filter={
                'targets.in_scope': {
                    '$exists': True, 
                    '$ne': []
                }
            },
            projection={
                '_id': 0, 
                'name': 1
            }
        ).distinct('name')

    # If given targets, iterate over
    for target in target_list:
        # Create directory to save assets for target
        # this should create an appropriate path depending on platform
        _target_path = pathlib.Path.home() / 'assets' / target
        _session_path = _target_path / dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        _session_path.mkdir(parents=True, exist_ok=True)

        # Query the database for scope, filtering on asset_type of URL
        scope = list(_scopes.find(
            filter={
                'name': target
            },
            projection={
                '_id': 0, 
                'in_scope': {
                    '$filter': {
                        'input': '$targets.in_scope', 
                        'cond': {
                            '$eq': [
                                '$$this.asset_type', 'URL'
                            ]
                        }
                    }
                }, 
                'out_of_scope': {
                    '$filter': {
                        'input': '$targets.out_of_scope', 
                        'cond': {
                            '$eq': [
                                '$$this.asset_type', 'URL'
                            ]
                        }
                    }
                }
            }
        ))

        # If the target isn't in the scope list, fail gracefully
        if len(scope) == 0:
            print(f"\nTarget {target} is not valid. Skipping target...\n")
            continue

        # Get Target Document
        result = _targets.find(
            filter={
                "target": target
            },
            projection={
                "_id": 1
            },
            sort=[("_time", pymongo.DESCENDING)]
        ).distinct("_id")
        # If there are no results, then create the document
        # return it in a list object like the other results
        if len(result) == 0:
            result = [_targets.insert_one({
                "_schema": 1,
                "_time": dt.now(),
                "path": str(_target_path),
                "target": target,
                "scope": scope
            }).inserted_id]
        # Keep the first (most recent) document
        target_document = result[0]

        # Create Session document
        ## Get Sessions collection
        ## Add a document for this session
        session_document = _sessions.insert_one({
            "_schema": 1,
            "path": str(_session_path),
            "target": target_document,
            "started": dt.now(),
            "finished": None,
            "components": component_list,
        })

        # Create domain documents for each domain in scope
        ## Start by getting a list of domains from scope by
        ##   extracting the domain and tld
        domain_list = []
        for in_scope in scope[0]["in_scope"]:
            domain = in_scope["asset_identifier"]
            ext = tldextract.extract(domain)
            domain_list.append(f"{ext.domain}.{ext.suffix}")
        
        # use fuzzy matching to determine if the domain belongs
        # to the target. We don't want to recon other companies
        # accidentally
        domain_list = process.extract(
                            target,
                            set(domain_list),
                            limit=100)
        
        ## then create the document with a unique set of domains
        for domain in domain_list:
            if domain[1] > 80:      # only if the fuzzy match is high
                domain_document = _domains.insert_one({
                    'scope': scope,
                    'date': dt.now(),
                    "name": domain[0],
                    "subdomains": [],
                })

        run_session()
    return 0

def main(args=None):
    # Get arguments, either passed in via tests or command line
    if not args:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("targets",
                        nargs="+",
                        default="AllAvailableTargets",
                        help="Enter targets by name. \
                            Entering nothing will use all available targets")
    parser.add_argument("-s", "--search", help="Search for the provided targets.")
    parser.add_argument("-u", "--update", help="Update target definitions.")
    args = parser.parse_args(args)
    # print("Arguments: " + str(args))

    # Setup MongoDB Connection
    # Setup MongoClient and get database
    _config = config.Config()
    _client = pymongo.MongoClient(_config.db_host)
    _db = _client[_config.db_name]

    # Reference Collections
    _targets = _db["Targets"]

    # Setup Collection indexes
    # Targets Collection should be unique to prevent dups
    _targets.create_index([("target", pymongo.ASCENDING)], unique=True)

    # Process the arguments in order of this precedence:
    #   update can be done independently
    #   if searching, use the target list for search and return
    #   if not searching, process the target list as a recon session
    if args.update:
        update_scopes(_db)

    if args.search:
        ret_result = search_scopes(args.targets, _db)
    elif args.targets:
        ret_result = process_targets(args.targets, _db)

    return ret_result


if __name__ == "__main__":
    main()