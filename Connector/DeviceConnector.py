import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
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
        self.last_parks_batch: list[ConnectorResponseModel] = None
        cataloge = Utility.read_json("/Users/mohammadreza/Documents/GitHub/AirWalk/Cataloge/Cataloge.json")
        self.config = cataloge["AQICN"]
        self.create_mongo_repo()
        self.repo = self.create_mongo_repo()
        self.register_resources()

    def get_last_batch(self) -> list[ConnectorResponseModel]:
        if self.location_queue.empty():
            return None
        if self.last_parks_batch is not None:
            return self.last_parks_batch
        else:
            return None

    def get_last_parks_batch(self, user_info: ApplicationDataModel) -> list[ConnectorResponseModel]:
        polygons = self.repo.read_turin_polygons()
        prepared_dateil: list[ConnectorResponseModel] = []
        for polygon in polygons:
            distance = Utility.calculate_distance(
                user_info.location,
                LocationModel(
                    latitude=polygon.properties.midpoint_lat,
                    longitude=polygon.properties.midpoint_lon
                    )
                )
            if distance < user_info.proximity:
                aqi_data = self.fetch_aqi_data(polygon.properties.midpoint_lat, polygon.properties.midpoint_lon)
                park_info = PhysicalAttributes(
                    size_score= polygon.properties.size_score,
                    route_score= polygon.properties.route_score,
                    surface_score= polygon.properties.surface_score,
                    type_score= polygon.properties.type_score,
                    compactness_score= polygon.properties.compactness_score,
                    access_score= polygon.properties.access_score,
                    pqs= polygon.properties.pqs
                )
                air_info = AirQualityAttributes(
                    pm25= getattr(aqi_data.data.iaqi.pm25, "v", 0),
                    pm10= getattr(aqi_data.data.iaqi.pm10, "v", 0),
                    o3= getattr(aqi_data.data.iaqi.o3, "v", 0),
                    no2= getattr(aqi_data.data.iaqi.no2, "v", 0),
                    so2= getattr(aqi_data.data.iaqi.so2, "v", 0),
                    co= getattr(aqi_data.data.iaqi.co, "v", 0)
                )
                prepared_dateil.append(
                    ConnectorResponseModel(
                        user_location=user_info.location,
                        proximity=user_info.proximity,
                        info=ConnectorDetailResponseModel(
                            park_location= LocationModel(latitude=polygon.properties.midpoint_lat, longitude=polygon.properties.midpoint_lon),
                            park_id= polygon.id,
                            distance= distance,
                            airel_attributes= air_info,
                            physical_attribute= park_info
                        )
                    )
                )
        
        return prepared_dateil

    def handle_incoming_location(self, data: dict) -> None:
        data_model = ApplicationDataModel(**data)
        connectorResponse = self.get_last_parks_batch(data_model)
        self.last_parks_batch = connectorResponse
        self.location_queue.put(connectorResponse)

    def fetch_aqi_data(self, lat, lon) -> Optional[AqicnResponseModel]:
        requestModel = RestRequestModel(
            baseUrl=self.config["baseUrl"],
            endpoint=self.config["endpoint"],
            headers=self.config["headers"],
            response_model=AqicnResponseModel,
            params= f"geo:{lat};{lon}/?token={self.config['params']['token']}",
        )
        result = self.api.get(requestModel)
        print(f"[AQI Data Fetched]")
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