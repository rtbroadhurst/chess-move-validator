from chess_validator.board import Board
from chess_validator.king_safety import is_in_check
from chess_validator.pieces import Piece
from chess_validator.validator import validate_move


def test_is_in_check_returns_true_when_enemy_rook_attacks_king():
    board = Board()
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(0, 4, Piece("black", "king"))
    board.set_piece(7, 0, Piece("black", "rook"))

    assert is_in_check(board, "white") is True


def test_is_in_check_returns_false_when_attack_is_blocked():
    board = Board()
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(0, 4, Piece("black", "king"))
    board.set_piece(7, 0, Piece("black", "rook"))
    board.set_piece(7, 2, Piece("white", "bishop"))

    assert is_in_check(board, "white") is False


def test_validate_move_rejects_move_that_exposes_own_king_to_check():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(0, 7, Piece("black", "king"))
    board.set_piece(7, 3, Piece("white", "rook"))
    board.set_piece(7, 0, Piece("black", "rook"))

    assert validate_move(board, 7, 3, 6, 3) is False


def test_validate_move_allows_blocking_move_that_stops_check():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(0, 7, Piece("black", "king"))
    board.set_piece(5, 2, Piece("white", "bishop"))
    board.set_piece(0, 4, Piece("black", "rook"))

    assert validate_move(board, 5, 2, 3, 4) is True


def test_validate_move_rejects_king_move_onto_attacked_square():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(0, 7, Piece("black", "king"))
    board.set_piece(0, 5, Piece("black", "rook"))

    assert validate_move(board, 7, 4, 6, 5) is False
