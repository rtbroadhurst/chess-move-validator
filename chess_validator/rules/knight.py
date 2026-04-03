"""Contains piece specific rules for the knight"""

from ..utilities import get_move_offset


def is_valid_knight_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if the knight move is valid."""

    
    KNIGHT_MOVES = {(2, 1), (1, 2)}
    
    delta_row, delta_col = get_move_offset(start_row, start_col, end_row, end_col)

    # Move must be in L shape
    if (abs(delta_row), abs(delta_col)) not in KNIGHT_MOVES:
        return False

    return True