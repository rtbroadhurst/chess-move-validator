"""Contains piece specific rules for the bishop"""

from ..utilities import get_delta


def is_valid_bishop_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if valid bishop move, otherwise False"""

    # Get move deltas
    delta_row, delta_col = get_delta(start_row, start_col, end_row, end_col)

    # Move must be diagonal 
    if not abs(delta_row) == abs(delta_col):
        return False
    
    # Move must not be obstructed 
    if delta_row > 0:
        step_row = 1
    elif delta_row < 0:
        step_row = -1

    if delta_col > 0:
        step_col = 1
    elif delta_col < 0:#
        step_col = -1

    current_row = start_row + step_row
    current_col = start_col + step_col

    while current_row != end_row:
        if not board.is_empty(current_row, current_col):
            return False
        
        current_row += step_row
        current_col += step_col


    return True