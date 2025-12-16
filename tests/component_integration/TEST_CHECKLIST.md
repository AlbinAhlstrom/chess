# Component Integration Test Checklist

This checklist tracks the implementation of integration tests verifying correct interactions between core components (`Game`, `Rules`, `GameState`, `Board`, `Move`).

## Game <-> Rules <-> Board Interactions
- [ ] **Move Application & Board Mutation**:
    - [ ] Making a move updates the board correctly (piece moved, original square empty).
    - [ ] Capture move updates board (target piece removed, attacker moved).
    - [ ] Castling move updates king AND rook positions.
    - [ ] En passant capture removes the correct pawn (not the destination square).
    - [ ] Promotion move places the promoted piece type.

## Game <-> Rules <-> GameState <-> FEN Helpers Interactions
- [ ] **State Transitions**:
    - [ ] Turn switch (White -> Black -> White).
    - [ ] Castling rights revoked on king/rook move/capture.
    - [ ] En passant square set on double push, cleared next turn.
    - [ ] Halfmove clock reset on pawn move/capture, incremented otherwise.
    - [ ] Fullmove count incremented after Black's move.
    - [ ] `Game` initializes correctly from FEN (using `fen_helpers`).
    - [ ] `Game` serialization (via `GameState.fen`) matches internal state after moves.
- [ ] **Immutability**:
    - [ ] `Game.history` stores distinct `GameState` snapshots (not references to mutated objects).

## Game <-> Move <-> Rules Interactions
- [ ] **Move Validation & Execution**:
    - [ ] `take_turn` raises exception for illegal moves.
    - [ ] `take_turn` executes legal moves.
    - [ ] `legal_moves` returns correct list from `Rules`.
- [ ] **SAN Generation**:
    - [ ] Disambiguation checks (e.g., two knights can move to same square).
    - [ ] Check/Checkmate indicators (+, #).
    - [ ] Capture notation (x).

## Rules <-> Piece <-> Board Interactions
- [ ] **Move Generation Blocking**:
    - [ ] Sliding pieces (Rook, Bishop, Queen) blocked by friendly/enemy pieces.
    - [ ] Knights jumping over pieces.
    - [ ] Pawns blocked by pieces in front.
- [ ] **Check Logic**:
    - [ ] `is_check` correctly identifies attacked king.
    - [ ] `king_left_in_check` prevents moving into check.

## Geometric Integration (Board <-> Square <-> Piece)
- [ ] **Coordinate Alignment**:
    - [ ] Verify `Piece` move patterns map correctly to `Board` coordinates (e.g., Row 0 vs Row 7).
    - [ ] Verify `Square` algebraic notation matches `Board` storage indices.
- [ ] **Boundary Conditions**:
    - [ ] Verify moves near board edges are handled consistently by `Piece` generation and `Board` validation.

## Game <-> History Interactions
- [ ] **Undo/Redo (via History)**:
    - [ ] `undo_move` restores previous `GameState` and `Board`.
    - [ ] `repetitions_of_position` counts accurately based on history.
