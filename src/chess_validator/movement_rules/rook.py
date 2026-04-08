"""Contains piece specific rules for the rook"""

from ..utilities import get_move_offset


def is_valid_rook_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if the rook move is valid."""
    
    
    delta_row, delta_col = get_move_offset(start_row, start_col, end_row, end_col)
    
    # Move must end in the same row or same column
    if delta_row and delta_col:
        return False
    
    # Move must not be blocked by an intermediate square
    if delta_row > 0:
        step_row = 1
    elif delta_row < 0:
        step_row = -1
    else:
        step_row = 0
        
    if delta_col > 0:
        step_col = 1
    elif delta_col < 0:
        step_col = -1
    else:
        step_col = 0
      
    current_row = start_row + step_row
    current_col = start_col + step_col

    while current_row != end_row or current_col != end_col:
        if not board.is_empty(current_row, current_col):
            return False
        current_row += step_row
        current_col += step_col

    return True


def generate_rook_pseudo_legal_moves(board, start_row, start_col):
    """Return rook move targets that match the piece's movement geometry."""

    moves = []

    for step_row, step_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        current_row = start_row + step_row
        current_col = start_col + step_col

        while board.is_in_bounds(current_row, current_col):
            moves.append((current_row, current_col))

            if not board.is_empty(current_row, current_col):
                break

            current_row += step_row
            current_col += step_col

    return moves
