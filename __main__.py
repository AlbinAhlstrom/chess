from pieces import Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook, Pawn
from chess import Color, Coordinate, Board


def main():
    """Set up and print the initial chess board.

    This function initializes an 8x8 chess board with all pieces in their
    standard starting positions. It prints the board layout and example moves
    for a sample pawn.

    Example:
        printed output:
        [[♜, ♞, ♝, ♛, ♚, ♝, ♞, ♜], ...]
    """

    def setup_starting_board() -> list[list[Piece]]:
        """Return a list of lists representing the starting chess board.

        Returns:
            8x8 board with pieces in standard starting positions.
        """
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        board = [[None for _ in range(8)] for _ in range(8)]

        board[1] = [Pawn(Color.BLACK, Coordinate(1, col)) for col in range(8)]
        board[6] = [Pawn(Color.WHITE, Coordinate(6, col)) for col in range(8)]

        board[0] = [
            piece(Color.BLACK, Coordinate(0, col))
            for col, piece in enumerate(piece_order)
        ]
        board[7] = [
            piece(Color.WHITE, Coordinate(7, col))
            for col, piece in enumerate(piece_order)
        ]

        return board

    board = setup_starting_board()
    history = [board]
    player_to_move = Color.WHITE
    castle_allowed = [Color.WHITE, Color.BLACK]
    en_passant_square = None
    halfmove_clock = 0

    board = Board(
        board,
        history,
        player_to_move,
        castle_allowed,
        en_passant_square,
        halfmove_clock,
    )
    for row in board.board:
        row = [char or 0 for char in row]
        print(row)


if __name__ == "__main__":
    main()
