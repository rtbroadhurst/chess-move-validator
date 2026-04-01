"""Contains piece specific rules for the knight"""

from ..utilities import get_delta


def is_valid_knight_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if valid knight move, otherwise False"""
    
    # Get move delta
    delta_row, delta_col = get_delta(start_row, start_col, end_row, end_col)

    # Move must be in L shape
    if (abs(delta_row), abs(delta_col)) not in {(2, 1), (1, 2)}:
        return False

    return True