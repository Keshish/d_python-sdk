from walacor_python_sdk.sdk_facade import SDKFacade
from walacor_python_sdk.w_client import W_Client


class Main:
    def greeting(self, name: str) -> str:
        return f"Hello {name}"


client = W_Client("http://44.203.135.89/api", "Admin", "GreenDoor99")
instance1 = SDKFacade(client)
instance1.auth.login()
