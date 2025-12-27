import pytest
from sqlalchemy import select
from backend.database import async_session, User, Rating
from backend.main import app
from fastapi.testclient import TestClient

@pytest.mark.anyio
async def test_get_leaderboard():
    # Setup: Add users and ratings
    async with async_session() as session:
        async with session.begin():
            # Check if users already exist
            u1 = (await session.execute(select(User).where(User.google_id == "leader-1"))).scalar_one_or_none()
            if not u1:
                u1 = User(google_id="leader-1", email="l1@ex.com", name="Top Player")
                session.add(u1)
            
            r1 = (await session.execute(select(Rating).where(Rating.user_id == "leader-1", Rating.variant == "standard"))).scalar_one_or_none()
            if not r1:
                r1 = Rating(user_id="leader-1", variant="standard", rating=2000.0, rd=30.0)
                session.add(r1)
            else:
                r1.rating = 2000.0 # Reset for test
            
            # Create user 2
            u2 = (await session.execute(select(User).where(User.google_id == "leader-2"))).scalar_one_or_none()
            if not u2:
                u2 = User(google_id="leader-2", email="l2@ex.com", name="Second Player")
                session.add(u2)
            
            r2 = (await session.execute(select(Rating).where(Rating.user_id == "leader-2", Rating.variant == "standard"))).scalar_one_or_none()
            if not r2:
                r2 = Rating(user_id="leader-2", variant="standard", rating=1800.0, rd=40.0)
                session.add(r2)
            else:
                r2.rating = 1800.0 # Reset for test

    with TestClient(app) as client:
        response = client.get("/api/leaderboard/standard")
        assert response.status_code == 200
        data = response.json()
        assert data["variant"] == "standard"
        assert len(data["leaderboard"]) >= 2
        # Verify sorting
        assert data["leaderboard"][0]["name"] == "Top Player"
        assert data["leaderboard"][0]["rating"] == 2000
        assert data["leaderboard"][1]["name"] == "Second Player"
        assert data["leaderboard"][1]["rating"] == 1800
