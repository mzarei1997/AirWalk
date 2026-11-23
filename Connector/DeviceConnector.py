from typing import List
from Rest.RestManager import RestManager
from Rest.RestRequestModel import RestRequestModel
from MQTT.MqttManager import MQTTManager
from Utilities.PollingBridge import PollingBridgeService
from pydantic import BaseModel

class DeviceConnector:

    def __init__(
        self,
        client_id: str,
        broker: str,
        port: int,
        api_timeout: float = 10.0,
    ):
        self._api = RestManager(timeout=api_timeout)
        self._mqtt = MQTTManager(client_id=client_id, broker=broker, port=port)
        self._bridges: List[PollingBridgeService] = []
        self._is_running = False

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
        # self.location_queue.put(data)
        print(f"[DeviceConnector] Stored new location: {data}")
        print("----------------------------")