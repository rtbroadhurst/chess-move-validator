from chess_validator.attacks import is_square_attacked, piece_attacks_square
from chess_validator.board import Board
from chess_validator.pieces import Piece


def test_piece_attacks_square_returns_false_for_same_square():
    board = Board()
    board.set_piece(4, 4, Piece("white", "rook"))

    assert piece_attacks_square(board, 4, 4, 4, 4) is False


def test_white_pawn_attacks_empty_diagonal_square():
    board = Board()
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert piece_attacks_square(board, 6, 4, 5, 5) is True


def test_rook_does_not_attack_through_blocking_piece():
    board = Board()
    board.set_piece(4, 4, Piece("white", "rook"))
    board.set_piece(4, 5, Piece("white", "pawn"))

    assert piece_attacks_square(board, 4, 4, 4, 7) is False


def test_is_square_attacked_detects_pawn_attack():
    board = Board()
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert is_square_attacked(board, 5, 5, "white") is True


def test_king_does_not_attack_two_squares_horizontally():
    board = Board()
    board.set_piece(7, 4, Piece("white", "king"))

    assert piece_attacks_square(board, 7, 4, 7, 6) is False
