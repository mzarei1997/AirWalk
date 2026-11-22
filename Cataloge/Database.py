from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

class MongoDatabase:

    def __init__(self, uri: str, db_name: str):
        self._client = MongoClient(uri)
        self._db: Database = self._client[db_name]

    def ping(self) -> bool:
        self._client.admin.command("ping")
        return True

    def get_collection(self, name: str) -> Collection:
        return self._db[name]

    def close(self) -> None:
        self._client.close()