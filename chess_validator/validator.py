from .rules.pawn import is_valid_pawn_move
from .rules.rook import is_valid_rook_move
from .rules.bishop import is_valid_bishop_move
from .rules.knight import is_valid_knight_move


"""Contains logic for validating moves"""

def validate_move(board, start_row, start_col, end_row, end_col):
    """Return True if a move is valid, False if not"""
    
    if not basic_checks(board, start_row, start_col, end_row, end_col):
        return False

    # Get piece type
    piece_type = (board.get_piece(start_row, start_col)).kind

    # Match piece type to ruleset
    match piece_type:
        case "pawn":
            return is_valid_pawn_move(board, start_row, start_col, end_row, end_col)
        case "rook":
            return is_valid_rook_move(board, start_row, start_col, end_row, end_col)
        case "knight":
            return is_valid_knight_move(board, start_row, start_col, end_row, end_col)
        case "bishop":
            return is_valid_bishop_move(board, start_row, start_col, end_row, end_col)
        case "queen":
            pass
        case "king":
            pass
        case _:
            return False


def basic_checks(board, start_row, start_col, end_row, end_col):
    """
    Complete basic intital checks
    Return False if any have failed
    Otherwise, returns True
    """
    
    # Check starting and destination squares are on the board
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
    
