import pytest
from unittest.mock import patch, MagicMock
from walacor_python_sdk.w_client import W_Client



BASE_URL= "http://fakeapi.com"
USERNAME= "testuser"
PASSWORD= "testpass"
TEST_ENDPOINT = "test-endpoint"

def test_client_authenticate_success():
    """Test that W_Client successfully authenticates and stores token"""
    with patch("requests.Session.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"token": "fake_token"}
        mock_post.return_value = mock_response

        client = W_Client(BASE_URL, USERNAME, PASSWORD)
        client.authenticate()

        assert client.token == "fake_token"
        mock_post.assert_called_once_with(
            f"{BASE_URL}/auth",
            json={"username": USERNAME, "password": PASSWORD},
        )


def test_client_authticate_failure():
    """Test that W_Client raises an exception on failed authentication"""
    with patch("requests.Session.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        client = W_Client(BASE_URL, USERNAME, PASSWORD)

        with pytest.raises(Exception, match="Authentication failed"):
            client.authenticate()

def test_client_request_with_authentication():
    """Test that W_Client adds the authentication token in headers"""
    with patch("requests.Session.post") as mock_post, patch("requests.Session.request") as mock_request:
        # Mock authentication
        mock_auth_response = MagicMock()
        mock_auth_response.status_code = 200
        mock_auth_response.json.return_value = {"token": "fake_token"}
        mock_post.return_value = mock_auth_response

        # Mock request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        client = W_Client(BASE_URL, USERNAME, PASSWORD)
        client.authenticate()  

        response = client.request("GET", TEST_ENDPOINT)

        assert response == mock_response
        mock_request.assert_called_once_with(
            "GET",
            f"{BASE_URL}/test-endpoint",
            headers={"Authorization": "Bearer fake_token"} 
        )

def test_client_request_with_authentication():
    """Test that W_Client re-authenticates and retries on 401 Unauthorized"""
    with patch("requests.Session.post") as mock_post, patch("requests.Session.request") as mock_request:
        # Mock authentication
        mock_auth_response = MagicMock()
        mock_auth_response.status_code = 200
        mock_auth_response.json.return_value = {"token": "fake_token"}
        mock_post.return_value = mock_auth_response

        # Mock request 
        mock_unauth_response = MagicMock()
        mock_unauth_response.status_code = 401

        mock_success_response = MagicMock()
        mock_success_response.status_code = 200

        mock_request.side_effect = [mock_unauth_response, mock_success_response]

        client = W_Client(BASE_URL, USERNAME, PASSWORD)
        response = client.request("GET", TEST_ENDPOINT)

        assert response == mock_success_response
        assert client.token == "fake_token"

        assert mock_post.call_count == 1
        assert mock_request.call_count == 2
