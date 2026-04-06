from chess_validator.movement_rules import generate_pawn_pseudo_legal_moves
from chess_validator.validator import validate_move
from chess_validator.pieces import Piece
from tests.helpers import board_with_kings

# Testing through validate_move because pawn rules rely on shared validator checks and it better reflects real usage.

def test_allows_white_pawn_single_step_forward():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert validate_move(board, 6, 4, 5, 4) is True


def test_rejects_white_pawn_single_step_into_occupied_square():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 4, Piece("black", "knight"))

    assert validate_move(board, 6, 4, 5, 4) is False


def test_allows_white_pawn_double_step_from_starting_row():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert validate_move(board, 6, 4, 4, 4) is True


def test_rejects_white_pawn_double_step_when_blocked():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 4, Piece("black", "knight"))

    assert validate_move(board, 6, 4, 4, 4) is False


def test_rejects_white_pawn_double_step_from_non_starting_row():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(5, 4, Piece("white", "pawn"))

    assert validate_move(board, 5, 4, 3, 4) is False


def test_allows_white_pawn_diagonal_capture():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 5, Piece("black", "knight"))

    assert validate_move(board, 6, 4, 5, 5) is True


def test_rejects_white_pawn_diagonal_move_without_capture():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert validate_move(board, 6, 4, 5, 5) is False


def test_allows_white_en_passant_capture():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(3, 4, Piece("white", "pawn"))
    board.set_piece(3, 5, Piece("black", "pawn"))
    board.en_passant_target = (2, 5)

    assert validate_move(board, 3, 4, 2, 5) is True


def test_rejects_white_pawn_diagonal_move_onto_own_piece():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 5, Piece("white", "knight"))

    assert validate_move(board, 6, 4, 5, 5) is False


def test_rejects_white_pawn_backward_move():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert validate_move(board, 6, 4, 7, 4) is False


def test_allows_black_pawn_single_step_forward():
    board = board_with_kings()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))

    assert validate_move(board, 1, 4, 2, 4) is True


def test_allows_black_pawn_double_step_from_starting_row():
    board = board_with_kings()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))

    assert validate_move(board, 1, 4, 3, 4) is True


def test_allows_black_pawn_diagonal_capture():
    board = board_with_kings()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))
    board.set_piece(2, 3, Piece("white", "knight"))

    assert validate_move(board, 1, 4, 2, 3) is True


def test_rejects_black_pawn_backward_move():
    board = board_with_kings()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))

    assert validate_move(board, 1, 4, 0, 4) is False


def test_rejects_black_pawn_diagonal_move_without_capture():
    board = board_with_kings()
    board.turn = "black"
    board.set_piece(1, 4, Piece("black", "pawn"))

    assert validate_move(board, 1, 4, 2, 3) is False


def test_allows_black_en_passant_capture():
    board = board_with_kings()
    board.turn = "black"
    board.set_piece(4, 4, Piece("black", "pawn"))
    board.set_piece(4, 3, Piece("white", "pawn"))
    board.en_passant_target = (5, 3)

    assert validate_move(board, 4, 4, 5, 3) is True


def test_allows_white_pawn_promotion_with_valid_type():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(1, 4, Piece("white", "pawn"))

    assert validate_move(board, 1, 4, 0, 4, "queen") is True


def test_rejects_white_pawn_promotion_without_type():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(1, 4, Piece("white", "pawn"))

    assert validate_move(board, 1, 4, 0, 4) is False


def test_rejects_white_pawn_promotion_with_invalid_type():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(1, 4, Piece("white", "pawn"))

    assert validate_move(board, 1, 4, 0, 4, "king") is False


def test_rejects_promotion_type_for_non_promotion_move():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))

    assert validate_move(board, 6, 4, 5, 4, "queen") is False


def test_generates_white_pawn_pseudo_legal_moves():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(6, 4, Piece("white", "pawn"))
    board.set_piece(5, 5, Piece("black", "knight"))

    moves = generate_pawn_pseudo_legal_moves(board, 6, 4)

    assert moves == [
        (5, 4),
        (4, 4),
        (5, 3),
        (5, 5),
    ]


def test_generates_white_en_passant_pseudo_legal_move():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(3, 4, Piece("white", "pawn"))
    board.set_piece(3, 5, Piece("black", "pawn"))
    board.en_passant_target = (2, 5)

    moves = generate_pawn_pseudo_legal_moves(board, 3, 4)

    assert moves == [
        (2, 4),
        (1, 4),
        (2, 3),
        (2, 5),
    ]


def test_generates_geometry_targets_for_promoting_white_pawn():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(1, 4, Piece("white", "pawn"))
    board.set_piece(0, 5, Piece("black", "rook"))

    moves = generate_pawn_pseudo_legal_moves(board, 1, 4)

    assert moves == [
        (0, 4),
        (-1, 4),
        (0, 3),
        (0, 5),
    ]
