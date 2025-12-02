from chess.board import Board
from chess.enums import Color
from chess.game import Game
from chess.move import Move
from chess.piece.king import King


def main():
    fen = "4k3/4R3/r4K2/8/8/8/8/8 w KQkq - 0 1"
    board = Board.from_fen(fen)
    game = Game(board)

    while True:
        board.print()

        print(f"Player to move: {board.player_to_move}")
        print(f"Legal moves: {[str(move) for move in game.legal_moves]}")

        uci_str = input("Enter a move: ")

        try:
            move = Move.from_uci(uci_str)
        except ValueError as e:
            print(e)
            continue

        is_legal, reason = game.is_move_pseudo_legal(move)
        if not is_legal:
            print(f"Illegal move: {reason}")
            continue

        board.make_move(move)


if __name__ == "__main__":
    main()
