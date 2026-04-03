import pytest

import chess_validator.board as board_module
from chess_validator.board import Board
from chess_validator.pieces import Piece


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
    knight = Piece("white", "knight")

    board.set_piece(2, 5, knight)

    assert board.get_piece(2, 5) is knight


def test_set_piece_can_clear_a_square():
    board = Board()
    board.set_piece(2, 5, "N")

    board.set_piece(2, 5, None)

    assert board.get_piece(2, 5) is None


def test_set_piece_raises_for_out_of_bounds_position():
    board = Board()

    with pytest.raises(ValueError):
        board.set_piece(-1, 0, Piece("white", "king"))


def test_is_empty_reports_square_state():
    board = Board()

    assert board.is_empty(1, 1) is True
    board.set_piece(1, 1, Piece("white", "pawn"))
    assert board.is_empty(1, 1) is False


def test_find_king_returns_coordinates_for_matching_colour():
    board = Board()
    board.set_piece(0, 4, Piece("black", "king"))
    board.set_piece(7, 4, Piece("white", "king"))

    assert board.find_king("white") == (7, 4)
    assert board.find_king("black") == (0, 4)


def test_move_piece_returns_false_and_leaves_board_unchanged_for_invalid_move(monkeypatch):
    board = Board()
    pawn = Piece("white", "pawn")
    board.set_piece(6, 4, pawn)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: False)

    moved = board.move_piece(6, 4, 5, 4)

    assert moved is False
    assert board.get_piece(6, 4) is pawn
    assert board.get_piece(5, 4) is None
    assert board.turn == "white"


def test_move_piece_moves_piece_and_switches_turn_for_valid_move(monkeypatch):
    board = Board()
    pawn = Piece("white", "pawn")
    board.set_piece(6, 4, pawn)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    moved = board.move_piece(6, 4, 5, 4)

    assert moved is True
    assert board.get_piece(6, 4) is None
    assert board.get_piece(5, 4) is pawn
    assert board.turn == "black"


def test_move_piece_replaces_destination_piece_when_move_is_valid(monkeypatch):
    board = Board()
    rook = Piece("white", "rook")
    knight = Piece("black", "knight")
    board.set_piece(7, 0, rook)
    board.set_piece(4, 0, knight)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    moved = board.move_piece(7, 0, 4, 0)

    assert moved is True
    assert board.get_piece(7, 0) is None
    assert board.get_piece(4, 0) is rook


def test_load_fen_loads_empty_board():
    board = Board()

    board.load_fen("8/8/8/8/8/8/8/8")

    assert all(square is None for row in board.grid for square in row)


def test_load_fen_places_pieces_on_expected_squares():
    board = Board()

    board.load_fen("4k3/8/8/8/8/8/4P3/4K3")

    black_king = board.get_piece(0, 4)
    white_pawn = board.get_piece(6, 4)
    white_king = board.get_piece(7, 4)

    assert isinstance(black_king, Piece)
    assert black_king.colour == "black"
    assert black_king.kind == "king"

    assert isinstance(white_pawn, Piece)
    assert white_pawn.colour == "white"
    assert white_pawn.kind == "pawn"

    assert isinstance(white_king, Piece)
    assert white_king.colour == "white"
    assert white_king.kind == "king"

    assert board.get_piece(3, 3) is None


def test_load_fen_raises_when_rank_count_is_invalid():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("8/8/8/8/8/8/8")


def test_load_fen_raises_when_rank_width_is_invalid():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("9/8/8/8/8/8/8/8")
