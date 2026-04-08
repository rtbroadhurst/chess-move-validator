from chess_validator.validator import validate_move
from chess_validator.pieces import Piece
from .helpers import board_with_kings


def test_allows_king_move_one_square_up():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 3, 4) is True


def test_allows_king_move_one_square_down():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 5, 4) is True


def test_allows_king_move_one_square_left():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 4, 3) is True


def test_allows_king_move_one_square_right():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 4, 5) is True


def test_allows_king_move_one_square_diagonally():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 3, 3) is True


def test_rejects_king_move_two_squares_vertically():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 2, 4) is False


def test_rejects_king_move_two_squares_horizontally():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 4, 6) is False


def test_allows_kingside_castle_when_rights_path_and_safety_are_clear():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 7, None)
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(7, 7, Piece("white", "rook"))

    assert validate_move(board, 7, 4, 7, 6) is True


def test_rejects_castle_when_path_square_is_attacked():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 7, None)
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(7, 7, Piece("white", "rook"))
    board.set_piece(0, 5, Piece("black", "rook"))

    assert validate_move(board, 7, 4, 7, 6) is False


def test_rejects_castle_when_rights_are_missing():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 7, None)
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(7, 7, Piece("white", "rook"))
    board.castling_rights["white_kingside"] = False

    assert validate_move(board, 7, 4, 7, 6) is False


def test_rejects_king_move_two_squares_diagonally():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))

    assert validate_move(board, 4, 4, 2, 2) is False


def test_allows_king_capture():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))
    board.set_piece(3, 3, Piece("black", "bishop"))

    assert validate_move(board, 4, 4, 3, 3) is True


def test_rejects_king_move_onto_own_piece():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "king"))
    board.set_piece(3, 3, Piece("white", "bishop"))

    assert validate_move(board, 4, 4, 3, 3) is False
