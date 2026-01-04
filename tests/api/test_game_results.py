import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend import database
from backend.database import User, GameModel
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
            
            # Drain until we get the state for this move
            while True:
                msg = ws.receive_json()
                if msg.get("type") == "game_state":
                    # Check if this state corresponds to the current move (last move in history matches)
                    # Or just check if it's the checkmate move
                    if uci == "d8h4":
                        history = msg.get("move_history")
                        if history[-1] == "0-1":
                            assert history[-2].endswith("#")
                            break
                        else: continue # Might be an intermediate state
                    break # Not the mate move, just continue to next move

@pytest.mark.asyncio
async def test_game_result_history_resign(client):
    """Test that result is appended on resignation."""
    resp = client.post("/api/game/new", json={"variant": "standard"})
    game_id = resp.json()["game_id"]
    
    with client.websocket_connect(f"/ws/{game_id}") as ws:
        ws.receive_json() # Initial
        
        # Make a move to ensure it's not aborted
        ws.send_json({"type": "move", "uci": "e2e4"})
        
        # Wait for move to be processed
        while True:
            msg = ws.receive_json()
            if msg.get("type") == "game_state" and "e4" in msg.get("move_history", []):
                break

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
        # Wait, my fix for anon was: game.resign(game.state.turn) -> Black starts -> Black resigns -> 1-0?
        # No, turn is Black after e4.
        # If no user_id, resign uses game.state.turn.
        # Turn is Black. So Black resigns.
        # If Black resigns, White wins -> 1-0.
        assert history[-1] == "1-0"

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
        
        while True:
            msg = ws.receive_json()
            if msg.get("type") == "game_state":
                history = msg.get("move_history")
                if history and history[-1] == "1/2-1/2":
                    break

