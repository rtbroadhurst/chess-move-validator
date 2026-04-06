"""Contains piece specific rules for the pawn"""

from ..utilities import get_move_offset


def generate_pawn_pseudo_legal_moves(board, start_row, start_col):
    """Return pawn move targets that match the piece's movement geometry."""

    piece = board.get_piece(start_row, start_col)
    if piece is None or piece.kind != "pawn":
        return []

    direction, _ = _get_pawn_direction_and_starting_row(piece)
    return [
        (start_row + direction, start_col),
        (start_row + (2 * direction), start_col),
        (start_row + direction, start_col - 1),
        (start_row + direction, start_col + 1),
    ]


def is_valid_pawn_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if the pawn move is valid."""
    
    piece = board.get_piece(start_row, start_col)
    if piece is None or piece.kind != "pawn":
        return False

    if (end_row, end_col) not in generate_pawn_pseudo_legal_moves(board, start_row, start_col):
        return False

    delta_row, delta_col = get_move_offset(start_row, start_col, end_row, end_col)
    
    # Determine movement direction and starting row based on colour
    direction, starting_row = _get_pawn_direction_and_starting_row(piece)

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
    if is_valid_pawn_attack(board, start_row, start_col, end_row, end_col):
        
        # Must capture opposing piece
        target_piece = board.get_piece(end_row, end_col)
        
        # Don't need to check colour for en passant since it is a always the opposite
        if target_piece is None and not is_valid_en_passant(board, start_row, start_col, end_row, end_col):
            return False
        
        if target_piece and target_piece.colour == piece.colour:
            return False
        
        return True
    
    return False


def is_valid_pawn_attack(board, start_row, start_col, target_row, target_col) -> bool:
    """Return True if valid pawn attack"""
    
    piece = board.get_piece(start_row, start_col)
    if piece is None or piece.kind != "pawn":
        return False
    
    delta_row, delta_col = get_move_offset(start_row, start_col, target_row, target_col)
    direction, _ = _get_pawn_direction_and_starting_row(piece)

    return delta_row == direction and abs(delta_col) == 1


def is_valid_en_passant(board, start_row, start_col, target_row, target_col):
    """Return True if the pawn move is a legal en passant capture."""

    piece = board.get_piece(start_row, start_col)
    if piece is None or piece.kind != "pawn":
        return False

    if board.en_passant_target != (target_row, target_col):
        return False

    if not board.is_empty(target_row, target_col):
        return False

    captured_piece = board.get_piece(start_row, target_col)
    if captured_piece is None or captured_piece.kind != "pawn":
        return False

    return captured_piece.colour != piece.colour


def _get_pawn_direction_and_starting_row(piece) -> tuple[int, int]:
    """Return the forward direction and starting rank for a pawn."""

    if piece.colour == "white":
        return -1, 6

    return 1, 1
