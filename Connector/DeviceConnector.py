from queue import Queue
from typing import Any, List, Optional
from Cataloge.AQICN.ResponseModelAQICN import AqicnResponseModel
from Rest.RestManager import RestManager
from Rest.RestRequestModel import RestRequestModel
from MQTT.MqttManager import MQTTManager
from Utilities.PollingBridge import PollingBridgeService
from pydantic import BaseModel

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from Utilities.Utility import Utility

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
        self.latest_location: Optional[Any] = None
        cataloge = Utility.read_json("/Users/mohammadreza/Documents/GitHub/AirWalk/Cataloge/Cataloge.json")
        print(cataloge)
        self.config = cataloge["AQICN"]

    def add_polling_source(
        self,
        rest_request: RestRequestModel,
        publish_topic: str,
        interval: float = 10.0,
        qos: int = 1,
        retain: bool = False,
    ) -> None:
        bridge = PollingBridgeService(
            rest_manager=self._api,
            mqtt_manager=self._mqtt,
            rest_request=rest_request,
            publish_topic=publish_topic,
            interval=interval,
            qos=qos,
            retain=retain,
        )
        self._bridges.append(bridge)

        # If the connector is already running, start this bridge immediately
        if self._is_running:
            bridge.start()

    def start(self) -> None:
        if self._is_running:
            return

        self._mqtt.connect()
        for bridge in self._bridges:
            bridge.start()
        self._is_running = True

    def stop(self) -> None:
        if not self._is_running:
            return

        for bridge in self._bridges:
            bridge.stop()
        self._mqtt.disconnect()
        self._is_running = False

    def handle_incoming_location(self, data: BaseModel) -> None:
        self.latest_location = data
        self.location_queue.put(data)
        # print(f"[DeviceConnector] Stored new location: {data}")

    def fetch_aqi_data(self) -> Optional[BaseModel]:
        if self.location_queue.empty():
            return None
        self.latest_location = self.location_queue.get()
        print(self.latest_location)
        requestModel = RestRequestModel(
            baseUrl=self.config["baseUrl"],
            endpoint=self.config["endpoint"],
            headers=self.config["headers"],
            response_model=AqicnResponseModel,
            params= f"geo:{self.latest_location['location']['latitude']};{self.latest_location['location']['longitude']}/?token={self.config['params']['token']}",
        )
        result = self.api.get(requestModel)
        return result

