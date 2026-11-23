from pydantic import BaseModel

class LocationModel(BaseModel):
    latitude: float
    longitude: float
    
class ApplicationDataModel(BaseModel):
    location: LocationModel
    proximity: int


