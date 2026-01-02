import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.main import app

@pytest.mark.asyncio
async def test_websocket_connection(client):
    print("Starting test_websocket_connection")
    create_res = client.post("/api/game/new", json={"variant": "standard"})
    game_id = create_res.json()["game_id"]
    print(f"Game created: {game_id}")

    with client.websocket_connect(f"/ws/{game_id}") as websocket:
        print("Connected to websocket")
        data = websocket.receive_json()
        print(f"Received initial state: {data['type']}")
        assert data["type"] == "game_state"
        assert data["fen"] == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

@pytest.mark.asyncio
async def test_websocket_make_move(client):
    print("Starting test_websocket_make_move")
    create_res = client.post("/api/game/new", json={"variant": "standard"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as websocket:
        websocket.receive_json()
        print("Received initial state")

        print("Sending move e2e4")
        websocket.send_json({"type": "move", "uci": "e2e4"})

        # Drain until we get the game_state
        found = False
        for i in range(10): # Avoid infinite loop
            print(f"Waiting for message {i}...")
            data = websocket.receive_json()
            print(f"Received message type: {data.get('type')}")
            if data["type"] == "game_state":
                assert "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1" in data["fen"]
                assert data["turn"] == "b"
                found = True
                break
        assert found, "Did not receive game_state after move"

@pytest.mark.asyncio
async def test_websocket_invalid_move_format(client):
    create_res = client.post("/api/game/new", json={"variant": "standard"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as websocket:
        websocket.receive_json()

        websocket.send_json({"type": "move", "uci": "garbage"})

        data = websocket.receive_json()
        assert data["type"] == "error"

@pytest.mark.asyncio
async def test_websocket_illegal_move_logic(client):
    create_res = client.post("/api/game/new", json={"variant": "standard"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as websocket:
        websocket.receive_json()

        websocket.send_json({"type": "move", "uci": "e2e5"})

        data = websocket.receive_json()
        assert data["type"] == "error"

@pytest.mark.asyncio
async def test_websocket_undo_move(client):
    create_res = client.post("/api/game/new", json={"variant": "standard"})
    game_id = create_res.json()["game_id"]

    with client.websocket_connect(f"/ws/{game_id}") as websocket:
        websocket.receive_json()

        websocket.send_json({"type": "move", "uci": "e2e4"})

        found = False
        for _ in range(10):
            msg = websocket.receive_json()
            if msg["type"] == "game_state":
                found = True; break
        assert found

        websocket.send_json({"type": "undo"})
        pass

@pytest.mark.asyncio
async def test_websocket_checkmate_status(client):
    create_res = client.post("/api/game/new", json={"variant": "standard"})
    game_id = create_res.json()["game_id"]

    moves = ["f2f3", "e7e5", "g2g4", "d8h4"]

    with client.websocket_connect(f"/ws/{game_id}") as websocket:
        websocket.receive_json()

        for m in moves:
            websocket.send_json({"type": "move", "uci": m})
            found = False
            for _ in range(10):
                data = websocket.receive_json()
                if data["type"] == "error":
                    pytest.fail(f"Received error on move {m}: {data.get('message')}")
                if data["type"] == "game_state":
                    if m == "d8h4":
                        assert data["is_over"] is True
                    found = True; break
            assert found
