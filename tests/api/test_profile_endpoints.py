import pytest
from sqlalchemy import select
from backend import database
from backend.database import User, Rating

@pytest.mark.anyio
async def test_get_user_profile_success(client):
    google_id = "test-google-id"
    # Setup test user and rating
    async with database.async_session() as session:
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
async def test_get_user_profile_not_found(client):
    response = client.get("/api/user/non-existent-id")
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["name"] == "Anonymous"
    assert data["overall"] == 1500.0