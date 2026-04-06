"""Contains piece specific rules for the queen"""

from .bishop import generate_bishop_pseudo_legal_moves
from .rook import is_valid_rook_move
from .bishop import is_valid_bishop_move
from .rook import generate_rook_pseudo_legal_moves

def is_valid_queen_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if the queen move is valid."""


    # Since the queen combines rook and bishop movement we can do the movement checking by reusing their functions.
    return (
          is_valid_rook_move(board, start_row, start_col, end_row, end_col) 
          or is_valid_bishop_move(board, start_row, start_col, end_row, end_col)
      )


def generate_queen_pseudo_legal_moves(board, start_row, start_col):
    """Return queen move targets that match the piece's movement geometry."""

    return (
        generate_rook_pseudo_legal_moves(board, start_row, start_col)
        + generate_bishop_pseudo_legal_moves(board, start_row, start_col)
    )
