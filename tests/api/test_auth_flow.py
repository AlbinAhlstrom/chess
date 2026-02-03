from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from backend.main import app

def test_google_auth_creates_user(client: TestClient):
    """
    Test that the /auth endpoint:
    1. Accepts a mock Google token.
    2. Creates a new user in the database.
    3. Sets the session cookie.
    4. Redirects to frontend.
    """
    
    mock_user_info = {
        "sub": "1234567890",
        "email": "testuser@example.com",
        "name": "Test User",
        "picture": "https://example.com/pic.jpg"
    }
    
    mock_token = {
        "userinfo": mock_user_info
    }

    # We mock the method on the oauth.google object
    # Since the endpoint awaits this call, we need an AsyncMock (or a sync func returning a future, but AsyncMock is easiest)
    # The path to patch depends on where it is imported/used.
    # In backend/api/endpoints/auth.py, it is used as `oauth.google.authorize_access_token(request)`
    
    with patch("backend.api.endpoints.auth.oauth.google.authorize_access_token", new_callable=AsyncMock) as mock_auth:
        mock_auth.return_value = mock_token
        
        # 1. Call /auth
        # We need to simulate the callback request.
        # The endpoint expects the oauth lib to handle the request state, but since we mocked authorize_access_token,
        # we might bypass the internal checks if we are lucky, or we might need to mock more.
        # Let's try mocking the result directly.
        
        # Explicitly disable following redirects to assert the redirect header
        response = client.get("/auth/auth", follow_redirects=False)
        
        # Check redirect
        assert response.status_code == 307 or response.status_code == 302
        assert "location" in response.headers
        
        # 2. Verify User is logged in via /api/me
        # TestClient cookies are preserved across requests
        response_me = client.get("/api/me")
        assert response_me.status_code == 200
        data = response_me.json()
        
        assert "user" in data
        user = data["user"]
        assert user["id"] == mock_user_info["sub"]
        assert user["email"] == mock_user_info["email"]
        assert user["name"] == mock_user_info["name"]
        
        # 3. Verify accessing /api/user/{id} works
        response_profile = client.get(f"/api/user/{mock_user_info['sub']}")
        assert response_profile.status_code == 200
        profile_data = response_profile.json()
        assert profile_data["user"]["id"] == mock_user_info["sub"]
