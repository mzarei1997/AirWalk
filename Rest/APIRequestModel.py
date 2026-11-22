from pydantic import BaseModel
from typing import Dict, Optional, Type

class APIRequestModel(BaseModel):
    baseUrl: str
    endpoint: str
    payload: Optional[BaseModel] = None
    response_model: Type[BaseModel]
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, str]] = None