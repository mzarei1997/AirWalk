from typing import TypeVar

import requests
from pydantic import BaseModel

from .RestRequestModel import RestRequestModel

class RestManager:
    T = TypeVar("T", bound=BaseModel)

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        self._session = requests.Session()

    def get(
        self,
        model: RestRequestModel
    ) -> T:
        print(f"[Call] {model.baseUrl}/{model.endpoint.lstrip('/')}/{model.params}")
        response = self._session.get(
            f"{model.baseUrl}/{model.endpoint.lstrip('/')}/{model.params}",
            params=model.params or {},
            json=model.payload.model_dump(exclude_none=True) if model.payload else None,
            headers=model.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return model.response_model.model_validate(response.json())

    def post(
        self,
        model: RestRequestModel
    ) -> T:
        response = self._session.post(
            f"{model.baseUrl}/{model.endpoint.lstrip('/')}/{model.params}",
            params=model.params or {},
            json=model.payload.model_dump(exclude_none=True) if model.payload else None,
            headers=model.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return model.response_model.model_validate(response.json())

    def put(
        self,
        model: RestRequestModel
    ) -> T:
        response = self._session.put(
            f"{model.baseUrl}/{model.endpoint.lstrip('/')}/{model.params}",
            params=model.params or {},
            json=model.payload.model_dump(exclude_none=True) if model.payload else None,
            headers=model.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return model.response_model.model_validate(response.json())

    def delete(
        self,
        model: RestRequestModel
    ) -> T:
        response = self._session.delete(
            f"{model.baseUrl}/{model.endpoint.lstrip('/')}/{model.params}",
            params=model.params or {},
            headers=model.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if model.response_model and response.content:
            return model.response_model.model_validate(response.json())
        return None