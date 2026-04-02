"""Contains piece specific rules for the queen"""

from .rook import is_valid_rook_move
from .bishop import is_valid_bishop_move

def is_valid_queen_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if valid queen move, otherwise False"""

    # Since the queen combines rook and bishop movement we can do the movement checking by reusing their functions.
    return (
          is_valid_rook_move(board, start_row, start_col, end_row, end_col) 
          or is_valid_bishop_move(board, start_row, start_col, end_row, end_col)
      )