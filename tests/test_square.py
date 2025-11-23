from chess.square import Square, Coordinate


def test_coordinate_from_str():
    c = Coordinate.from_str("e4")
    assert (c.row, c.col) == (4, 4)


def test_coordinate_to_str():
    assert str(Coordinate(7, 0)) == "a1"
    assert str(Coordinate(0, 7)) == "h8"


def test_square_equality():
    s = Square("e4")
    assert s == "e4"
    assert s == (4, 4)
    assert s == Coordinate(4, 4)


def test_square_add_and_remove_piece(board):
    s = board.get_square("a2")
    p = s.piece
    s.remove_piece()
    assert s.piece is None
    s.add_piece(p)
    assert s.piece is p
    assert p.square is s
