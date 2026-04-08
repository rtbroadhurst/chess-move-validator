from chess_validator.movement_rules import generate_rook_pseudo_legal_moves
from chess_validator.validator import validate_move
from chess_validator.pieces import Piece
from .helpers import board_with_kings

def test_allows_rook_vertical_move_on_clear_file():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))

    assert validate_move(board, 7, 0, 4, 0) is True


def test_allows_rook_horizontal_move_on_clear_rank():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))

    assert validate_move(board, 7, 0, 7, 5) is True


def test_rejects_rook_diagonal_move():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))

    assert validate_move(board, 7, 0, 5, 2) is False


def test_rejects_rook_vertical_move_when_blocked():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))
    board.set_piece(5, 0, Piece("black", "pawn"))

    assert validate_move(board, 7, 0, 4, 0) is False


def test_rejects_rook_horizontal_move_when_blocked():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))
    board.set_piece(7, 3, Piece("black", "pawn"))

    assert validate_move(board, 7, 0, 7, 5) is False


def test_allows_rook_capture_when_path_is_clear():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))
    board.set_piece(4, 0, Piece("black", "knight"))

    assert validate_move(board, 7, 0, 4, 0) is True


def test_rejects_rook_move_onto_own_piece():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))
    board.set_piece(4, 0, Piece("white", "knight"))

    assert validate_move(board, 7, 0, 4, 0) is False


def test_generates_rook_pseudo_legal_moves_until_board_edge():
    board = board_with_kings()
    board.set_piece(4, 4, Piece("white", "rook"))

    moves = generate_rook_pseudo_legal_moves(board, 4, 4)

    assert moves == [
        (3, 4),
        (2, 4),
        (1, 4),
        (0, 4),
        (5, 4),
        (6, 4),
        (7, 4),
        (4, 3),
        (4, 2),
        (4, 1),
        (4, 0),
        (4, 5),
        (4, 6),
        (4, 7),
    ]


def test_generates_rook_pseudo_legal_moves_stop_at_first_blocker():
    board = board_with_kings()
    board.set_piece(4, 4, Piece("white", "rook"))
    board.set_piece(2, 4, Piece("black", "pawn"))
    board.set_piece(4, 6, Piece("white", "pawn"))

    moves = generate_rook_pseudo_legal_moves(board, 4, 4)

    assert moves == [
        (3, 4),
        (2, 4),
        (5, 4),
        (6, 4),
        (7, 4),
        (4, 3),
        (4, 2),
        (4, 1),
        (4, 0),
        (4, 5),
        (4, 6),
    ]
