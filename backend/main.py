from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from chess.game import Game
from chess.board import Board
from pydantic import BaseModel

from chess.move import Move


app = FastAPI()

origins = [
    "http://localhost:3000"
    "http://127.0.0.1:3000"
    "http://localhost:8000"
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

board = Board.starting_setup()
game = Game(board)


class MoveRequest(BaseModel):
    move_uci: str


class SquareSelection(BaseModel):
    square: str


@app.get("/api/board")
def get_board_state():
    """Returns the current state of the board."""
    board_fen = game.board.fen
    return {"status": "ok", "fen": board_fen, "message": "Initial board state loaded."}


@app.post("/api/move")
def make_move(move_request: MoveRequest):
    """Makes a move."""
    move = Move.from_uci(move_request.move_uci)
    if not game.is_move_legal(move):
        print(f"Illegal move attempt: {move}")
        raise HTTPException(status_code=400, detail=f"Illegal move: {move}.")
    game.take_turn(move)
    return {
        "fen": game.board.fen,
        "status": "success",
    }


@app.post("/api/square/select")
def check_square_selectability(square_request: SquareSelection):
    square = square_request.square
    try:
        return {
            "is_selectable": game.is_square_selectable(square),
            "status": "success",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@app.post("/api/moves/legal")
def legal_moves(square_request: SquareSelection):
    square = game.board.get_square(square_request.square)
    if square.is_empty:
        raise HTTPException(status_code=400, detail=f"{square} has no piece.")
    try:
        return {
            "moves": game.get_legal_moves(square.piece),
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
