import threading
from typing import Optional
from MQTT.MqttManager import MQTTManager
from MQTT.MqttRequestModel import MQTTRequestModel
from Rest.RestManager import RestManager
from Rest.RestRequestModel import RestRequestModel

class PollingBridgeService:
    def __init__(
        self,
        rest_manager: RestManager,
        mqtt_manager: MQTTManager,
        rest_request: RestRequestModel,
        publish_topic: str,
        interval: float = 10.0,
        qos: int = 1,
        retain: bool = False,
    ):
        self._rest = rest_manager
        self._mqtt = mqtt_manager
        self._rest_request = rest_request
        self._publish_topic = publish_topic
        self._interval = interval
        self._qos = qos
        self._retain = retain

        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join()

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                data = self._rest.get(self._rest_request)
                self._mqtt.publish(
                    MQTTRequestModel(
                        topic=self._publish_topic,
                        payload=data,
                        qos=self._qos,
                        retain=self._retain,
                    )
                )
            except Exception as e:
                print(f"[PollingBridge] Error: {e}")

            self._stop_event.wait(self._interval)