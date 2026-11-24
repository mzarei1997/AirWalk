from pathlib import Path
import time
import json
from typing import Any, Dict, List, Optional

from tomlkit import document
from Cataloge.Database import MongoDatabase
from pymongo import MongoClient, UpdateOne, GEOSPHERE

from Cataloge.PolygonsDataModel import TurinPolygonModel

class CatalogeRepository:

    def __init__(self, mongo_uri: str, db_name: str, collection: str):
        self.db = MongoDatabase(mongo_uri, db_name)
        # self.db = self.client[db_name]
        # self.boundary_col = self.db.get_collection("regions")
        self.polygons_col = self.db.get_collection(collection)

    def write_turin_boundary(self, file_path: str | Path, force: bool = False) -> None:
        """Writes turin_boundary.geojson to MongoDB once."""
        if not force and self.boundary_col.count_documents({}) > 0:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            feature = json.load(f)["features"][0]

        doc = {
            "_id": feature["properties"]["osm_id"],
            "properties": feature["properties"],
            "geometry": feature["geometry"],
        }
        self.boundary_col.create_index([("geometry", GEOSPHERE)])
        self.boundary_col.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)

    def read_turin_boundary(self) -> Optional[Dict[str, Any]]:
        return self.boundary_col.find_one()

    def write_turin_polygons(self, file_path: str | Path, force: bool = False) -> None:
        """Writes turin_polygons.geojson to MongoDB once."""
        if not force and self.polygons_col.count_documents({}) > 0:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            features = json.load(f)["features"]

        ops = [
            UpdateOne(
                {"_id": feat["properties"]["location_id"]},
                {
                    "$set": {
                        "_id": feat["properties"]["location_id"],
                        "properties": feat["properties"],
                        "geometry": feat["geometry"],
                    }
                },
                upsert=True,
            )
            for feat in features
        ]
        if ops:
            self.polygons_col.create_index([("geometry", GEOSPHERE)])
            self.polygons_col.bulk_write(ops)

    def read_turin_polygons(self, include_geometry: bool = True) -> List[TurinPolygonModel]:
        projection = None if include_geometry else {"geometry": 0}
        documents = self.polygons_col.find({}, projection)
        return [
            TurinPolygonModel.model_validate(document) for document in documents
        ]