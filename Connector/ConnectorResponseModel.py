import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from pydantic import BaseModel
from Micorservices.ApplicationDataModel import LocationModel

    
def AirQualityAttributes(BaseModel):
    aqi: int
    pm25: float
    pm10: float
    o3: float
    no2: float
    so2: float
    co: float

def PhysicalAttributes(BaseModel):
    size_score: float
    route_score: float
    surface_score: float
    type_score: float
    compactness_score: float
    access_score: float
    pqs: float
    
def ConnectorDetailResponseModel(BaseModel):
    park_location: LocationModel
    park_id: str
    airel_attributes: AirQualityAttributes
    physical_attribute: PhysicalAttributes

def ConnectorResponseModel(BaseModel):
    user_location: LocationModel
    proximity: int
    info: ConnectorDetailResponseModel
    

