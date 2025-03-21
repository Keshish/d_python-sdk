from unittest.mock import patch

from walacor_python_sdk.sdk_facade import SDKFacade
from walacor_python_sdk.w_client import W_Client

BASE_URL = "http://fakeapi.com"
USERNAME = "testuser"
PASSWORD = "testpass"
TEST_ENDPOINT = "test-endpoint"


def test_sdk_facade_auth_service_lazy_loading():
    """Test that SDKFacade properly initializes AuthService lazily"""
    with patch(
        "walacor_python_sdk.authentication.auth_service.AuthService", autospec=True
    ) as mock_auth_service:
        client = W_Client(BASE_URL, USERNAME, PASSWORD)
        facade = SDKFacade(client=client, auth_service_cls=mock_auth_service)

        assert facade._auth is None

        _ = facade.auth

        assert facade._auth is not None
        mock_auth_service.assert_called_once_with(client)
