# from Cataloge.AQICN.CatalogeRepository import CatalogeRepository 
# from Cataloge.AQICN.ResponseModelAQICN import AqicnResponseModel
# from Rest.RestRequestModel import RestRequestModel
# from Rest.RestManager import RestManager
# from Connector.DeviceConnector import DeviceConnector
# from Utilities.Utility import Utility
# from MQTT.MqttManager import MQTTManager
# from Utilities.PollingBridge import PollingBridgeService
# from MQTT.MqttRequestModel import MQTTRequestModel 
# from Cataloge.Database import MongoDatabase
# from pathlib import Path


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from Utilities.Utility import Utility
import paho.mqtt.client as mqtt
import json
import time
import random


last_location = None
mqtt_topic_info = None
mqtt_topic_location = None
mqtt_qos = 0

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Gateway connected. Subscribing...")
        client.subscribe(mqtt_topic_location, qos=mqtt_qos)
    else:
        print(f"Connection failed with code {reason_code}")

def on_message(client, userdata, msg):
    global last_location
    last_location = json.loads(msg.payload.decode("utf-8"))
    print(f"[Received Location] {last_location}")

if __name__ == "__main__":
    catalog = Utility.read_json("Cataloge/Cataloge.json")
    mqtt_config = catalog["northbound_mqtt"]

    mqtt_broker = mqtt_config["broker"]
    mqtt_port = mqtt_config["port"]
    mqtt_topic_info = mqtt_config["info_protocol"]["topic"] # to pubslish the info
    mqtt_client_id = mqtt_config["info_protocol"]["client_id"] 
    mqtt_topic_location = mqtt_config["location_protocol"]["topic"] # to subscribe for location
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
            # receiver
            if last_location is not None:
                print(f"Processing new location once")
                last_location = None
            # provider
            # payload = "air quality update"
            # client.publish(topic=mqtt_topic_info, payload=json.dumps(payload))
            # print(f"[Published AQI] {payload}")

            time.sleep(3)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

