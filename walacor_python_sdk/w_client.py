from typing import Any, Optional

import requests


class W_Client:
    def __init__(self, base_url: str, username: str, password: str) -> None:
        self.base_url: str = base_url
        self.username: str = username
        self.password: str = password
        self.token: Optional[str] = None
        self.session: requests.Session = requests.Session()

    def authenticate(self) -> None:
        """Authenticate and store token"""
        response: requests.Response = self.session.post(
            f"{self.base_url}/auth",
            json={"username": self.username, "password": self.password},
        )
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            raise Exception("Authentication failed")

    def request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        """Automatically adds authentication token if available"""
        if self.token:
            kwargs.setdefault("headers", {})["Authorization"] = f"Bearer {self.token}"

        response: requests.Response = self.session.request(
            method, f"{self.base_url}/{endpoint}", **kwargs
        )

        if response.status_code == 401:
            self.authenticate()
            return self.request(method, endpoint, **kwargs)

        return response
