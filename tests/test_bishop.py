from chess_validator.movement_rules import generate_bishop_pseudo_legal_moves
from chess_validator.validator import validate_move
from chess_validator.pieces import Piece
from tests.helpers import board_with_kings


def test_allows_bishop_move_up_left_on_clear_diagonal():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 2, 2) is True


def test_allows_bishop_move_up_right_on_clear_diagonal():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 2, 6) is True


def test_allows_bishop_move_down_left_on_clear_diagonal():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 6, 2) is True


def test_allows_bishop_move_down_right_on_clear_diagonal():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 6, 6) is True


def test_rejects_bishop_horizontal_move():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 4, 6) is False


def test_rejects_bishop_vertical_move():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 1, 4) is False


def test_rejects_bishop_move_when_blocked_on_diagonal():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))
    board.set_piece(3, 3, Piece("black", "pawn"))

    assert validate_move(board, 4, 4, 2, 2) is False


def test_allows_bishop_capture_when_path_is_clear():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))
    board.set_piece(2, 2, Piece("black", "knight"))

    assert validate_move(board, 4, 4, 2, 2) is True


def test_rejects_bishop_move_onto_own_piece():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "bishop"))
    board.set_piece(2, 2, Piece("white", "knight"))

    assert validate_move(board, 4, 4, 2, 2) is False


def test_generates_bishop_pseudo_legal_moves_until_board_edge():
    board = board_with_kings()
    board.set_piece(4, 4, Piece("white", "bishop"))

    moves = generate_bishop_pseudo_legal_moves(board, 4, 4)

    assert moves == [
        (3, 3),
        (2, 2),
        (1, 1),
        (0, 0),
        (3, 5),
        (2, 6),
        (1, 7),
        (5, 3),
        (6, 2),
        (7, 1),
        (5, 5),
        (6, 6),
        (7, 7),
    ]


def test_generates_bishop_pseudo_legal_moves_stop_at_first_blocker():
    board = board_with_kings()
    board.set_piece(4, 4, Piece("white", "bishop"))
    board.set_piece(2, 2, Piece("black", "pawn"))
    board.set_piece(6, 6, Piece("white", "pawn"))

    moves = generate_bishop_pseudo_legal_moves(board, 4, 4)

    assert moves == [
        (3, 3),
        (2, 2),
        (3, 5),
        (2, 6),
        (1, 7),
        (5, 3),
        (6, 2),
        (7, 1),
        (5, 5),
        (6, 6),
    ]
