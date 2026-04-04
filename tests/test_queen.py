from chess_validator.validator import validate_move
from chess_validator.pieces import Piece
from tests.helpers import board_with_kings


def test_allows_queen_vertical_move_on_clear_file():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "queen"))

    assert validate_move(board, 4, 4, 1, 4) is True


def test_allows_queen_horizontal_move_on_clear_rank():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "queen"))

    assert validate_move(board, 4, 4, 4, 7) is True


def test_allows_queen_diagonal_move_on_clear_path():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "queen"))

    assert validate_move(board, 4, 4, 1, 1) is True


def test_rejects_queen_knight_like_move():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "queen"))

    assert validate_move(board, 4, 4, 2, 3) is False


def test_rejects_queen_vertical_move_when_blocked():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "queen"))
    board.set_piece(2, 4, Piece("black", "pawn"))

    assert validate_move(board, 4, 4, 1, 4) is False


def test_rejects_queen_diagonal_move_when_blocked():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "queen"))
    board.set_piece(3, 3, Piece("black", "pawn"))

    assert validate_move(board, 4, 4, 1, 1) is False


def test_allows_queen_capture_on_clear_file():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "queen"))
    board.set_piece(1, 4, Piece("black", "rook"))

    assert validate_move(board, 4, 4, 1, 4) is True


def test_allows_queen_capture_on_clear_diagonal():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "queen"))
    board.set_piece(1, 1, Piece("black", "bishop"))

    assert validate_move(board, 4, 4, 1, 1) is True


def test_rejects_queen_move_onto_own_piece():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "queen"))
    board.set_piece(1, 4, Piece("white", "rook"))

    assert validate_move(board, 4, 4, 1, 4) is False
