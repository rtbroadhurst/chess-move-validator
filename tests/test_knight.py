from chess_validator.validator import validate_move
from chess_validator.board import Board
from chess_validator.pieces import Piece


def test_allows_knight_move_two_up_one_left():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))

    assert validate_move(board, 4, 4, 2, 3) is True


def test_allows_knight_move_two_up_one_right():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))

    assert validate_move(board, 4, 4, 2, 5) is True


def test_allows_knight_move_one_up_two_left():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))

    assert validate_move(board, 4, 4, 3, 2) is True


def test_allows_knight_move_one_up_two_right():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))

    assert validate_move(board, 4, 4, 3, 6) is True


def test_rejects_knight_straight_move():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))

    assert validate_move(board, 4, 4, 2, 4) is False


def test_rejects_knight_diagonal_move():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))

    assert validate_move(board, 4, 4, 2, 2) is False


def test_allows_knight_to_jump_over_pieces():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))
    board.set_piece(3, 4, Piece("white", "pawn"))
    board.set_piece(4, 5, Piece("white", "pawn"))

    assert validate_move(board, 4, 4, 2, 5) is True


def test_allows_knight_capture():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))
    board.set_piece(2, 5, Piece("black", "bishop"))

    assert validate_move(board, 4, 4, 2, 5) is True


def test_rejects_knight_move_onto_own_piece():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))
    board.set_piece(2, 5, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 2, 5) is False
