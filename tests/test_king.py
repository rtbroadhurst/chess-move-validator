from chess_validator.validator import validate_move
from chess_validator.board import Board
from chess_validator.pieces import Piece


def test_allows_king_move_one_square_up():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 3, 4) is True


def test_allows_king_move_one_square_down():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 5, 4) is True


def test_allows_king_move_one_square_left():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 4, 3) is True


def test_allows_king_move_one_square_right():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 4, 5) is True


def test_allows_king_move_one_square_diagonally():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 3, 3) is True


def test_rejects_king_move_two_squares_vertically():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 2, 4) is False


def test_rejects_king_move_two_squares_horizontally():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 4, 6) is False


def test_rejects_king_move_two_squares_diagonally():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 2, 2) is False


def test_allows_king_capture():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))
    board.set_piece(3, 3, Piece("black", "bishop"))

    assert validate_move(board, 4, 4, 3, 3) is True


def test_rejects_king_move_onto_own_piece():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))
    board.set_piece(3, 3, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 3, 3) is False
