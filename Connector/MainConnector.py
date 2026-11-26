import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from MQTT.MqttRequestModel import MQTTRequestModel 
from MQTT.MqttManager import MQTTManager
from Connector.DeviceConnector import DeviceConnector
from Utilities.Utility import Utility
import paho.mqtt.client as mqtt
import json
import time
import random

def create_device_connector() -> DeviceConnector:
    cataloge = Utility.read_json("Cataloge/Cataloge.json")
    cataloge_mqtt = cataloge["southbound_mqtt"]
    dc = DeviceConnector(
        client_id=cataloge_mqtt["client_id"],
        broker=cataloge_mqtt["broker"],
        port=cataloge_mqtt["port"],
        api_timeout=cataloge_mqtt["timeout"],
    )
    return dc

if __name__ == "__main__":
    catalog = Utility.read_json("Cataloge/Cataloge.json")
    mqtt_config = catalog["northbound_mqtt"]
    deviceConnector = create_device_connector()
    # deviceConnector.start()

    main_connector_mqtt = MQTTManager(
        client_id=mqtt_config["info_protocol"]["client_id"],
        broker=mqtt_config["broker"], 
        port=mqtt_config["port"],
        callback=deviceConnector.handle_incoming_location
    )
    main_connector_mqtt.start()
    # client.user_data_set({"connector": deviceConnector})

    try:
        # Subscribe
        main_connector_mqtt.subscribe(
            model=MQTTRequestModel(
                topic= mqtt_config["location_protocol"]["topic"], 
                payload=None
            ),
                qos=mqtt_config["qos"]
            )
        print("[MQTT] Subscribed to location updates topic.")
        while True:
            # Publish
            while not deviceConnector.location_queue.empty():
                result = deviceConnector.get_last_batch() ## check from the course 
                if result is not None:
                    for item in result:
                        park_id = item.info.park_id
                        park_topic = mqtt_config["info_protocol"]["topic"].replace("+", park_id)
                        main_connector_mqtt.publish(
                            MQTTRequestModel(
                                topic=park_topic, # to publish the location updates
                                payload=item
                            ),
                            qos= mqtt_config["qos"]
                        )
                        print(f"[Info Published] for park_id: {park_id} at topic: {park_topic}")
                    deviceConnector.location_queue.get()  # Remove the processed item from the queue
                    print(f"[Location Removed] for park_id: {park_id}")
            time.sleep(3)
    except KeyboardInterrupt:
        main_connector_mqtt.stop()

