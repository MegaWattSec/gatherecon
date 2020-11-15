import argparse
import pymongo
import config

def main():
    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", help="Search for targets, given \
                        a filter.")
    parser.add_argument("-t", "--targets", help="Select targets with a comma \
                        separated list. 'All' will use all available targets")
    parser.add_argument("-u", "--update", help="Update target definitions.")
    args = parser.parse_args()

    # Setup MongoDB Connection
    # Setup MongoClient and get database
    _config = config.Config()
    _client = pymongo.MongoClient(_config.db_host)
    _db = _client[_config.db_name]

    # If given targets, iterate over
    target_list = args["targets"]
    if target_list is not None:
        for target in target_list:
            # Instantiate the session object
            print("do something")

    return 0


if __name__ == "__main__":
    main()