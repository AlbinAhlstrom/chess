from hypothesis import given
from chess.square import Square
from conftest import rows_cols, squares, square_notation


@given(row=rows_cols(), col=rows_cols())
def test_square_from_row_col_is_valid(row: int, col: int):
    """Checks that creating a Square with valid indices (0-7) does not raise an error."""
    try:
        Square(row, col)
    except ValueError:
        assert False, f"Square({row}, {col}) raised ValueError unexpectedly."


@given(square=squares())
def test_square_to_str_round_trip(square: Square):
    """
    Checks that converting a Square to its algebraic notation and back
    results in the original row and column.
    """
    notation = str(square)
    back_to_square = Square.from_str(notation)
    assert back_to_square == square  # Use the dataclass equality


@given(notation=square_notation())
def test_square_from_str_round_trip(notation: str):
    """
    Checks that converting from algebraic notation to a Square and back
    results in the original notation.
    """
    square = Square.from_str(notation)
    back_to_notation = str(square)
    assert back_to_notation == notation.lower()
