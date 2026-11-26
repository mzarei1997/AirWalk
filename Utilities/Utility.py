import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from Micorservices.ApplicationDataModel import LocationModel
import json
from math import radians, sin, cos, sqrt, atan2

class Utility:
    @staticmethod
    def read_json(config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config

    @staticmethod
    def check_qos(incoming_qos: int):
        valid_qos = [0, 1, 2]
        if incoming_qos not in valid_qos:
            raise ValueError(f"Invalid QoS value: {incoming_qos}. Must be one of {valid_qos}.")

    @staticmethod
    def calculate_distance(firstLoc: LocationModel, secondLoc: LocationModel):
        R = 6_371_000  # Earth's radius in meters

        lat1, lon1 = radians(firstLoc.latitude), radians(firstLoc.longitude)
        lat2, lon2 = radians(secondLoc.latitude), radians(secondLoc.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c 