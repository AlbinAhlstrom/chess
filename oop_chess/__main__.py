from oop_chess.game import Game, IllegalMoveException
from oop_chess.move import Move
from oop_chess.enums import GameOverReason, MoveLegalityReason


def main():
    game = Game()

    while True:
        print(game.state.board)

        if game.rules.get_game_over_reason(game.state) != GameOverReason.ONGOING:
            message = "Checkmate" if game.rules.get_game_over_reason(game.state) == GameOverReason.CHECKMATE else "Draw"
            print(message)
            break

        print(f"Player to move: {game.state.turn}")
        print(f"Legal moves: {[str(move) for move in game.rules.get_legal_moves(game.state)]}")
        print(f"{game.state.fen=}")

        uci_str = input("Enter a move: ")

        try:
            move = Move(uci_str, game.state.turn)
            if game.rules.validate_move(game.state, move) == MoveLegalityReason.LEGAL:
                game.take_turn(move)
            else:
                print(game.rules.validate_move(game.state, move).value)

        except (ValueError, IllegalMoveException) as e:
            print(e)
            continue


if __name__ == "__main__":
    main()

