from walacor_python_sdk.walacor_service import WalacorService

walacor_service = WalacorService("http://44.203.135.89/api", "Admin", "GreenDoor99")
walacor_service.auth.login()
