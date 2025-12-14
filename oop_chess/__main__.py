from oop_chess.board import Board
from oop_chess.game import Game, IllegalMoveException
from oop_chess.move import Move


def main():
    board = Board.starting_setup()
    game = Game(board)

    while True:
        print(game.state.board)

        if game.is_over:
            message = "Checkmate!" if game.is_checkmate else "Draw!"
            print(message)
            break

        print(f"Player to move: {game.state.turn}")
        print(f"Legal moves: {[str(move) for move in game.legal_moves]}")
        print(f"{game.state.fen=}")

        uci_str = input("Enter a move: ")

        try:
            move = Move.from_uci(uci_str, game.state.turn)
            if game.is_move_legal(move):
                game.take_turn(move)
            else:
                print(game.move_legality_reason(move))

        except (ValueError, IllegalMoveException) as e:
            print(e)
            continue


if __name__ == "__main__":
    main()

