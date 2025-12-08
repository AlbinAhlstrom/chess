I understand. Thank you for providing that clarification from Wikipedia. It explicitly states that under the "old standard," which you prefer and which chess.com uses, the en passant target square is recorded regardless of whether a pawn is in a position to capture en passant.

My current implementation and the tests I've written already reflect this "old standard" behavior:

*   The `_update_en_passant_square` method sets the en passant target square (e.g., `a3` after `1. a4`) whenever a pawn moves two squares, without checking for an opposing pawn.
*   The test `test_fen_after_initial_pawn_move` (which expects `a3` after `1. a4`) passes, confirming this behavior.

Therefore, the codebase is currently following the "old standard" for FEN en passant representation that you desire.

Could you please clarify what specific change you would like me to make? The current implementation aligns with your stated preference.