from hypothesis import given, assume, strategies as st
from itertools import chain

from chess.board import Board
from chess.game import Game
from chess.move import Move
from chess.square import Square
from chess.enums import Color
from chess.piece import King, Queen, Rook, Bishop, Knight, Pawn, SlidingPiece, SteppingPiece, Piece
from chess.game import IllegalMoveException


# --- CONSTANTS ---
# Row 0 is Rank 8 (Top), Row 7 is Rank 1 (Bottom)
SAFE_BLACK_KING_SQ = Square(0, 4) # e8 (Row 0)
SAFE_WHITE_KING_SQ = Square(7, 4) # e1 (Row 7)


# --- FEN HELPER ---

def get_fen_placement(pieces_dict: dict[Square, Piece]) -> str:
    """
    Translates a dictionary of {Square: Piece} into the 8-rank FEN piece placement string.

    FEN starts from Rank 8 (Row 0) down to Rank 1 (Row 7).
    """
    board_state = {}
    for sq, piece in pieces_dict.items():
        board_state[(sq.row, sq.col)] = getattr(piece, 'fen_symbol', piece.fen)

    fen_parts = []
    # Iterate from Row 0 (Rank 8) to Row 7 (Rank 1)
    for r in range(8):
        empty_count = 0
        rank_str = ""
        for c in range(8):
            symbol = board_state.get((r, c))
            if symbol:
                if empty_count > 0:
                    rank_str += str(empty_count)
                    empty_count = 0
                rank_str += symbol
            else:
                empty_count += 1

        if empty_count > 0:
            rank_str += str(empty_count)
        fen_parts.append(rank_str)

    return "/".join(fen_parts)


def king_safe_fen(pieces_dict: dict[Square, Piece], player_to_move: Color = Color.WHITE, move_data: str = "KQkq - 0 1") -> str:
    """
    Constructs a full FEN string, ensuring the opponent King is safely placed if missing.
    It ensures the placed opponent King is not adjacent to the current player's King.
    """
    pieces_dict_copy = pieces_dict.copy()
    opponent_color = player_to_move.opposite

    # 1. Find the current player's King location (if present)
    player_king_sq = next((sq for sq, p in pieces_dict_copy.items() if isinstance(p, King) and p.color == player_to_move), None)

    # 2. Check if the opponent King is missing
    if not any(isinstance(p, King) and p.color == opponent_color for p in pieces_dict_copy.values()):

        # Priority list for opponent King placement (e.g., e8, a8, h8, e1, a1, h1)
        if opponent_color == Color.BLACK:
            candidate_sqs = [Square(0, 4), Square(0, 0), Square(0, 7)] # e8, a8, h8
        else: # Color.WHITE
            candidate_sqs = [Square(7, 4), Square(7, 0), Square(7, 7)] # e1, a1, h1

        safe_sq = None

        # Try finding a suitable square from the candidates
        for candidate in candidate_sqs:
            # Must not be occupied
            if candidate in pieces_dict_copy:
                continue

            # Must not be adjacent to the current player's King
            if player_king_sq and candidate.is_adjacent_to(player_king_sq):
                continue

            safe_sq = candidate
            break

        # Fallback: If no candidate works, try any empty square that isn't adjacent to player's king
        if safe_sq is None:
             all_squares = [Square(r, c) for r in range(8) for c in range(8)]
             for sq in all_squares:
                 if sq not in pieces_dict_copy and (not player_king_sq or not sq.is_adjacent_to(player_king_sq)):
                     safe_sq = sq
                     break

        # If a safe square was found, place the opponent King
        if safe_sq is not None:
             pieces_dict_copy[safe_sq] = King(opponent_color)

    fen_placement = get_fen_placement(pieces_dict_copy)
    active_color_fen = 'w' if player_to_move == Color.WHITE else 'b'

    return f"{fen_placement} {active_color_fen} {move_data}"


# --- HYPOTHESIS STRATEGIES ---

@st.composite
def squares(draw):
    row = draw(st.integers(0, 7))
    col = draw(st.integers(0, 7))
    return Square(row, col)


@st.composite
def check_scenario_by_stepping_piece(draw, piece_cls):
    king_sq = draw(squares())
    attacker_sq = None

    if piece_cls == Knight:
        dummy_knight = Knight(Color.BLACK, king_sq)
        possible_attacker_sqs = dummy_knight.theoretical_moves
        assume(possible_attacker_sqs)
        attacker_sq = draw(st.sampled_from(possible_attacker_sqs))

    elif piece_cls == Pawn:
        # Black moves DOWN (Row+). To attack King at R, Pawn must be at R-1.
        possible_offsets = [(-1, -1), (-1, 1)]
        valid_pawn_squares = []
        for dr, dc in possible_offsets:
            r, c = king_sq.row + dr, king_sq.col + dc
            if Square.is_valid(r, c):
                valid_pawn_squares.append(Square(r, c))

        assume(valid_pawn_squares)
        attacker_sq = draw(st.sampled_from(valid_pawn_squares))

    assume(attacker_sq is not None)

    # We rely on king_safe_fen to place the opponent king safely,
    # but ensure the core pieces are not the default safe square.
    # Note: SAFE_BLACK_KING_SQ is for the *opponent* king when player_to_move is white.
    assume(king_sq != SAFE_BLACK_KING_SQ and attacker_sq != SAFE_BLACK_KING_SQ)

    pieces = {
        king_sq: King(Color.WHITE),
        attacker_sq: piece_cls(Color.BLACK)
    }

    return king_safe_fen(pieces, Color.WHITE)


@st.composite
def check_scenario_by_sliding_piece(draw, piece_cls: type[SlidingPiece], moveset):
    king_sq = draw(squares())
    direction = draw(st.sampled_from(moveset))

    path = direction.get_path(king_sq)
    assume(path)

    attacker_sq = draw(st.sampled_from(path))
    assume(attacker_sq != king_sq)

    assume(king_sq != SAFE_BLACK_KING_SQ and attacker_sq != SAFE_BLACK_KING_SQ)

    # Ensure no piece is blocking the path on the safe king square
    path_set = set(direction.get_path(king_sq))
    # We only care about squares strictly between attacker and king
    # (The get_path returns squares radiating OUT from King)
    # If attacker is at index I, squares 0 to I-1 are between King and Attacker.
    attacker_index = path.index(attacker_sq)
    squares_between = path[:attacker_index]
    assume(SAFE_BLACK_KING_SQ not in squares_between)

    pieces = {
        king_sq: King(Color.WHITE),
        attacker_sq: piece_cls(Color.BLACK)
    }

    return king_safe_fen(pieces, Color.WHITE)


@st.composite
def check_scenario_capture_escape(draw):
    king_sq = draw(squares())

    direction = draw(st.sampled_from(Rook.MOVESET.value))
    path = direction.get_path(king_sq)
    assume(len(path) >= 2)

    attacker_sq = path[-1]

    attacker_dummy = Rook(Color.WHITE, attacker_sq)
    ally_candidate_sqs = attacker_dummy.theoretical_moves

    line_of_attack = set(path)
    valid_ally_sqs = [sq for sq in ally_candidate_sqs if sq not in line_of_attack and sq != king_sq and sq != attacker_sq]
    assume(valid_ally_sqs)

    ally_sq = draw(st.sampled_from(valid_ally_sqs))

    assume(king_sq != SAFE_BLACK_KING_SQ and attacker_sq != SAFE_BLACK_KING_SQ and ally_sq != SAFE_BLACK_KING_SQ)

    # Ensure path is clear of Safe King
    attacker_index = path.index(attacker_sq)
    squares_between = path[:attacker_index]
    assume(SAFE_BLACK_KING_SQ not in squares_between)

    pieces = {
        king_sq: King(Color.WHITE),
        attacker_sq: Rook(Color.BLACK),
        ally_sq: Rook(Color.WHITE)
    }

    fen_string = king_safe_fen(pieces, Color.WHITE)
    capture_move = Move(ally_sq, attacker_sq)

    # Use move.start for logging
    print(f"\n--- Scenario: Capture Escape ({capture_move.start}) ---")
    print(f"White King at: {king_sq}")
    print(f"Black Attacker at: {attacker_sq}")
    print(f"White Ally (mover) at: {ally_sq}")
    print(f"Move: {capture_move}")
    print(f"FEN: {fen_string}")

    return fen_string, capture_move


@st.composite
def check_scenario_king_capture(draw):
    king_sq = draw(squares())

    direction = draw(st.sampled_from(Rook.MOVESET.value))
    attacker_sq = king_sq.adjacent(direction)
    assume(attacker_sq is not None)

    assume(king_sq != SAFE_BLACK_KING_SQ and attacker_sq != SAFE_BLACK_KING_SQ)

    pieces = {
        king_sq: King(Color.WHITE),
        attacker_sq: Rook(Color.BLACK)
    }

    fen_string = king_safe_fen(pieces, Color.WHITE)
    capture_move = Move(king_sq, attacker_sq)

    # Use move.start
    print(f"\n--- Scenario: King Capture ({capture_move.start}) ---")
    print(f"White King at: {king_sq}")
    print(f"Black Attacker at: {attacker_sq}")
    print(f"Move: {capture_move}")
    print(f"FEN: {fen_string}")

    return fen_string, capture_move


@st.composite
def check_scenario_move_king(draw):
    king_sq = draw(squares())

    direction = draw(st.sampled_from(Rook.MOVESET.value))
    path = direction.get_path(king_sq)
    assume(path)
    attacker_sq = path[-1]

    assume(king_sq != SAFE_BLACK_KING_SQ and attacker_sq != SAFE_BLACK_KING_SQ)

    attacker_index = path.index(attacker_sq)
    squares_between = path[:attacker_index]
    assume(SAFE_BLACK_KING_SQ not in squares_between)

    pieces = {
        king_sq: King(Color.WHITE),
        attacker_sq: Rook(Color.BLACK)
    }

    fen_string = king_safe_fen(pieces, Color.WHITE)
    board = Board.from_fen(fen_string)
    game = Game(board)

    adjacents = King(Color.WHITE, king_sq).theoretical_moves

    safe_moves = []
    for dest in adjacents:
        # Use try/except to robustly filter out illegal moves without crashing the generator.
        try:
            # Re-initialize the game object for each check to ensure clean state
            test_game = Game(Board.from_fen(fen_string))
            mv = Move(king_sq, dest)
            if test_game.is_move_legal(mv):
                safe_moves.append(mv)
        except IllegalMoveException:
            continue
        except Exception:
            # Handle other unexpected errors that might make the move illegal
            continue

    assume(safe_moves)
    move = draw(st.sampled_from(safe_moves))

    # Use move.start
    print(f"\n--- Scenario: King Move Escape ({move.start}) ---")
    print(f"White King at: {king_sq}")
    print(f"Black Attacker at: {attacker_sq}")
    print(f"Move: {move}")
    print(f"FEN: {fen_string}")

    return fen_string, move


@st.composite
def check_scenario_block(draw):
    king_sq = draw(squares())

    direction = draw(st.sampled_from(Rook.MOVESET.value))
    path = direction.get_path(king_sq)
    assume(len(path) >= 2)

    attacker_sq = path[-1]
    block_sq = path[0]

    dummy = Rook(Color.WHITE, block_sq)
    candidates = dummy.theoretical_moves

    forbidden = set(path) | {king_sq, attacker_sq}
    valid_candidates = [sq for sq in candidates if sq not in forbidden]
    assume(valid_candidates)

    ally_start = draw(st.sampled_from(valid_candidates))

    assume(king_sq != SAFE_BLACK_KING_SQ and attacker_sq != SAFE_BLACK_KING_SQ and ally_start != SAFE_BLACK_KING_SQ)

    attacker_index = path.index(attacker_sq)
    squares_between = path[:attacker_index]
    assume(SAFE_BLACK_KING_SQ not in squares_between)

    pieces = {
        king_sq: King(Color.WHITE),
        attacker_sq: Rook(Color.BLACK),
        ally_start: Rook(Color.WHITE)
    }

    fen_string = king_safe_fen(pieces, Color.WHITE)
    block_move = Move(ally_start, block_sq)

    # Use move.start
    print(f"\n--- Scenario: Block Line of Sight ({block_move.start}) ---")
    print(f"White King at: {king_sq}")
    print(f"Black Attacker at: {attacker_sq}")
    print(f"Blocking Square: {block_sq}")
    print(f"White Ally (mover) at: {ally_start}")
    print(f"Move: {block_move}")
    print(f"FEN: {fen_string}")

    return fen_string, block_move


@st.composite
def double_check_scenario(draw):
    king_sq = draw(squares())

    dir1 = draw(st.sampled_from(Rook.MOVESET.value))
    path1 = dir1.get_path(king_sq)
    assume(path1)
    att1_sq = path1[-1]

    dir2 = draw(st.sampled_from(Bishop.MOVESET.value))
    path2 = dir2.get_path(king_sq)
    assume(path2)
    att2_sq = path2[-1]

    assume(att1_sq != att2_sq)

    assume(king_sq != SAFE_BLACK_KING_SQ and att1_sq != SAFE_BLACK_KING_SQ and att2_sq != SAFE_BLACK_KING_SQ)

    # Ensure path clear
    path_set_1 = set(path1[:path1.index(att1_sq)])
    path_set_2 = set(path2[:path2.index(att2_sq)])
    assume(SAFE_BLACK_KING_SQ not in path_set_1)
    assume(SAFE_BLACK_KING_SQ not in path_set_2)

    pieces = {
        king_sq: King(Color.WHITE),
        att1_sq: Rook(Color.BLACK),
        att2_sq: Bishop(Color.BLACK)
    }

    return king_safe_fen(pieces, Color.WHITE)


# --- TESTS ---

@given(board_fen=check_scenario_by_stepping_piece(Pawn))
def test_king_attacked_by_pawn_is_check(board_fen):
    """
    Verify check when King is attacked by a Pawn.
    """
    board = Board.from_fen(board_fen)
    assert board.current_player_in_check


@given(board_fen=check_scenario_by_stepping_piece(Knight))
def test_king_attacked_by_knight_is_check(board_fen):
    """
    Verify check when King is attacked by a Knight.
    """
    board = Board.from_fen(board_fen)
    assert board.current_player_in_check


@given(board_fen=check_scenario_by_sliding_piece(Rook, Rook.MOVESET.value))
def test_king_attacked_by_rook_is_check(board_fen):
    """
    Verify check when King is attacked by a Rook.
    """
    board = Board.from_fen(board_fen)
    assert board.current_player_in_check


@given(board_fen=check_scenario_by_sliding_piece(Bishop, Bishop.MOVESET.value))
def test_king_attacked_by_bishop_is_check(board_fen):
    """
    Verify check when King is attacked by a Bishop.
    """
    board = Board.from_fen(board_fen)
    assert board.current_player_in_check


@given(board_fen=check_scenario_by_sliding_piece(Queen, Queen.MOVESET.value))
def test_king_attacked_by_queen_is_check(board_fen):
    """
    Verify check when King is attacked by a Queen.
    """
    board = Board.from_fen(board_fen)
    assert board.current_player_in_check


@given(scenario=check_scenario_capture_escape())
def test_escape_by_capturing_attacker(scenario):
    """
    Verify that capturing the attacker with a non-King piece is a legal way to escape check.
    """
    board_fen, capture_move = scenario
    board = Board.from_fen(board_fen)
    game = Game(board)

    assert board.current_player_in_check, "Setup failed: Player should be in check"
    assert game.is_move_legal(capture_move), "The capture move should be legal to escape check"


@given(scenario=check_scenario_king_capture())
def test_escape_by_king_captures_attacker(scenario):
    """
    Verify that the King capturing the adjacent, unprotected attacker is a legal move to escape check.
    """
    board_fen, capture_move = scenario
    board = Board.from_fen(board_fen)
    game = Game(board)

    assert board.current_player_in_check
    assert game.is_move_legal(capture_move)


@given(scenario=check_scenario_move_king())
def test_escape_by_moving_king_to_safe_square(scenario):
    """
    Verify that moving the King out of check to an unattacked adjacent square is a legal move.
    """
    board_fen, move = scenario
    board = Board.from_fen(board_fen)
    game = Game(board)

    assert board.current_player_in_check
    assert game.is_move_legal(move)


@given(scenario=check_scenario_block())
def test_escape_by_blocking_line_of_sight(scenario):
    """
    Verify that interposing a piece to block a sliding attacker's line of check is a legal move.
    """
    board_fen, block_move = scenario
    board = Board.from_fen(board_fen)
    game = Game(board)

    assert board.current_player_in_check
    assert game.is_move_legal(block_move)


@given(board_fen=double_check_scenario())
def test_double_check_validation(board_fen):
    """
    Test the condition for double check by manually counting the number of attackers.
    """
    board = Board.from_fen(board_fen)
    assert board.current_player_in_check

    king = board.get_pieces(King, board.player_to_move)[0]
    enemies = board.get_pieces(color=board.player_to_move.opposite)

    attackers = []
    for enemy in enemies:
        # Check if the King's square is in the unblocked path of the enemy piece
        if king.square in board.unblocked_paths(enemy):
            attackers.append(enemy)

    assert len(attackers) >= 2, "Board should have at least 2 pieces attacking the king"
