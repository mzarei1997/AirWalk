from typing import Callable, Optional, Type, TypeVar
import paho.mqtt.client as mqtt
from pydantic import BaseModel
from MQTT.MqttRequestModel import MQTTRequestModel

T = TypeVar("T", bound=BaseModel)

class MQTTManager:
    def __init__(self, client_id: str, broker: str = "localhost", port: int = 1883):
        self._broker = broker
        self._port = port
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self._handlers: dict[str, tuple[Optional[Type[BaseModel]], Callable]] = {}

        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

    def connect(self) -> None:
        self._client.connect(self._broker, self._port)
        self._client.loop_start()

    def disconnect(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    def publish(self, model: MQTTRequestModel) -> None:
        body = model.payload.model_dump_json(exclude_none=True) if model.payload else ""
        self._client.publish(model.topic, payload=body, qos=model.qos, retain=model.retain)

    def subscribe(self, model: MQTTRequestModel, on_receive: Callable[[str, T], None]) -> None:
        self._handlers[model.topic] = (model.response_model, on_receive)
        self._client.subscribe(model.topic, qos=model.qos)

    def _on_connect(self, client, userdata, flags, reason_code, properties) -> None:
        for topic in self._handlers:
            client.subscribe(topic)

    def _on_message(self, client, userdata, msg) -> None:
        raw_text = msg.payload.decode("utf-8")
        for pattern, (response_model, callback) in self._handlers.items():
            if mqtt.topic_matches_sub(pattern, msg.topic):
                parsed = response_model.model_validate_json(raw_text) if response_model else raw_text
                callback(msg.topic, parsed)