from typing import Optional, Type
from pydantic import BaseModel

class MQTTRequestModel(BaseModel):
    topic: str
    payload: Optional[BaseModel] = None
    response_model: Optional[Type[BaseModel]] = None
    qos: int = 1
    retain: bool = False