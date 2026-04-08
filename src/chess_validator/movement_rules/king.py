"""Contains piece specific rules for the king"""

from ..utilities import get_move_offset


def is_valid_king_move(board, start_row, start_col, end_row, end_col) -> bool:
    """Return True if the king move is valid."""

    delta_row, delta_col = get_move_offset(start_row, start_col, end_row, end_col)

    if delta_row == 0 and abs(delta_col) == 2:
        return is_valid_castling_move(board, start_row, start_col, end_col)

    # Can move by one square in each direction
    if abs(delta_row) > 1 or abs(delta_col) > 1:
        return False

    return True


def is_valid_castling_move(board, start_row, start_col, end_col) -> bool:
    """Return True if the attempted king move is a legal castle."""

    piece = board.get_piece(start_row, start_col)
    if piece is None or piece.kind != "king":
        return False

    
    home_row = 7 if piece.colour == "white" else 0
    if start_row != home_row or start_col != 4:
        return False

    side = "kingside" if end_col == 6 else "queenside" if end_col == 2 else None
    if side is None:
        return False

    if not board.castling_rights[f"{piece.colour}_{side}"]:
        return False

    rook_col = 7 if side == "kingside" else 0
    rook = board.get_piece(home_row, rook_col)
    if rook is None or rook.kind != "rook" or rook.colour != piece.colour:
        return False

    path_cols = range(start_col + 1, rook_col) if side == "kingside" else range(rook_col + 1, start_col)
    for col in path_cols:
        if not board.is_empty(home_row, col):
            return False

    from ..attacks import is_square_attacked

    enemy_colour = "black" if piece.colour == "white" else "white"
    transit_cols = [start_col, start_col + 1] if side == "kingside" else [start_col, start_col - 1]
    transit_cols.append(end_col)

    for col in transit_cols:
        if is_square_attacked(board, home_row, col, enemy_colour):
            return False

    return True


def generate_king_pseudo_legal_moves(board, start_row, start_col):
    """Return king move targets that match the piece's movement geometry."""

    return [
        (start_row - 1, start_col - 1),
        (start_row - 1, start_col),
        (start_row - 1, start_col + 1),
        (start_row, start_col - 1),
        (start_row, start_col + 1),
        (start_row + 1, start_col),
        (start_row + 1, start_col - 1),
        (start_row + 1, start_col + 1),
    ]
