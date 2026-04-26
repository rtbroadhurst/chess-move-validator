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


def generate_knight_pseudo_legal_moves(board, start_row, start_col):
    """Return knight move targets that match the piece's movement geometry."""

    return [
        (start_row + 2, start_col + 1),
        (start_row + 2, start_col - 1),
        (start_row + 1, start_col + 2),
        (start_row + 1, start_col - 2),
        (start_row - 1, start_col + 2),
        (start_row - 1, start_col - 2),
        (start_row - 2, start_col + 1),
        (start_row - 2, start_col - 1),
    ]
