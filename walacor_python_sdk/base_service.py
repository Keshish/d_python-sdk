from abc import ABC
from typing import Any, Dict

import requests

from walacor_python_sdk.w_client import W_Client


class BaseService(ABC):
    def __init__(self, client: W_Client) -> None:
        self.client: W_Client = client

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        try:
            response: requests.Response = self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            json_response: Dict[str, Any] = response.json()
            return json_response
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            raise

    def get(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self._request("DELETE", endpoint, **kwargs)
