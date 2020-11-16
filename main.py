import sys
import argparse
import pymongo
import config

def main(args=None):
    # Get arguments, either passed in via tests or command line
    if not args:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("targets",
                        nargs="+",
                        help="Enter targets by name. \
                            Entering nothing will use all available targets")
    parser.add_argument("-s", "--search", help="Search for targets, given \
                        a filter.")
    parser.add_argument("-u", "--update", help="Update target definitions.")
    args = parser.parse_args(args)
    print("Arguments: " + str(args))

    # Setup MongoDB Connection
    # Setup MongoClient and get database
    _config = config.Config()
    _client = pymongo.MongoClient(_config.db_host)
    _db = _client[_config.db_name]

    # If given targets, iterate over
    target_list = args.targets
    for target in target_list:
        # if the target is blank, process all targets
        if target == "":
            target = "AllTargetsAvailable"

        # Instantiate the session object
        print("do something with " + str(target))

    return 0


if __name__ == "__main__":
    main()