import pytest
from sqlalchemy import select
from backend.database import async_session, User, Rating
from backend.main import app
from fastapi.testclient import TestClient

@pytest.mark.anyio
async def test_get_user_profile_success():
    # Setup: Add a user and some ratings to the DB
    google_id = "test-user-123"
    async with async_session() as session:
        async with session.begin():
            # Check if user exists to avoid duplicates if tests run multiple times on same DB
            stmt = select(User).where(User.google_id == google_id)
            existing_user = (await session.execute(stmt)).scalar_one_or_none()
            if not existing_user:
                user = User(
                    google_id=google_id,
                    email="test@example.com",
                    name="Test User",
                    picture="http://example.com/pic.jpg"
                )
                session.add(user)
                
                # Add a rating
                rating = Rating(
                    user_id=google_id,
                    variant="standard",
                    rating=1600.0,
                    rd=50.0
                )
                session.add(rating)

    with TestClient(app) as client:
        response = client.get(f"/api/user/{google_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["name"] == "Test User"
        assert data["user"]["id"] == google_id
        assert len(data["ratings"]) == 1
        assert data["ratings"][0]["variant"] == "standard"
        assert data["ratings"][0]["rating"] == 1600.0
        assert data["overall"] == 1600.0

@pytest.mark.anyio
async def test_get_user_profile_not_found():
    with TestClient(app) as client:
        response = client.get("/api/user/non-existent-id")
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["name"] == "Anonymous"
        assert data["overall"] == 1500.0
