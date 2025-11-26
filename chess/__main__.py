from chess.board import Board
from chess.move import Move


def make_move(uci_str: str, board: Board):
    move = Move.from_uci(uci_str)
    board.make_move(move)


def main():
    board = Board.starting_setup()

    while True:
        board.print()

        print(f"Player to move: {board.player_to_move}")
        uci_str = input("Enter a move: ")

        make_move(uci_str, board)


if __name__ == "__main__":
    main()
