from chess_validator.board import Board
from chess_validator.pieces import Piece
from chess_validator.validator import basic_checks


def test_basic_checks_rejects_piece_of_wrong_turn():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("black", "pawn"))

    assert basic_checks(board, 6, 4, 5, 4) is False


def test_basic_checks_rejects_move_onto_own_piece():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 4, Piece("white", "knight"))

    assert basic_checks(board, 6, 4, 5, 4) is False


def test_returns_true_for_valid_move():
    board = Board()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 4, None)

    assert basic_checks(board, 6, 4, 5, 4) is True
