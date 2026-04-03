from chess_validator.validator import validate_move
from chess_validator.board import Board
from chess_validator.pieces import Piece

# Testing through validate_move because pawn rules rely on shared validator checks and it better reflects real usage.

def test_allows_white_pawn_single_step_forward():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert validate_move(board, 6, 4, 5, 4) is True


def test_rejects_white_pawn_single_step_into_occupied_square():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 4, Piece("black", "knight"))

    assert validate_move(board, 6, 4, 5, 4) is False


def test_allows_white_pawn_double_step_from_starting_row():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert validate_move(board, 6, 4, 4, 4) is True


def test_rejects_white_pawn_double_step_when_blocked():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 4, Piece("black", "knight"))

    assert validate_move(board, 6, 4, 4, 4) is False


def test_rejects_white_pawn_double_step_from_non_starting_row():
    board = Board()
    board.turn = "white"
    board.set_piece(5, 4, Piece("white", "pawn"))

    assert validate_move(board, 5, 4, 3, 4) is False


def test_allows_white_pawn_diagonal_capture():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 5, Piece("black", "knight"))

    assert validate_move(board, 6, 4, 5, 5) is True


def test_rejects_white_pawn_diagonal_move_without_capture():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert validate_move(board, 6, 4, 5, 5) is False


def test_rejects_white_pawn_diagonal_move_onto_own_piece():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 5, Piece("white", "knight"))

    assert validate_move(board, 6, 4, 5, 5) is False


def test_rejects_white_pawn_backward_move():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert validate_move(board, 6, 4, 7, 4) is False


def test_allows_black_pawn_single_step_forward():
    board = Board()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))

    assert validate_move(board, 1, 4, 2, 4) is True


def test_allows_black_pawn_double_step_from_starting_row():
    board = Board()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))

    assert validate_move(board, 1, 4, 3, 4) is True


def test_allows_black_pawn_diagonal_capture():
    board = Board()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))
    board.set_piece(2, 3, Piece("white", "knight"))

    assert validate_move(board, 1, 4, 2, 3) is True


def test_rejects_black_pawn_backward_move():
    board = Board()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))

    assert validate_move(board, 1, 4, 0, 4) is False


def test_rejects_black_pawn_diagonal_move_without_capture():
    board = Board()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))

    assert validate_move(board, 1, 4, 2, 3) is False
