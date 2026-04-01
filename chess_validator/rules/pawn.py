"""Contains piece specific rules for the pawn"""

from ..utilities import get_delta


def is_valid_pawn_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if valid pawn move, otherwise False"""
    
    # Get piece object
    piece = board.get_piece(start_row, start_col)
    
    # Determine change in row and column
    delta_row, delta_col = get_delta(start_row, start_col, end_row, end_col)
    
    # Determine movement direction and starting row based on colour
    if piece.colour == "white":
        direction = -1
        starting_row = 6
    else:
        direction = 1
        starting_row = 1

    # Check one square forward move
    if delta_row == direction and delta_col == 0:
        
        # Must move into empty square
        if not board.is_empty(end_row, end_col):
            return False
        
        return True

    # Check two square forward move
    if delta_row == 2 * direction and delta_col == 0:
        
        # Pawn must be on starting row
        if start_row != starting_row:
            return False
        
        # Square in front must be empty
        if not board.is_empty(start_row + direction, start_col):
            return False
        
        # Destination square must also be empty
        if not board.is_empty(end_row, end_col):
            return False
        
        return True

    # Check diagonal capture move
    if delta_row == direction and abs(delta_col) == 1:
        
        # Must capture opposing piece
        target_piece = board.get_piece(end_row, end_col)
        
        if target_piece is None:
            return False
        
        if target_piece.colour == piece.colour:
            return False
        
        return True

    return False