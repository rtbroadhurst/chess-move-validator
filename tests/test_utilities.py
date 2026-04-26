from chess_validator.utilities import square_to_coords, coords_to_square


def test_square_to_coords():
    assert square_to_coords("a8") == (0, 0)
    assert square_to_coords("h1") == (7, 7)
    assert square_to_coords("e4") == (4, 4)


def test_coords_to_square():
    assert coords_to_square(0, 0) == "a8"
    assert coords_to_square(7, 7) == "h1"
    assert coords_to_square(4, 4) == "e4"


def test_square_to_coords_and_coords_to_square():
    square = "c6"
    row, col = square_to_coords(square)
    assert coords_to_square(row, col) == square
