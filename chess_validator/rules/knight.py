"""Contains piece specific rules for the bishop"""

from ..utilities import get_delta


def is_valid_bishop_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if valid bishop move, otherwise False"""
