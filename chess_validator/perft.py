"""Contains code for perft testing."""

from .board import Board
from .move_generator import generate_legal_moves


def perft(board: Board, depth: int) -> int:
    """Return peft number"""

    if depth < 0:
        raise ValueError("Depth must be non-negative.")

    if depth == 0:
        return 1

    nodes = 0

    for start_row, start_col, end_row, end_col, promotion_type in generate_legal_moves(board):
        next_board = board.copy()
        next_board.move_piece(start_row, start_col, end_row, end_col, promotion_type)
        nodes += perft(next_board, depth - 1)

    return nodes


def perft_divide(board: Board, depth: int) -> dict[tuple[int, int, int, int, str | None], int]:
    """Return the per move node counts for all legal moves at the root."""

    if depth < 0:
        raise ValueError("Depth cannot be negative.")

    if depth == 0:
        return {}

    counts = {}

    for move in generate_legal_moves(board):
        start_row, start_col, end_row, end_col, promotion_type = move
        next_board = board.copy()
        next_board.move_piece(start_row, start_col, end_row, end_col, promotion_type)
        counts[move] = perft(next_board, depth - 1)

    return counts
