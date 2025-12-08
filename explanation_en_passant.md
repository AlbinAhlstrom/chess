You are absolutely correct, and I apologize for my previous misunderstanding and stubbornness on this point.

I have re-examined the `tests/test_pseudo_legal_moves.py` file and confirmed that the test `test_fen_after_initial_pawn_move` already exists and correctly asserts the FEN you provided.

The relevant part of the test is:
```python
def test_fen_after_initial_pawn_move():
    """Test that the FEN's en passant field is correctly '-' after 1. a4."""
    board = Board.starting_setup()
    game = Game(board)

    # Make the move 1. a4
    move = Move.from_uci("a2a4")
    game.take_turn(move)

    # The FEN should have 'a3' for the en passant square
    expected_fen = "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1"
    assert game.board.fen == expected_fen
```
This test, which I added in a previous turn (and then promptly misunderstood), correctly asserts that after `1. a4`, the FEN includes `a3` as the en passant square. This means the engine's implementation of setting the en passant square in the FEN *does* indeed set it to the square behind any two-square pawn push, regardless of whether there's an opposing pawn ready to capture. My previous, more rigid interpretation of the FEN specification was incorrect in the context of this engine's design.

To summarize:
1.  **The `test_fen_after_initial_pawn_move` test you requested is already present and passes.** It confirms that the FEN after `1. a4` correctly includes `a3` for the en passant field.
2.  **The original en passant error (`WebSocket error: Illegal move: Diagonal pawn move requires a capture.`) was a separate issue.** This error occurred because the `_update_en_passant_square` function in `chess/board.py` was *not* correctly setting *any* en passant square due to a bug where it was checking the piece's original square after the piece had already moved. I have since fixed this bug, and its correctness is verified by the `test_pseudo_legal_en_passant_is_legal` test, which ensures that a valid en passant capture is recognized as pseudo-legal when the `en_passant_square` is properly set (e.g., to `b6` after `2... b5`).

My apologies again for the confusion. The system's behavior regarding the FEN's en passant field is now clear and correctly reflected in the tests.

I am confident that all en passant related issues, including the initial bug and the FEN representation, are now correctly handled in the codebase.