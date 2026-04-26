"""Contains logic to check if a move will put the king into check"""

from .attacks import is_square_attacked


def is_in_check(board, colour) -> bool:
    """Return True if the the king of that colour is in check"""

    king_row, king_col = board.find_king(colour)
    enemy_colour = "black" if colour == "white" else "white"
    return is_square_attacked(board, king_row, king_col, enemy_colour)
