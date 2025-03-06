from typing import Optional, Type

from walacor_python_sdk.authentication.auth_service import AuthService
from walacor_python_sdk.w_client import W_Client


class SDKFacade:
    def __init__(
        self, client: W_Client, auth_service_cls: Type[AuthService] = AuthService
    ) -> None:
        self._auth: Optional[AuthService] = None
        self.client: W_Client = client
        self.auth_service_cls: Type[AuthService] = auth_service_cls

    @property
    def auth(self) -> AuthService:
        if self._auth is None:
            self._auth = self.auth_service_cls(self.client)
        return self._auth
