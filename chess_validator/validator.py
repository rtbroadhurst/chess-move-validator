"""Contains logic for validating moves"""


from .movement_rules import (
      is_valid_pawn_move,
      is_valid_rook_move,
      is_valid_bishop_move,
      is_valid_knight_move,
      is_valid_queen_move,
      is_valid_king_move,
  )

from .king_safety import is_in_check


def validate_move(board, start_row, start_col, end_row, end_col):
    """Return True if a move is valid, False if not"""
    
    
    if not basic_checks(board, start_row, start_col, end_row, end_col):
        return False

    if not piece_rules(board, start_row, start_col, end_row, end_col):
        return False
    
    if king_in_check(board, start_row, start_col, end_row, end_col):
        return False
    
    return True
    
    
def basic_checks(board, start_row, start_col, end_row, end_col):
    """Return True if the move passes shared checks before piece specific validation."""    
    
    
    # Check that the source and destination squares are on the board
    if not board.is_in_bounds(start_row, start_col) or not board.is_in_bounds(end_row, end_col):
        return False
    
    # Check source square is not empty
    if board.is_empty(start_row, start_col):
        return False
    
    # Check source and destination are not the same square 
    if start_row == end_row and start_col == end_col:
        return False
    
    # Check piece belongs to the side whose turn it is
    moving_piece = board.get_piece(start_row, start_col)
    if moving_piece.colour != board.turn:
        return False
    
    # Check destination not occupied by own colour
    destination_piece = board.get_piece(end_row, end_col)
    if destination_piece is not None and destination_piece.colour == moving_piece.colour:
        return False

    return True
    

def piece_rules(board, start_row, start_col, end_row, end_col):
    """
    Match the type of piece to its specific rules

    Return True if it follows them, otherwise False
    """
    moving_piece = board.get_piece(start_row, start_col)

    match moving_piece.kind:
        case "pawn":
            return is_valid_pawn_move(board, start_row, start_col, end_row, end_col)
        case "rook":
            return is_valid_rook_move(board, start_row, start_col, end_row, end_col)
        case "knight":
            return is_valid_knight_move(board, start_row, start_col, end_row, end_col)
        case "bishop":
            return is_valid_bishop_move(board, start_row, start_col, end_row, end_col)
        case "queen":
            return is_valid_queen_move(board, start_row, start_col, end_row, end_col)
        case "king":
            return is_valid_king_move(board, start_row, start_col, end_row, end_col)
        case _:
            return False


def king_in_check(board, start_row, start_col, end_row, end_col) -> bool:
    """Returns True if king is in check afer the move"""
    
    board_copy = board.copy()
    
    board_copy._apply_move_unchecked(start_row, start_col, end_row, end_col)
    
    if is_in_check(board_copy, board_copy.turn):
        return True
    
    return False

    