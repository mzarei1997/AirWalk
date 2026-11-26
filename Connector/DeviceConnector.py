import json
from queue import Queue
from typing import Any, List, Optional
from Cataloge.AQICN.CatalogeRepository import CatalogeRepository
from Cataloge.AQICN.ResponseModelAQICN import AqicnResponseModel
from Rest.RestManager import RestManager
from Rest.RestRequestModel import RestRequestModel
from MQTT.MqttManager import MQTTManager
from Utilities.PollingBridge import PollingBridgeService
from pydantic import BaseModel
from Micorservices.ApplicationDataModel import LocationModel, ApplicationDataModel

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Utilities.Utility import Utility

from Connector.ConnectorResponseModel import AirQualityAttributes, PhysicalAttributes, ConnectorDetailResponseModel, ConnectorResponseModel 

class DeviceConnector:

    def __init__(
        self,
        client_id: str,
        broker: str,
        port: int,
        api_timeout: float = 10.0,
    ):
        self.api = RestManager(timeout=api_timeout)
        self._mqtt = MQTTManager(client_id=client_id, broker=broker, port=port)
        self._bridges: List[PollingBridgeService] = []
        self._is_running = False

        # Queue and state for incoming MQTT updates
        self.location_queue: Queue = Queue()
        self.last_parks_batch: ConnectorResponseModel = None
        cataloge = Utility.read_json("/Users/mohammadreza/Documents/GitHub/AirWalk/Cataloge/Cataloge.json")
        self.config = cataloge["AQICN"]
        self.create_mongo_repo()
        self.repo = self.create_mongo_repo()
        self.register_resources()


    def get_last_parks_batch(self, user_info: ApplicationDataModel):
        polygons = self.repo.read_turin_polygons()
        parks_info = []
        airels_info = []
        for polygon in polygons:
            distance = Utility.calculate_distance(
                user_info.location,
                LocationModel(
                    latitude=polygon.properties.midpoint_lat,
                    longitude=polygon.properties.midpoint_lon
                    )
                )
            if distance < user_info.proximity:
                park_info = PhysicalAttributes(
                    size_score: polygon.property.size_score,
                    route_score: polygon.property.route_score,
                    surface_score: polygon.property.surface_score,
                    type_score: polygon.property.type_score,
                    compactness_score: polygon.property.compactness_score,
                    access_score: polygon.property.access_score,
                    pqs: polygon.property.pqs
                )
                air_info = AirQualityAttributes(
                    aqi: int,
                    pm25: float,
                    pm10: float,
                    o3: float,
                    no2: float,
                    so2: float,
                    co: float
                )
                
                
                parks_info.append(air_info)
                airels_info.append(air_info)
        self.last_parks_batch = ConnectorResponseModel(
            user_location=user_info.location,
            proximity=user_info.proximity,
            info=ConnectorDetailResponseModel(
                park_location=LocationModel(
                    latitude=polygon.properties.midpoint_lat,
                    longitude=polygon.properties.midpoint_lon
                ),
                park_id=polygon.properties.park_id,
                airel_attributes=airels_info,
                physical_attribute=parks_info
            )
        )
                
        
    def handle_incoming_location(self, data: dict) -> None:
        data_model = ApplicationDataModel(**data)
        self.get_last_parks_batch(data_model)
        self.last_parks_batch = data
        self.location_queue.put(data)

    def fetch_aqi_data(self) -> Optional[BaseModel]:
        if self.location_queue.empty():
            return None
        self.last_parks_batch = self.location_queue.get()
        requestModel = RestRequestModel(
            baseUrl=self.config["baseUrl"],
            endpoint=self.config["endpoint"],
            headers=self.config["headers"],
            response_model=AqicnResponseModel,
            params= f"geo:{self.latest_location['location']['latitude']};{self.latest_location['location']['longitude']}/?token={self.config['params']['token']}",
        )
        result = self.api.get(requestModel)
        return result

    def register_resources(self) :
        mongo_config = self.get_mongo_config()
        self.repo.write_turin_polygons(file_path=mongo_config["collections"]["polygons"]["address"])

    def create_mongo_repo(self) -> CatalogeRepository:
        mongo_config = self.get_mongo_config()
        return CatalogeRepository(
            mongo_uri=mongo_config["url"],
            db_name=mongo_config["db_name"] 
        )

    def get_mongo_config(self) -> json:
        cataloge = Utility.read_json("/Users/mohammadreza/Documents/GitHub/AirWalk/Cataloge/Cataloge.json")
        mongo_config = cataloge["mongodb"]
        return mongo_config