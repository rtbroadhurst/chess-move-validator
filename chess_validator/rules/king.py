"""Contains piece specific rules for the king"""

from ..utilities import get_delta


def is_valid_king_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if valid king move, otherwise False"""
    
    # Get delta values for movement
    delta_row, delta_col = get_delta(start_row, start_col, end_row, end_col)
    
    # Can move by one square in each direction
    if not abs(delta_col) <= 1 or not abs(delta_row) <= 1:
        return False 
    
    return True