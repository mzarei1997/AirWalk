from dataclasses import asdict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from Connector.DeviceConnector import DeviceConnector
from Micorservices.ApplicationDataModel import ApplicationDataModel, LocationModel
from Utilities.Utility import Utility
import paho.mqtt.client as mqtt
import json
import time
import random

last_info = None
mqtt_topic_info = None
mqtt_topic_location = None
mqtt_qos = 0

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Device Connector connected. Subscribing...")
        client.subscribe(mqtt_topic_info, qos=mqtt_qos)
    else:
        print(f"Connection failed with code {reason_code}")

def on_message(client, userdata, msg):
    global last_info 
    last_info = json.loads(msg.payload.decode("utf-8"))
    print(f"[Received Info] {last_info}")

def prepare_payload():
    proximity = random.randint(0, 500)
    payload = ApplicationDataModel(
        location=LocationModel(
            latitude=37.7749,
            longitude=-122.4194
        ),
        proximity=proximity
    )
    return payload.model_dump_json()

if __name__ == "__main__":
    catalog = Utility.read_json("Cataloge/Cataloge.json")
    mqtt_config = catalog["northbound_mqtt"]

    mqtt_broker = mqtt_config["broker"]
    mqtt_port = mqtt_config["port"]
    mqtt_topic_info = mqtt_config["info_protocol"]["topic"] # to subscribe for info
    mqtt_topic_location = mqtt_config["location_protocol"]["topic"] # to publish the location updates
    mqtt_client_id = mqtt_config["location_protocol"]["client_id"]
    mqtt_qos = mqtt_config["qos"]
    mqtt_keepalive = mqtt_config["keep_alive"]

    Utility.check_qos(mqtt_qos)

    print("Device Connector getting initialized...")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=mqtt_client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, keepalive=mqtt_keepalive)
    client.loop_start()
    print("Device Connector started. Publishing AQI updates...")

    try:
        while True:
            # Reciever
            if last_info is not None:
                print(f"Received info once: {last_info}")
                last_info = None

            # provider
            payload = prepare_payload()
            client.publish(
                topic=mqtt_topic_location,
                payload=payload
            )
            print(f"[Published] {payload}")

            time.sleep(10)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()