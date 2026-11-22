from Cataloge.AQICN.ResponseModelAQICN import AqicnResponseModel
from Rest.RestRequestModel import RestRequestModel
from Rest.RestManager import RestManager
from Utilities.DeviceConnector import DeviceConnector
from Utilities.Utility import Utility
from MQTT.MqttManager import MQTTManager
from Utilities.PollingBridge import PollingBridgeService
from MQTT.MqttRequestModel import MQTTRequestModel 
import time



if __name__ == "__main__":

    ########### DeviceConnector Test
    # def subscribe_callback(topic: str, reading: AqicnResponseModel):
    #     city = reading.data.city.name
    #     aqi = reading.data.aqi
    #     print(f"[DB Service] Saving {city} (AQI: {aqi}) from '{topic}'")

    # connector = DeviceConnector(
    #     client_id="airwalk_aqicn_connector",
    #     broker="127.0.0.1",
    #     port=1883,
    # )

    # catalog = Utility.read_json("Cataloge/Cataloge.json")
    # token = catalog["AQICN"]["params"]["token"]
    # # Register Turin AQICN feed
    # connector.add_polling_source(
    #     rest_request=RestRequestModel(
    #         baseUrl="https://api.waqi.info",
    #         endpoint="/feed/geo:45.0703;7.6869/", #??
    #         response_model=AqicnResponseModel,
    #         params={"token": token},
    #     ),
    #     publish_topic="airwalk/turin/aqi",
    #     interval=10.0,
    # )

    # # Easily add a second city on the exact same connector & MQTT connection
    # # connector.add_polling_source(
    # #     api_request=RestRequestModel(
    # #         baseUrl="https://api.waqi.info",
    # #         endpoint="/feed/geo:45.3202;8.4186/",
    # #         response_model=AqicnResponseModel,
    # #         params={"token": "YOUR_TOKEN"},
    # #     ),
    # #     publish_topic="airwalk/vercelli/aqi",
    # #     interval=10.0,
    # # )

    # connector.start()

    # mqtt_for_subsribe = MQTTManager(client_id="airwalk_db_writer", broker="127.0.0.1", port=1883)
    # mqtt_for_subsribe.connect()
    # mqtt_for_subsribe.subscribe(
    #     MQTTRequestModel(
    #         topic="airwalk/turin/aqi",  # Matches 'airwalk/turin/aqi', 'airwalk/vercelli/aqi', etc.
    #         response_model=AqicnResponseModel,
    #     ),
    #     on_receive=subscribe_callback,
    # )

    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     connector.stop()


    ########## MQTT and Polling Test
    # api = RestManager()
    # mqtt_client = MQTTManager(client_id="airwalk_bridge", broker="127.0.0.1", port=1883)
    # print("[PollingBridge] Connecting to MQTT broker at localhost:1883...")
    # mqtt_client.connect()
    # print("[PollingBridge] Connected to MQTT broker at localhost:1883.")
    # request = RestRequestModel(
    #     baseUrl="https://api.waqi.info",
    #     endpoint="/feed/geo:45.0703;7.6869/",
    #     response_model=AqicnResponseModel,
    #     params={"token": "e2bcd0ea67986ee83d9d841a0efdc696df385e9d"},
    # )
    # bridge = PollingBridgeService(
    #     rest_manager=api,
    #     mqtt_manager=mqtt_client,
    #     rest_request=request,
    #     publish_topic="airwalk/turin/aqi",
    #     interval=10.0,
    # )
    # bridge.start()

    # try:
    #     while True:
    #         print("[PollingBridge] Running... Press Ctrl+C to stop.")
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     bridge.stop()
    #     mqtt_client.disconnect()


    ########## cataloge reader test
    # conf = Utility.read_json("Cataloge/Cataloge.json")
    # print(conf)


    ########## API TESTING
    # api_manager = APIManager()
    # res = api_manager.get(
    #     APIRequestModel(
    #         baseUrl="https://api.waqi.info/feed",
    #         endpoint=f"/geo:{45.0703};{7.6869}/",
    #         response_model=AqicnResponseModel,
    #         params={"token": "e2bcd0ea67986ee83d9d841a0efdc696df385e9d"}
    #     )
    # )
    # print(res)

