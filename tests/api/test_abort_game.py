import pytest
import json
from v_chess.enums import GameOverReason

@pytest.mark.asyncio
async def test_abort_game_no_moves(client):
    # 1. Create a game via API
    create_res = client.post("/api/game/new", json={"variant": "standard"})
    assert create_res.status_code == 200
    game_id = create_res.json()["game_id"]
    
    # 2. Connect via WebSocket
    with client.websocket_connect(f"/ws/{game_id}") as ws:
        # Initial state
        data = ws.receive_json()
        assert data["type"] == "game_state"
        assert not data["is_over"]
        assert len(data["move_history"]) == 0
        
        # Send resign (which should trigger abort because no moves)
        ws.send_json({"type": "resign"})
        
        # Expect game state update with aborted
        # We might receive multiple messages (e.g. if broadcasts happen), so loop until game_state
        found_aborted = False
        for _ in range(5):
            data = ws.receive_json()
            if data["type"] == "game_state" and data["is_over"]:
                assert data["winner"] == "aborted"
                assert "aborted" in data["move_history"]
                found_aborted = True
                break
        
        assert found_aborted, "Did not receive aborted game state"
