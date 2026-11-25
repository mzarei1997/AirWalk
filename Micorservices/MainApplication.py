import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from dataclasses import asdict
from MQTT.MqttRequestModel import MQTTRequestModel
from MQTT.MqttManager import MQTTManager
from Connector.DeviceConnector import DeviceConnector
from Micorservices.ApplicationDataModel import ApplicationDataModel, LocationModel
from Utilities.Utility import Utility
from pydantic import BaseModel
import paho.mqtt.client as mqtt
import random
import json
import time

def prepare_payload() -> BaseModel:
    proximity = random.randint(0, 500)
    payload = ApplicationDataModel(
        location=LocationModel(
            latitude=37.7749,
            longitude=-122.4194
        ),
        proximity=proximity
    )
    return payload

if __name__ == "__main__":
    catalog = Utility.read_json("Cataloge/Cataloge.json")
    mqtt_config = catalog["northbound_mqtt"]

    main_app_mqtt = MQTTManager(
        client_id=mqtt_config["location_protocol"]["client_id"],
        broker=mqtt_config["broker"], 
        port=mqtt_config["port"])
    main_app_mqtt.start()
    
    try:
        main_app_mqtt.subscribe(
            model=MQTTRequestModel(
                topic= mqtt_config["info_protocol"]["topic"],
                payload=None
            ),
            qos=mqtt_config["qos"]
        )
        while True:
            # provider
            payload = prepare_payload()
            main_app_mqtt.publish(
                MQTTRequestModel(
                    topic=mqtt_config["location_protocol"]["topic"], # to publish the location updates
                    payload=payload
                ),
                qos= mqtt_config["qos"]
            )
            print(f"[Published] {payload}")

            time.sleep(10)
    except KeyboardInterrupt:
        main_app_mqtt.stop()
