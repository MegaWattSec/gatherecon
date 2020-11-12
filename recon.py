import docker
from datetime import datetime as dt
from pathlib import Path
from pymongo import MongoClient, DESCENDING
from config import Config
import components
from component import Component
from importlib import import_module
from pkgutil import iter_modules

class ReconSession:
    
    def __init__(self, domain, scope):
        self.domain = domain
        self.scope = scope
        self.date = dt.now()

        # Create directory to save assets for domain
        # this should create an appropriate path depending on platform
        self._assets = Path.home() / 'assets'
        self._session_path = self._assets / self.domain / dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        self._session_path.mkdir(parents=True, exist_ok=True)

        # Load config
        self.config = Config()

        # Setup MongoClient
        self._client = MongoClient(self.config.db_host)

        # Get Mongo Database
        self._db = self._client[self.config.db_name]

        # Find Target document or
        # Add document to Targets collection
        self._targets = self._db["Targets"]
        self.target_document = self._targets.insert_one({
            "_schema": 1,
            "path": self.path,
            "scope": self.scope,
            "target": self.domain,
            "asn": None,
            "githubs": None,
            "domains": [],
            "hosts": [],
        })

        # Create component list
        # load subclasses from modules in components/ directory
        # use components dir from components package
        # import all the submodules
        # then gather a list of the names
        self.component_list = []
        package_dir = Path(components.__file__).resolve().parent
        for (_, module_name, _) in iter_modules([package_dir]):
            import_module(f"components.{module_name}")
        for each in Component.__subclasses__():
            self.component_list.append((each.__module__, each.__name__))

        # Create Session document
        ## Get Sessions collection
        ## Add a document for this session
        self._sessions = self._db["Sessions"]
        self.current_session = self._sessions.insert_one({
            "_schema": 1,
            "target": self.target_document.inserted_id,
            "started": dt.now(),
            "finished": None,
            "components": self.component_list,
        })

        # Return Domains collection
        self._domains = self._db["Domains"]

        # Create domain document
        # Keep the document Id for this session
        insert_result = self._domains.insert_one({ 
            'scope': self.scope,
            'path': self.path,
            'date': self.date,
            "name": self.domain,
            "subdomains": [],
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

    def get_sessions(self):
        self._cursor = self._sessions.find()
        return self._cursor

    def get_count(self):
        return self._sessions.count_documents({})

    def get_previous(self):
        return self._sessions.find({}, sort=[("date", DESCENDING)])[1:2]

    def get_latest(self):
        return self._sessions.find({}, sort=[("date", DESCENDING)])[0:1]

    def check_component(self, mod):
        m = import_module(mod[0])
        c = getattr(m, mod[1])
        if not Path(c(self.domain, self.scope).modfile).exists():
            print(f"Component {mod} failed to load properly.")
            return False
        return True

    def run(self):
        # Run components in list

        # Store asset metadata in document

        return True


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