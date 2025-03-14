from walacor_python_sdk.authentication.auth_service import AuthService
from walacor_python_sdk.sdk_facade import SDKFacade
from walacor_python_sdk.w_client import W_Client


class WalacorService:
    """
    A high-level entry point for users to interact with Walacor.
    """

    def __init__(
        self,
        server: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        self._client: W_Client | None = None
        self._facade: SDKFacade | None = None

        if server and username and password:
            self.setup(server, username, password)

    def setup(self, server: str, username: str, password: str) -> None:
        """Initial setup or re-setup if credentials / server change."""
        self._client = W_Client(server, username, password)
        self._facade = SDKFacade(self._client)

    def changeServer(self, new_server: str) -> None:
        """Change only the server URL, keep the same credentials."""
        if not self._client:
            raise ValueError("Client not initialized. Call setup() first.")
        self._client.base_url = new_server
        self._facade = SDKFacade(self._client)

    def changeCred(self, new_username: str, new_password: str) -> None:
        """Change only the username/password, keep the same server."""
        if not self._client:
            raise ValueError("Client not initialized. Call setup() first.")
        self._client._username = new_username
        self._client._password = new_password
        self._facade = SDKFacade(self._client)

    def changeAll(self, server: str, username: str, password: str) -> None:
        """Change both server and credentials in one call."""
        self.setup(server, username, password)

    @property
    def auth(self) -> AuthService:
        """Expose AuthService under WalacorService.auth"""
        if not self._facade:
            raise ValueError("Service not set up. Call setup() first.")
        return self._facade.auth
