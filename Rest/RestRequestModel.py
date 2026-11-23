from pydantic import BaseModel
from typing import Dict, Optional, Type

class RestRequestModel(BaseModel):
    baseUrl: str
    endpoint: str
    payload: Optional[BaseModel] = None
    response_model: Type[BaseModel]
    headers: Optional[Dict[str, str]] = None
    params: str = None