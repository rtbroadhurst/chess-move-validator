"""Contains piece-specific rules for the bishop."""

from ..utilities import get_move_offset


def is_valid_bishop_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if the bishop move is valid."""


    delta_row, delta_col = get_move_offset(start_row, start_col, end_row, end_col)

    # Move must be diagonal.
    if abs(delta_row) != abs(delta_col):
        return False

    # Move must not be obstructed.
    step_row = 1 if delta_row > 0 else -1
    step_col = 1 if delta_col > 0 else -1

    current_row = start_row + step_row
    current_col = start_col + step_col

    while current_row != end_row:
        if not board.is_empty(current_row, current_col):
            return False

        current_row += step_row
        current_col += step_col

    return True