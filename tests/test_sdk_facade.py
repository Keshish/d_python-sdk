from unittest.mock import patch

from walacor_python_sdk.sdk_facade import SDKFacade


def test_sdk_facade_auth_service_lazy_loading():
    with patch(
        "walacor_python_sdk.authentication.auth_service.AuthService", autospec=True
    ) as mock_auth_service:
        facade = SDKFacade(auth_service_cls=mock_auth_service)

        assert facade._auth is None
        _ = facade.auth
        assert facade._auth is not None
        mock_auth_service.assert_called_once()
