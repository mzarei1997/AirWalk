# from Cataloge.AQICN.CatalogeRepository import CatalogeRepository 
# from Cataloge.AQICN.ResponseModelAQICN import AqicnResponseModel
# from Rest.RestRequestModel import RestRequestModel
# from Rest.RestManager import RestManager
# from Connector.DeviceConnector import DeviceConnector
# from Utilities.Utility import Utility
# from MQTT.MqttManager import MQTTManager
# from Utilities.PollingBridge import PollingBridgeService
# from Cataloge.Database import MongoDatabase
# from pathlib import Path


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
        main_connector_mqtt.subscribe(
            model=MQTTRequestModel(
                topic= mqtt_config["location_protocol"]["topic"], 
                payload=None
            ),
                qos=mqtt_config["qos"]
            )
        while True:
            while not deviceConnector.location_queue.empty():
                aqi_data = deviceConnector.fetch_aqi_data() ## check from the course 
                if aqi_data is not None:
                    print(f"[AQI Fetched]")
                    # Publish `aqi_data` to your info topic here

            # main_connector_mqtt.publish(
            #     MQTTRequestModel(
            #         topic=mqtt_config["info_protocol"]["topic"], # to publish the location updates
            #         payload=None ## fill it with proper value
            #     ),
            #     qos= mqtt_config["qos"]
            # )
            # print(f"[Published] {None}")
            time.sleep(3)
    except KeyboardInterrupt:
        main_connector_mqtt.stop()

