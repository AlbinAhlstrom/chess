import pytest
import asyncio
import json
from backend.state import quick_match_queue
from backend.services.matchmaking_service import match_players
from backend.socket_manager import manager

@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_quick_match_success(client):
    # Ensure queue is empty
    quick_match_queue.clear()
    
    # Manually populate the queue
    quick_match_queue.append({
        "user_id": "user1",
        "variant": "standard",
        "time_control": {"limit": 600, "increment": 0},
        "rating": 1500,
        "range": 200,
        "joined_at": 0
    })
    
    quick_match_queue.append({
        "user_id": "user2",
        "variant": "standard",
        "time_control": {"limit": 600, "increment": 0},
        "rating": 1600,
        "range": 200,
        "joined_at": 0
    })
    
    # We need to mock manager.broadcast_lobby to avoid errors if no one is connected
    # or just let it run if it handles empty connections gracefully.
    
    # Run the matching logic directly
    await match_players()
    
    # Assertions
    assert len(quick_match_queue) == 0  # Should be matched and removed
    
@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_quick_match_no_match_rating(client):
    quick_match_queue.clear()
    
    quick_match_queue.append({
        "user_id": "user1",
        "variant": "standard",
        "time_control": {"limit": 600, "increment": 0},
        "rating": 1500,
        "range": 50,
        "joined_at": 0
    })
    
    quick_match_queue.append({
        "user_id": "user2",
        "variant": "standard",
        "time_control": {"limit": 600, "increment": 0},
        "rating": 1600,
        "range": 50,
        "joined_at": 0
    })
    
    await match_players()
    
    assert len(quick_match_queue) == 2

@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_quick_match_no_match_variant(client):
    quick_match_queue.clear()
    
    quick_match_queue.append({
        "user_id": "user1",
        "variant": "standard",
        "time_control": {"limit": 600, "increment": 0},
        "rating": 1500,
        "range": 200,
        "joined_at": 0
    })
    
    quick_match_queue.append({
        "user_id": "user2",
        "variant": "atomic",
        "time_control": {"limit": 600, "increment": 0},
        "rating": 1500,
        "range": 200,
        "joined_at": 0
    })
    
    await match_players()
    
    assert len(quick_match_queue) == 2