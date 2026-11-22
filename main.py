from Cataloge.AQICN.ResponseModelAQICN import AqicnResponseModel
from Rest.APIRequestModel import APIRequestModel
from Rest.APIManager import APIManager
from Utilities.Utility import Utility



if __name__ == "__main__":

    ## cataloge reader test
    # conf = Utility.read_json("Cataloge/Cataloge.json")
    # print(conf)


    ## API TESTING
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

