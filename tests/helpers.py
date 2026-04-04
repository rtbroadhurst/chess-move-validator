from chess_validator.board import Board
from chess_validator.pieces import Piece


def board_with_kings() -> Board:
    """Return a board containing both kings on safe default squares."""

    board = Board()

    if board.get_piece(7, 7) is None:
        board.set_piece(7, 7, Piece("white", "king"))

    if board.get_piece(0, 7) is None:
        board.set_piece(0, 7, Piece("black", "king"))

    return board
