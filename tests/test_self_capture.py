import sys
import os

# Ensure we can import oop_chess from the current directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from oop_chess.game import Game
from oop_chess.board import Board
from oop_chess.move import Move
from oop_chess.square import Square
from oop_chess.enums import Color

def test_capture_own_king_bug():
    print("--- Diagnostic Test: Capture Own King ---")
    
    # 1. Setup Board
    board = Board.starting_setup()
    game = Game(board)
    print("Board initialized with starting setup.")
    
    # 2. Identify White King and White Rook (A1)
    # A1 is Square(7, 0). E1 is Square(7, 4).
    start_sq = Square(7, 0) # A1
    end_sq = Square(7, 4)   # E1
    
    piece_at_start = board.get_piece(start_sq)
    piece_at_end = board.get_piece(end_sq)
    
    print(f"Start Square (A1): {piece_at_start} (Color: {piece_at_start.color if piece_at_start else 'None'})")
    print(f"End Square (E1): {piece_at_end} (Color: {piece_at_end.color if piece_at_end else 'None'})")
    
    if not piece_at_start or piece_at_start.color != Color.WHITE:
        print("FAIL: Expected White piece at A1.")
        return
    if not piece_at_end or piece_at_end.color != Color.WHITE:
        print("FAIL: Expected White piece at E1.")
        return

    # 3. Create Move via UCI (as Backend does)
    move_uci = "a1e1"
    try:
        move = Move.from_uci(move_uci, player_to_move=board.player_to_move)
        print(f"Move created from UCI '{move_uci}': {move}")
    except Exception as e:
        print(f"FAIL: Move.from_uci failed: {e}")
        return

    # 4. Check Pseudo Legality
    is_pseudo, reason = game.is_move_pseudo_legal(move)
    print(f"is_move_pseudo_legal: {is_pseudo}, Reason: '{reason}'")
    
    if is_pseudo:
        print("FAIL: Move should NOT be pseudo-legal (capturing own piece).")
    else:
        print("PASS: Move is correctly rejected as pseudo-illegal.")

    # 5. Check Full Legality
    is_legal = game.is_move_legal(move)
    print(f"is_move_legal: {is_legal}")
    
    if is_legal:
        print("FAIL: Move should NOT be legal.")
    else:
        print("PASS: Move is correctly rejected as illegal.")

    # 6. Check take_turn
    print("Attempting game.take_turn(move)...")
    try:
        game.take_turn(move)
        print("CRITICAL FAIL: take_turn executed the illegal move!")
    except Exception as e:
        print(f"PASS: take_turn raised exception as expected: {e}")

if __name__ == "__main__":
    test_capture_own_king_bug()
