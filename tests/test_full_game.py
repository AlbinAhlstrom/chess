import re
import os
import pytest
from dataclasses import dataclass
from typing import List, Optional, Type, Tuple

from chess.board import Board
from chess.game import Game
from chess.move import Move
from chess.piece.pawn import Pawn
from chess.piece.king import King
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.piece.bishop import Bishop
from chess.piece.knight import Knight
from chess.piece.piece import Piece
from chess.square import Square
from chess.enums import Color

class PGNParser:
    """Parses PGN (Portable Game Notation) formatted game data."""

    @staticmethod
    def parse_moves(pgn_text: str) -> List[str]:
        """
        Extracts a list of moves in SAN (Standard Algebraic Notation) from a PGN string.
        Strips tags, comments, move numbers, and the game result.
        """
        lines = [line for line in pgn_text.splitlines() if not line.startswith("[")]
        text = " ".join(lines)
        
        text = re.sub(r'\{.*?\}', '', text) # Remove comments
        text = re.sub(r'\d+\.', '', text) # Remove move numbers
        text = text.replace("1-0", "").replace("0-1", "").replace("1/2-1/2", "") # Remove result
        
        moves = text.split()
        return moves

    @staticmethod
    def parse_file(file_path: str) -> List[Tuple[str, str, List[str]]]:
        """
        Parses a PGN file containing multiple games.
        Returns a list of games, where each game is a tuple of 
        (white_player, black_player, moves).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PGN file not found: {file_path}")

        with open(file_path, 'r') as f:
            content = f.read()
        
        raw_games = content.split('[Event "')
        games = []
        for raw in raw_games:
            if not raw.strip():
                continue
            
            full_pgn = '[Event "' + raw
            
            white_match = re.search(r'\[White "(.*?)"\]', full_pgn)
            black_match = re.search(r'\[Black "(.*?)"\]', full_pgn)
            white_player = white_match.group(1) if white_match else "Unknown"
            black_player = black_match.group(1) if black_match else "Unknown"

            moves = PGNParser.parse_moves(full_pgn)
            if moves:
                games.append((white_player, black_player, moves))
        
        return games


class SANInterpreter:
    """
    Interprets SAN (Standard Algebraic Notation) strings and converts them
    into Move objects by matching against the game's legal moves.
    """
    def __init__(self, game: Game):
        self.game = game
        self.piece_map = {
            'N': Knight,
            'B': Bishop,
            'R': Rook,
            'Q': Queen,
            'K': King
        }

    def get_move(self, san: str) -> Move:
        """
        Converts a SAN string to a Move object.
        Coordinates parsing and filtering of legal moves.
        """
        legal_moves = self.game.legal_moves
        clean_san = self._clean_san(san)

        castling_move = self._get_castling_move(clean_san, legal_moves)
        if castling_move:
            return castling_move

        clean_san, promotion_char = self._parse_promotion(clean_san)
        piece_type, target_row, target_col, disambiguation = self._parse_piece_info(clean_san)

        candidates = self._find_candidates(
            legal_moves, piece_type, target_row, target_col, promotion_char, disambiguation
        )

        return self._validate_candidates(candidates, san, legal_moves)

    def _clean_san(self, san: str) -> str:
        """Removes decorators like check (+), checkmate (#), and captures (x)."""
        return san.replace("x", "").replace("+", "").replace("#", "")

    def _get_castling_move(self, clean_san: str, legal_moves: List[Move]) -> Optional[Move]:
        """Identifies if the SAN represents castling and returns the corresponding move."""
        if clean_san == "O-O":
            candidates = [m for m in legal_moves if isinstance(self.game.board.get_piece(m.start), King) and abs(m.start.col - m.end.col) == 2 and m.end.col == 6]
            return self._validate_candidates(candidates, clean_san, legal_moves)
        if clean_san == "O-O-O":
            candidates = [m for m in legal_moves if isinstance(self.game.board.get_piece(m.start), King) and abs(m.start.col - m.end.col) == 2 and m.end.col == 2]
            return self._validate_candidates(candidates, clean_san, legal_moves)
        return None

    def _parse_promotion(self, clean_san: str) -> Tuple[str, Optional[str]]:
        """Separates the promotion piece character from the SAN string if present."""
        if "=" in clean_san:
            parts = clean_san.split("=")
            return parts[0], parts[1]
        return clean_san, None

    def _parse_piece_info(self, clean_san: str) -> Tuple[Type[Piece], int, int, str]:
        """
        Parses the SAN string to extract the piece type, target coordinates, 
        and any disambiguation info.
        """
        piece_type = Pawn
        target_str = clean_san[-2:]
        disambiguation = ""

        if clean_san[0] in self.piece_map:
            piece_type = self.piece_map[clean_san[0]]
            disambiguation = clean_san[1:-2]
        else:
            disambiguation = clean_san[:-2]

        target_col = ord(target_str[0]) - ord('a')
        target_row = 8 - int(target_str[1])
        
        return piece_type, target_row, target_col, disambiguation

    def _find_candidates(
        self,
        legal_moves: List[Move],
        piece_type: Type[Piece],
        target_row: int,
        target_col: int,
        promotion_char: Optional[str],
        disambiguation: str
    ) -> List[Move]:
        """Filters legal moves based on parsed criteria."""
        candidates = []
        for move in legal_moves:
            if move.end.row != target_row or move.end.col != target_col:
                continue

            piece = self.game.board.get_piece(move.start)
            if not isinstance(piece, piece_type):
                continue

            if promotion_char:
                if not move.promotion_piece or move.promotion_piece.fen.upper() != promotion_char:
                    continue
            elif move.promotion_piece:
                continue

            if not self._check_disambiguation(move, disambiguation):
                continue

            candidates.append(move)
        return candidates

    def _check_disambiguation(self, move: Move, disambiguation: str) -> bool:
        """
        Checks if a move matches the provided disambiguation string.
        Disambiguation can be by file (e.g., 'Rad1'), rank (e.g., 'R1d2'), or both.
        """
        if not disambiguation:
            return True
            
        start_sq = move.start
        start_file = chr(ord('a') + start_sq.col)
        start_rank = str(8 - start_sq.row)
        
        if len(disambiguation) == 1:
            return disambiguation == start_file or disambiguation == start_rank
        
        return disambiguation == start_file + start_rank

    def _validate_candidates(self, candidates: List[Move], san: str, all_legal_moves: List[Move]) -> Move:
        """
        Validates the filtered candidates. Ensures exactly one matching move exists.
        """
        if len(candidates) == 0:
            self._debug_failure(san, all_legal_moves)
            raise ValueError(f"No matching legal move found for SAN: {san}")
        if len(candidates) > 1:
            raise ValueError(f"Ambiguous move for SAN: {san}. Candidates: {candidates}")
        return candidates[0]

    def _debug_failure(self, san: str, legal_moves: List[Move]):
        """Coordinates debugging output when a move cannot be resolved."""
        print(f"\n--- DEBUG: Failed to find move for {san} ---")
        self._log_board_state()
        self._log_attack_analysis(san)
        self._log_legal_moves(legal_moves)
        print("--------------------------------------------\n")

    def _log_board_state(self):
        """Prints current board visual and FEN."""
        print("Board State:")
        self.game.board.print()
        print(f"FEN: {self.game.board.fen}")
        print(f"Turn: {self.game.board.player_to_move}")

    def _log_attack_analysis(self, san: str):
        """Analyzes and logs why a target square might be invalid (e.g. attacked)."""
        clean_san = self._clean_san(san)
        clean_san, _ = self._parse_promotion(clean_san)
        target_str = clean_san[-2:]
        
        try:
            target_col = ord(target_str[0]) - ord('a')
            target_row = 8 - int(target_str[1])
            target_sq = Square(target_row, target_col)
            print(f"Target Square: {target_sq} ({target_str})")

            is_attacked = self.game.board.is_under_attack(target_sq, self.game.board.player_to_move.opposite)
            print(f"Is target {target_sq} under attack by {self.game.board.player_to_move.opposite}? {is_attacked}")

            if is_attacked:
                self._log_attackers(target_sq)
        except Exception as e:
            print(f"Could not analyze target square: {e}")

    def _log_attackers(self, target_sq: Square):
        """Identifies pieces attacking a specific square."""
        attackers = []
        opponent_pieces = self.game.board.get_pieces(color=self.game.board.player_to_move.opposite)
        for piece in opponent_pieces:
            if isinstance(piece, Pawn):
                if target_sq in piece.capture_squares:
                    attackers.append(piece)
            elif target_sq in self.game.board.unblocked_paths(piece):
                attackers.append(piece)
        print(f"Attackers: {[f'{p} at {p.square}' for p in attackers]}")

    def _log_legal_moves(self, legal_moves: List[Move]):
        """Prints all currently legal moves."""
        print("Legal Moves:")
        for m in legal_moves:
            print(f"  {m}")


# Load games for parametrization
pgn_path = os.path.join(os.path.dirname(__file__), 'example_games.pgn')
games_moves = PGNParser.parse_file(pgn_path)

@pytest.mark.parametrize("white_player,black_player,moves", games_moves, ids=[f"game_{white.replace(' ', '_').replace(',', '')}_{black.replace(' ', '_').replace(',', '')}" for white, black, _ in games_moves])
def test_pgn_game(white_player, black_player, moves):
    """
    Tests a single full game by parsing moves and executing them.
    """
    board = Board.starting_setup()
    game = Game(board)
    interpreter = SANInterpreter(game)
    
    for i, san in enumerate(moves):
        try:
            move = interpreter.get_move(san)
            game.take_turn(move)
        except Exception as e:
            pytest.fail(f"Failed at move {i+1} ('{san}') for game {white_player} vs {black_player}: {e}")
