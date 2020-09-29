import docker
from pymongo import MongoClient

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

class GatherDb:

    def __init__(self):
        self._client = MongoClient()
        self._db = self._client.test_database
        self._collection = self._db.test_collection

    def __del__(self):
        self._client.close()


class SessionList(list):
    session_list = []

    def __init__(self):
        self.session_list = NotImplemented