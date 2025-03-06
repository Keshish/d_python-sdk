import requests


class W_Client:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()

    def authenticate(self):
        """Authenticate and store token"""
        response = self.session.post(
            f"{self.base_url}/auth",
            json={"username": self.username, "password": self.password},
        )
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            raise Exception("Authentication failed")

    def request(self, method: str, endpoint: str, **kwargs):
        """Automatically adds authentication token if available"""
        if self.token:
            kwargs.setdefault("headers", {})["Authorization"] = f"Bearer {self.token}"

        response = self.session.request(method, f"{self.base_url}/{endpoint}", **kwargs)

        if response.status_code == 401:  
            self.authenticate()
            return self.request(method, endpoint, **kwargs)

        return response
