from typing import Callable, Optional, Type, TypeVar
import paho.mqtt.client as mqtt
from pydantic import BaseModel
from MQTT.MqttRequestModel import MQTTRequestModel
from Utilities.Utility import Utility
import json

T = TypeVar("T", bound=BaseModel)

class MQTTManager:
    def __init__(self, client_id: str, broker: str = "localhost", port: int = 1883, callback: json = None):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.callback = callback
        self.topics = set()

    def start(self) -> None:
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, model: MQTTRequestModel, qos: int = 0) -> None:
        body = model.payload.model_dump_json(exclude_none=True) if model.payload else ""
        Utility.check_qos(qos)
        self.client.publish(model.topic, payload=body, qos=qos)

    def subscribe(self, model: MQTTRequestModel, qos: int = 0) -> None:
        self.topics.add(model.topic)
        self.client.subscribe(model.topic, qos=qos)

    def unsubscribe(self, model: MQTTRequestModel):
        self.topics.discard(model.topic)
        self.client.unsubscribe(model.topic)

    def on_connect(self, client, userdata, flags, reason_code, properties) -> None:
        for topic in list(self.topics):
            self.client.subscribe(topic=topic)

    def on_message(self, client, userdata, msg) -> json:
        result = json.loads(msg.payload.decode("utf-8"))
        if self.callback:
            self.callback(result)
        return result

    def on_publish(self, client, userdata, mid, reason_code, properties) -> None:
        # print(f"[Published] Message ID: {mid}")
        pass