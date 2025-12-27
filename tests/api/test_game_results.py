import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import async_session, User, GameModel
import uuid
import json

@pytest.mark.asyncio
async def test_game_result_history_checkmate(client):
    """Test that 1-0 or 0-1 is appended to move history on checkmate."""
    # Create game via API
    resp = client.post("/api/game/new", json={"variant": "standard"})
    game_id = resp.json()["game_id"]
    
    with client.websocket_connect(f"/ws/{game_id}") as ws:
        ws.receive_json() # Initial
        
        # 1. f3 e5 2. g4 Qh4#
        moves = ["f2f3", "e7e5", "g2g4", "d8h4"]
        for uci in moves:
            ws.send_json({"type": "move", "uci": uci})
            # Receive broadcast
            msg = ws.receive_json()
            if uci == "d8h4":
                # Check history in message
                history = msg["move_history"]
                assert history[-1] == "0-1"
                assert history[-2].endswith("#") # Checkmate suffix

@pytest.mark.asyncio
async def test_game_result_history_resign(client):
    """Test that result is appended on resignation."""
    resp = client.post("/api/game/new", json={"variant": "standard"})
    game_id = resp.json()["game_id"]
    
    with client.websocket_connect(f"/ws/{game_id}") as ws:
        ws.receive_json() # Initial
        
        # White resigns
        # Need to simulate user being White. 
        # In test environment, session might be empty or mocked?
        # main.py checks user_id against white_player_id.
        # If created via API without auth, white_player_id might be None?
        # Let's check new_game logic: 
        # user_session = request.session.get("user") -> None
        # white_id = None.
        # Resign handler: if (not white_id and not black_id): allow.
        
        ws.send_json({"type": "resign"})
        msg = ws.receive_json()
        
        history = msg["move_history"]
        # If white resigns (default assumption in my fix for anon?), 0-1
        # Wait, my fix for anon was: game.resign(game.state.turn) -> White starts -> White resigns -> 0-1
        assert history[-1] == "0-1"

@pytest.mark.asyncio
async def test_game_result_history_draw_agreement(client):
    """Test that 1/2-1/2 is appended on draw agreement."""
    resp = client.post("/api/game/new", json={"variant": "standard"})
    game_id = resp.json()["game_id"]
    
    with client.websocket_connect(f"/ws/{game_id}") as ws:
        ws.receive_json() # Initial
        
        # Make a move so it's not empty history (optional but realistic)
        ws.send_json({"type": "move", "uci": "e2e4"})
        ws.receive_json()
        
        # Send draw accept (simulating agreement, as offer just broadcasts)
        ws.send_json({"type": "draw_accept"})
        msg = ws.receive_json()
        
        history = msg["move_history"]
        assert history[-1] == "1/2-1/2"

