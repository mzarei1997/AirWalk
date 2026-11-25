from typing import Optional, Type
from pydantic import BaseModel

class MQTTRequestModel(BaseModel):
    topic: str
    payload: Optional[BaseModel] = None
