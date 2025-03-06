from walacor_python_sdk.authentication.auth_service import AuthService

class SDKFacade:
    def __init__(self, auth_service_cls=AuthService): 
        self._auth = None
        self.auth_service_cls = auth_service_cls

    @property
    def auth(self) -> AuthService:
        if self._auth is None:
            self._auth = self.auth_service_cls() 
        return self._auth
