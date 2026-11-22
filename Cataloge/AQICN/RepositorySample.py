import time
from typing import Any, Dict, List, Optional

from Cataloge.Database import MongoDatabase


class SampleRepository:

    def __init__(self, db: MongoDatabase, collection_name: str):
        self._collection = db.get_collection(collection_name)
        
    def read():
        pass
    def delete():
        pass
    def update():
        pass
    def write():
        pass