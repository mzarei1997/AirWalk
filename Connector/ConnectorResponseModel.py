import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from pydantic import BaseModel
from Micorservices.ApplicationDataModel import LocationModel

class AirQualityAttributes(BaseModel):
    pm25: float
    pm10: float
    o3: float
    no2: float
    so2: float
    co: float

class PhysicalAttributes(BaseModel):
    size_score: float
    route_score: float
    surface_score: float
    type_score: float
    compactness_score: float
    access_score: float
    pqs: float
    
class ConnectorDetailResponseModel(BaseModel):
    park_location: LocationModel
    park_id: str
    distance: float
    airel_attributes: AirQualityAttributes
    physical_attribute: PhysicalAttributes

class ConnectorResponseModel(BaseModel):
    user_location: LocationModel
    proximity: int
    info: ConnectorDetailResponseModel
    

