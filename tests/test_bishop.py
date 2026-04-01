from chess_validator.validator import validate_move
from chess_validator.board import Board
from chess_validator.pieces import Piece


def test_allows_bishop_move_up_left_on_clear_diagonal():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 2, 2) is True


def test_allows_bishop_move_up_right_on_clear_diagonal():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 2, 6) is True


def test_allows_bishop_move_down_left_on_clear_diagonal():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 6, 2) is True


def test_allows_bishop_move_down_right_on_clear_diagonal():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 6, 6) is True


def test_rejects_bishop_horizontal_move():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 4, 6) is False


def test_rejects_bishop_vertical_move():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 1, 4) is False


def test_rejects_bishop_move_when_blocked_on_diagonal():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))
    board.set_piece(3, 3, Piece("black", "pawn"))

    assert validate_move(board, 4, 4, 2, 2) is False


def test_allows_bishop_capture_when_path_is_clear():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))
    board.set_piece(2, 2, Piece("black", "knight"))

    assert validate_move(board, 4, 4, 2, 2) is True


def test_rejects_bishop_move_onto_own_piece():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))
    board.set_piece(2, 2, Piece("white", "knight"))

    assert validate_move(board, 4, 4, 2, 2) is False
