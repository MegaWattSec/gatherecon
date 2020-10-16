import docker
from datetime import datetime as dt
from pathlib import Path
from pymongo import MongoClient, DESCENDING
from box import Box
from ruamel.yaml import RoundTripLoader
from config import Config

class ReconSession:
    
    def __init__(self, database, domain, scope):
        self.domain = domain
        self.scope = scope
        self.date = dt.now()

        # Load config
        self.config = Config()

        # Setup MongoClient
        self._client = MongoClient(self.config.db_host)

        # Get Mongo Database
        self._db = self._client[database]

        # Create Session document
        ## Get Sessions collection
        ## Add a document for this session
        self._sessions = self._db["Sessions"]
        self.current_session = self._sessions.insert_one({
            "_schema": 1,
            #"target": NotImplemented,
            "started": dt.now(),
            "finished": None,
        })

        # Return Domains collection
        self._domains = self._db["Domains"]

        # Create directory to save assets for domain
        ## Get base asset directory from config
        ## then create unique subdirectory
        self._assets = Path.home() / 'assets'
        self._session_path = self._assets / self.domain / dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        self._session_path.mkdir(parents=True, exist_ok=True)

        # Get modules from config
        self.modules = self.config.modules

        # Create db document
        # Store session properties in document
        # Keep the document Id for this session
        insert_result = self._domains.insert_one({ 
            'scope': self.scope,
            'path': self.path,
            'date': self.date,
        })
        self._id = insert_result.inserted_id
        
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._client.close()

    # Get the path property returned as String instead of pathlib.Path object
    @property
    def path(self):
        return str(self._session_path)

    # Get session ID as string
    @property
    def id(self):
        return str(self._id)

    @property
    def db_document(self):
        return self._domains.find_one({ "_id": self._id })

    def run(self):
        # Run modules in list

        # Store asset metadata in document

        return True


class SessionList:

    def __init__(self, database, domain):
        self.domain = domain

        # Load config
        self.config = Config()

        # Setup MongoClient
        self._client = MongoClient(self.config.db_host)

        # Get Mongo Database
        self._db = self._client[database]

        # Return collection
        self._sessions = self._db["Sessions"]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._client.close()

    def get_sessions(self):
        self._cursor = self._sessions.find()
        return self._cursor

    def get_count(self):
        return self._sessions.count_documents({})

    def get_previous(self):
        return self._sessions.find({}, sort=[("date", DESCENDING)])[1:2]

    def get_latest(self):
        return self._sessions.find({}, sort=[("date", DESCENDING)])[0:1]



_dclient = docker.from_env()
try:
    container = _dclient.containers.get('mongodb')
except docker.errors.NotFound:
    container = _dclient.containers.run(
        "mongo",
        detach = True,
        name = "mongodb",
        ports = {
            '27017/tcp': 27017,
            '27018/tcp': 27018,
            '27019/tcp': 27019
        }
    )