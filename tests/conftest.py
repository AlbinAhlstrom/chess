import os
import uuid
import asyncio
import pytest
from hypothesis import strategies as st
from fastapi.testclient import TestClient
from sqlalchemy import event

# Force a separate test database before importing app
# Use a unique file in tests/ dir for the whole session
test_db_name = f"test_chess_{uuid.uuid4().hex}.db"
test_db_path = os.path.join(os.path.dirname(__file__), test_db_name)
print(f"DEBUG: tests/conftest.py setting DATABASE_URL to sqlite+aiosqlite:///{test_db_path}")
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{test_db_path}"

# CRITICAL: Setup database before any backend imports
from backend import database
database.setup_database(os.environ["DATABASE_URL"])

from backend.main import app
from backend.database import init_db
from v_chess.square import Square
from v_chess.enums import Color
from v_chess.piece.piece import Piece
from v_chess.piece import piece_from_char
from typing import Type

random_row_col = st.integers(min_value=0, max_value=7)
piece_types: list[Type[Piece]] = list(set(piece_from_char.values()))
random_color = st.sampled_from(Color)
random_piece_cls = st.sampled_from(piece_types)

@st.composite
def random_square(draw):
    return draw(st.builds(Square, random_row_col, random_row_col))

@st.composite
def random_piece(draw):
    piece_cls = draw(random_piece_cls)
    color = draw(random_color)
    return piece_cls(color)

@st.composite
def random_square_str(draw):
    file_char = draw(st.sampled_from("abcdefgh"))
    rank_char = draw(st.sampled_from("12345678"))
    return file_char + rank_char

from backend.state import games, game_variants, seeks, quick_match_queue, pending_takebacks

@pytest.fixture(autouse=True)
def clear_state():
    """Clear global in-memory state before each test to prevent leakage."""
    games.clear()
    game_variants.clear()
    seeks.clear()
    quick_match_queue.clear()
    pending_takebacks.clear()
    yield

@pytest.fixture(scope="module", autouse=True)
def setup_test_db(request):
    """Module-level setup to ensure DB is initialized."""
    # Skip for E2E tests which use their own environment/DB
    # Also skip for unit tests which don't need a database
    path = str(request.node.fspath)
    if "tests/e2e" in path or "tests/unit" in path:
        yield
        return
    
    # Run init using a separate thread to avoid "running event loop" conflicts
    import threading
    
    def _run_init():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            new_loop.run_until_complete(init_db())
        finally:
            new_loop.close()

    thread = threading.Thread(target=_run_init)
    thread.start()
    thread.join()
    
    # Debug: Verify DB exists and is writable
    assert os.path.exists(test_db_path), f"DB file {test_db_path} not created"
    assert os.access(test_db_path, os.W_OK), f"DB file {test_db_path} is not writable"
    
    yield
    # Cleanup happens in pytest_sessionfinish

def pytest_sessionfinish(session, exitstatus):
    """Cleanup the session database file after all tests are done."""
    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
            print(f"DEBUG: Cleaned up session DB at {test_db_path}")
        except Exception as e:
            print(f"DEBUG: Failed to cleanup session DB: {e}")

@pytest.fixture(scope="module")
def client():
    # Lifespan will also call init_db, which is fine (idempotent)
    with TestClient(app) as c:
        yield c
