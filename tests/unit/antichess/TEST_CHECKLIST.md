# Antichess Test Checklist

This checklist tracks the implementation of tests specifically for the Antichess variant logic.

## Unit Tests (`tests/unit/antichess/`)
- [ ] **Mandatory Capture (`AntichessRules`)**:
    - [ ] Verify `is_move_legal` rejects non-captures when a capture exists.
    - [ ] Verify `get_legal_moves` returns ONLY captures when available.
    - [ ] Verify `get_legal_moves` returns all pseudolegal moves when NO capture exists.
    - [ ] Verify en passant capture counts as a mandatory capture.
- [ ] **King Mechanics**:
    - [ ] Verify `is_check` always returns `False`.
    - [ ] Verify `is_checkmate` always returns `False`.
    - [ ] Verify King is allowed to move into an attacked square.
    - [ ] Verify Castling is illegal (if `NO_CASTLING_RIGHT` is enforced).
- [ ] **Termination Conditions**:
    - [ ] Verify `is_game_over` is `True` when current player has 0 pieces.
    - [ ] Verify `is_game_over` is `True` when current player has pieces but 0 legal moves (Stalemate).
    - [ ] Verify `is_draw` is `False` (Antichess usually resolves to win/loss, though repetition draws exist).

## Component Integration Tests (`tests/component_integration/antichess/`)
- [ ] **Forced Sequences**:
    - [ ] Setup a board where White MUST capture. Verify `Game` rejects other moves.
    - [ ] Setup a chain capture (capture -> opponent MUST capture back).
- [ ] **King Capture**:
    - [ ] Verify King can be captured like a normal piece (if standard Antichess rules apply).

## System Tests (`tests/system/antichess/`)
- [ ] **Full Game**:
    - [ ] Simulate a short Antichess game.
- [ ] **Win by Loss**:
    - [ ] Setup board with 1 White piece. Move it to be captured. Verify White Wins (Game Over).
- [ ] **Win by Stalemate**:
    - [ ] Setup board where White is blocked but has pieces. Verify White Wins.
