import pytest

from chess_validator.board import Board


def test_board_starts_with_expected_defaults():
    board = Board()

    assert len(board.grid) == 8
    assert all(len(row) == 8 for row in board.grid)
    assert all(square is None for row in board.grid for square in row)
    assert board.turn == "white"
    assert board.en_passant_target is None


def test_is_in_bounds():
    board = Board()

    assert board.is_in_bounds(0, 0) is True
    assert board.is_in_bounds(7, 7) is True
    assert board.is_in_bounds(4, 2) is True
    assert board.is_in_bounds(-1, 0) is False
    assert board.is_in_bounds(0, -1) is False
    assert board.is_in_bounds(8, 0) is False
    assert board.is_in_bounds(0, 8) is False


def test_get_piece_returns_none_for_empty_square():
    board = Board()

    assert board.get_piece(3, 3) is None


def test_get_piece_raises_for_out_of_bounds_position():
    board = Board()

    with pytest.raises(ValueError):
        board.get_piece(8, 0)


def test_set_piece_stores_piece_on_board():
    board = Board()

    board.set_piece(2, 5, "N")

    assert board.get_piece(2, 5) == "N"


def test_set_piece_can_clear_a_square():
    board = Board()
    board.set_piece(2, 5, "N")

    board.set_piece(2, 5, None)

    assert board.get_piece(2, 5) is None


def test_set_piece_raises_for_out_of_bounds_position():
    board = Board()

    with pytest.raises(ValueError):
        board.set_piece(-1, 0, "K")


def test_is_empty_reports_square_state():
    board = Board()

    assert board.is_empty(1, 1) is True
    board.set_piece(1, 1, "P")
    assert board.is_empty(1, 1) is False


def test_load_fen_loads_empty_board():
    board = Board()

    board.load_fen("8/8/8/8/8/8/8/8")

    assert all(square is None for row in board.grid for square in row)


def test_load_fen_places_pieces_on_expected_squares():
    board = Board()

    board.load_fen("4k3/8/8/8/8/8/4P3/4K3")

    assert board.get_piece(0, 4) == "k"
    assert board.get_piece(6, 4) == "P"
    assert board.get_piece(7, 4) == "K"
    assert board.get_piece(3, 3) is None


def test_load_fen_raises_when_rank_count_is_invalid():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("8/8/8/8/8/8/8")


def test_load_fen_raises_when_rank_width_is_invalid():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("9/8/8/8/8/8/8/8")
