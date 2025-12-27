import pytest
import json
from backend.main import app
from fastapi.testclient import TestClient

def test_atomic_explosion_broadcast(client):
    """
    Test that a capture in Atomic chess correctly broadcasts the explosion_square.
    """
    # 1. Create a new Atomic game
    create_res = client.post("/api/game/new", json={"variant": "atomic"})
    assert create_res.status_code == 200
    game_id = create_res.json()["game_id"]

    # 2. Connect to the WebSocket
    with client.websocket_connect(f"/ws/{game_id}") as ws:
        # Receive initial state
        initial_msg = ws.receive_json()
        assert initial_msg["type"] == "game_state"

        # 3. Setup a capture scenario (Scholar's mate attempt or similar)
        # e2e4, e7e5, d1h5, g7g6, h5xe5 (Explosion at e5)
        moves = ["e2e4", "e7e5", "d1h5", "g7g6"]
        for move in moves:
            ws.send_json({"type": "move", "uci": move})
            ws.receive_json() # Ignore intermediate states

        # 4. Perform the capture
        ws.send_json({"type": "move", "uci": "h5e5"})
        capture_msg = ws.receive_json()

        # 5. Assert explosion detection
        assert capture_msg["type"] == "game_state"
        assert "x" in capture_msg["move_history"][-1] # Ensure it's a capture in SAN
        assert capture_msg["explosion_square"] == "e5" # The critical field we implemented

def test_standard_move_no_explosion(client):
    """
    Test that a standard non-capture move does NOT broadcast an explosion_square.
    """
    create_res = client.post("/api/game/new", json={"variant": "atomic"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as ws:
        ws.receive_json() # init

        ws.send_json({"type": "move", "uci": "e2e4"})
        msg = ws.receive_json()

        assert msg["type"] == "game_state"
        assert msg["explosion_square"] is None
