"""Contains logic for determining whether squares are attacked."""


from .movement_rules import (
    is_valid_pawn_attack,
    is_valid_rook_move,
    is_valid_bishop_move,
    is_valid_knight_move,
    is_valid_queen_move,
    is_valid_king_move,
  )


def is_square_attacked(board, target_row, target_col, by_colour) -> bool:
    """Return True if the target square is attacked by the given colour."""

    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)

            if piece is None or piece.colour != by_colour:
                continue

            if piece_attacks_square(board, row, col, target_row, target_col):
                return True

    return False


def piece_attacks_square(board, start_row, start_col, target_row, target_col) -> bool:
    """Return True if the piece on the start square attacks the target square."""
    
    if not board.is_in_bounds(target_row, target_col):
        return False
    
    if start_row == target_row and start_col == target_col:
        return False
    
    piece = board.get_piece(start_row, start_col)

    if piece is None:
        return False

    # Other than for pawn, movement_rules logic is reused 
    match piece.kind:
        case "pawn":
            return is_valid_pawn_attack(board, start_row, start_col, target_row, target_col)
        case "rook":
            return is_valid_rook_move(board, start_row, start_col, target_row, target_col)
        case "knight":
            return is_valid_knight_move(board, start_row, start_col, target_row, target_col)
        case "bishop":
            return is_valid_bishop_move(board, start_row, start_col, target_row, target_col)
        case "queen":
            return is_valid_queen_move(board, start_row, start_col, target_row, target_col)
        case "king":
            return is_valid_king_move(board, start_row, start_col, target_row, target_col)
        case _:
            return False
        

