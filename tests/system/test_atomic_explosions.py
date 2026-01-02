import pytest
import json
from backend.main import app
from fastapi.testclient import TestClient

def wait_for_game_state(ws):
    """Wait for and return the next game_state message, skipping noise."""
    while True:
        msg = ws.receive_json()
        if msg["type"] == "game_state":
            return msg

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
        initial_msg = wait_for_game_state(ws)
        assert initial_msg["type"] == "game_state"

        # 3. Setup a capture scenario (Scholar's mate attempt or similar)
        # e2e4, e7e5, d1h5, g7g6, h5xe5 (Explosion at e5)
        moves = ["e2e4", "e7e5", "d1h5", "g7g6"]
        for move in moves:
            ws.send_json({"type": "move", "uci": move})
            wait_for_game_state(ws) # Ignore intermediate states

        # 4. Perform the capture
        ws.send_json({"type": "move", "uci": "h5e5"})
        capture_msg = wait_for_game_state(ws)

        # 5. Assert explosion detection
        assert capture_msg["type"] == "game_state"
        assert "x" in capture_msg["move_history"][-1] # Ensure it's a capture in SAN
        assert capture_msg["explosion_square"] == "e5" # The critical field we implemented

def test_atomic_pawn_capture_e4d5(client):
    """
    Test specific e4d5 pawn capture reported by user.
    """
    create_res = client.post("/api/game/new", json={"variant": "atomic"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as ws:
        wait_for_game_state(ws) # init

        # Setup: e2e4, d7d5
        ws.send_json({"type": "move", "uci": "e2e4"})
        wait_for_game_state(ws)
        ws.send_json({"type": "move", "uci": "d7d5"})
        wait_for_game_state(ws)

        # Capture: e4d5
        ws.send_json({"type": "move", "uci": "e4d5"})
        msg = wait_for_game_state(ws)

        assert msg["type"] == "game_state"
        assert "x" in msg["move_history"][-1]
        assert msg["explosion_square"] == "d5"

def test_standard_move_no_explosion(client):
    """
    Test that a standard non-capture move does NOT broadcast an explosion_square.
    """
    create_res = client.post("/api/game/new", json={"variant": "atomic"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as ws:
        wait_for_game_state(ws) # init

        ws.send_json({"type": "move", "uci": "e2e4"})
        msg = wait_for_game_state(ws)

        assert msg["type"] == "game_state"
        assert msg["explosion_square"] is None

def test_crazyhouse_drop_broadcast(client):
    """
    Test that a piece drop in Crazyhouse correctly broadcasts the is_drop flag.
    """
    # 1. Create a game with pieces already in pocket (via FEN)
    # White has a Pawn in pocket: [P]
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR[P] w KQkq - 0 1"
    create_res = client.post("/api/game/new", json={"variant": "crazyhouse", "fen": fen})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as ws:
        wait_for_game_state(ws) # init

        # 2. Perform a drop move: P@e4
        ws.send_json({"type": "move", "uci": "P@e4"})
        msg = wait_for_game_state(ws)

        assert msg["type"] == "game_state"
        assert msg["is_drop"] is True

def test_threecheck_strike_broadcast(client):
    """
    Test that a check in Three-Check results in a FEN with updated check counts.
    """
    create_res = client.post("/api/game/new", json={"variant": "threecheck"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as ws:
        wait_for_game_state(ws) # init

        # e2e4, e7e5, d1h5, d8h4, h5xf7+ (Check)
        moves = ["e2e4", "e7e5", "d1h5", "d8h4", "h5f7"]
        last_msg = None
        for move in moves:
            ws.send_json({"type": "move", "uci": move})
            last_msg = wait_for_game_state(ws)

        assert last_msg["type"] == "game_state"
        # Check FEN suffix for +1+0
        assert "+1+0" in last_msg["fen"]

def test_racingkings_turbo_logic(client):
    """
    Test that a King move in Racing Kings is correctly detected.
    """
    # Racing Kings starting position: kings are on the first/second rank
    create_res = client.post("/api/game/new", json={"variant": "racingkings"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as ws:
        wait_for_game_state(ws) # init

        # Move White King: h1h2 (if h1 is king) or h2h3
        # In FEN "8/8/8/8/8/8/krbnNBRK/qrbnNBRQ", h2(row 6, col 7) is King 'K'.
        ws.send_json({"type": "move", "uci": "h2h3"})
        msg = wait_for_game_state(ws)

        assert msg["type"] == "game_state"
        assert msg["uci_history"][-1] == "h2h3"

def test_antichess_shatter_logic(client):
    """
    Test that a capture in Antichess is correctly identified.
    """
    create_res = client.post("/api/game/new", json={"variant": "antichess"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as ws:
        wait_for_game_state(ws) # init

        # e2e4, d7d5, e4xd5 (Mandatory capture often in Antichess)
        ws.send_json({"type": "move", "uci": "e2e4"})
        wait_for_game_state(ws)
        ws.send_json({"type": "move", "uci": "d7d5"})
        wait_for_game_state(ws)
        
        ws.send_json({"type": "move", "uci": "e4d5"})
        msg = wait_for_game_state(ws)

        assert msg["type"] == "game_state"
        assert "x" in msg["move_history"][-1]

