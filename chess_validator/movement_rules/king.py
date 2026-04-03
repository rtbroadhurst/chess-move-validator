"""Contains piece specific rules for the king"""

from ..utilities import get_move_offset


def is_valid_king_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if the king move is valid."""    
    
    
    # Get delta values for movement
    delta_row, delta_col = get_move_offset(start_row, start_col, end_row, end_col)
    
    # Can move by one square in each direction
    if abs(delta_row) > 1 or abs(delta_col) > 1:
        return False    
    
    return True