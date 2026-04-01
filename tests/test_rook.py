from chess_validator.validator import validate_move
from chess_validator.board import Board
from chess_validator.pieces import Piece

def test_allows_rook_vertical_move_on_clear_file():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))

    assert validate_move(board, 7, 0, 4, 0) is True


def test_allows_rook_horizontal_move_on_clear_rank():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))

    assert validate_move(board, 7, 0, 7, 5) is True


def test_rejects_rook_diagonal_move():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))

    assert validate_move(board, 7, 0, 5, 2) is False


def test_rejects_rook_vertical_move_when_blocked():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))
    board.set_piece(5, 0, Piece("black", "pawn"))

    assert validate_move(board, 7, 0, 4, 0) is False


def test_rejects_rook_horizontal_move_when_blocked():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))
    board.set_piece(7, 3, Piece("black", "pawn"))

    assert validate_move(board, 7, 0, 7, 5) is False


def test_allows_rook_capture_when_path_is_clear():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))
    board.set_piece(4, 0, Piece("black", "knight"))

    assert validate_move(board, 7, 0, 4, 0) is True


def test_rejects_rook_move_onto_own_piece():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 0, Piece("white", "rook"))
    board.set_piece(4, 0, Piece("white", "knight"))

    assert validate_move(board, 7, 0, 4, 0) is False
