# System Test Checklist

This checklist tracks high-level system tests that verify the `Game` behaves correctly as a complete unit, simulating real-world usage scenarios.

## Full Game Simulations
- [ ] **Fool's Mate**: Verify the fastest possible checkmate (2 moves).
- [ ] **Scholar's Mate**: Verify a common 4-move checkmate.
- [ ] **The "Opera Game"**: Replay Morphy vs. Duke/Count (1858) to verify a complex, realistic game flow.
- [ ] **Random Legal Game (Fuzzing)**: Play a game with random legal moves for N turns (or until end) to ensure stability and no crashes.

## Game Termination & Draw Conditions
- [ ] **Checkmate**: Verify `is_checkmate` and `is_over` are True, and `game_over_reason` is correct.
- [ ] **Stalemate**: Setup a known stalemate position and verify `is_over`, `is_draw`, and `game_over_reason`.
- [ ] **Insufficient Material**:
    - [ ] K vs K.
    - [ ] K+N vs K.
    - [ ] K+B vs K.
    - [ ] Verify `is_draw` is True.
- [ ] **50-Move Rule**: Simulate 50 moves without capture/pawn move and verify draw claim.
- [ ] **Threefold Repetition**: (Already partially covered in integration, but do a system-level verification with a longer sequence).

## Complex Mechanics Interactions
- [ ] **Castling & Checks**: Verify castling is prevented when:
    - [ ] King is in check.
    - [ ] King passes through check.
    - [ ] King lands in check.
- [ ] **Promotion Sequence**: Pawn moves to 7th, promotes, and the new piece delivers checkmate.
- [ ] **En Passant Chain**: A sequence involving multiple pawn interactions and an en passant capture leading to a discovered check.

## Persistence & State Management
- [ ] **FEN Save/Load Cycle**:
    - [ ] Play N moves.
    - [ ] Get FEN.
    - [ ] Create NEW Game from FEN.
    - [ ] Verify all state (turn, rights, EP, clock) is identical.
    - [ ] Verify next legal moves are identical.
- [ ] **Undo/Redo Stability**:
    - [ ] Play 10 moves.
    - [ ] Undo 10 moves.
    - [ ] Verify state matches start (except maybe move counts if history tracking is simple).
    - [ ] Replay different moves.

## Error Handling & Robustness
- [ ] **Illegal Move Sequences**: Attempt a series of invalid moves (syntax error, logic error, wrong turn) and ensure game state remains consistent and valid.
