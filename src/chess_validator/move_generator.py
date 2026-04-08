"""Contains code to generate all legal moves from a board position"""

from .board import Board
from .movement_rules import (
    generate_bishop_pseudo_legal_moves,
    generate_king_pseudo_legal_moves,
    generate_knight_pseudo_legal_moves,
    generate_pawn_pseudo_legal_moves,
    generate_queen_pseudo_legal_moves,
    generate_rook_pseudo_legal_moves,
)
from .validator import validate_move


def generate_legal_moves(board: Board) -> list[tuple[int, int, int, int, str | None]]:
    """Generate all legal moves from a board position"""

    legal_moves = []

    for start_row, start_col, end_row, end_col, promotion_type in generate_pseudo_legal_moves(board):
        if validate_move(board, start_row, start_col, end_row, end_col, promotion_type):
            legal_moves.append((start_row, start_col, end_row, end_col, promotion_type))

    return legal_moves


def generate_pseudo_legal_moves(board: Board) -> list[tuple[int, int, int, int, str | None]]:
    """Generate pseudo legal moves based on movement geometry to be processed by generate_legal_moves"""

    moves = []

    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is None or piece.colour != board.turn:
                continue

            match piece.kind:
                case "pawn":
                    target_squares = generate_pawn_pseudo_legal_moves(board, row, col)
                    for end_row, end_col in target_squares:
                        if end_row in (0, 7):
                            for promotion_type in ("queen", "rook", "bishop", "knight"):
                                moves.append((row, col, end_row, end_col, promotion_type))
                        else:
                            moves.append((row, col, end_row, end_col, None))
                            
                case "knight":
                    target_squares = generate_knight_pseudo_legal_moves(board, row, col)
                    for end_row, end_col in target_squares:
                        moves.append((row, col, end_row, end_col, None))
                        
                case "bishop":
                    target_squares = generate_bishop_pseudo_legal_moves(board, row, col)
                    for end_row, end_col in target_squares:
                        moves.append((row, col, end_row, end_col, None))
                        
                case "rook":
                    target_squares = generate_rook_pseudo_legal_moves(board, row, col)
                    for end_row, end_col in target_squares:
                        moves.append((row, col, end_row, end_col, None))
                        
                case "queen":
                    target_squares = generate_queen_pseudo_legal_moves(board, row, col)
                    for end_row, end_col in target_squares:
                        moves.append((row, col, end_row, end_col, None))
                        
                case "king":
                    target_squares = generate_king_pseudo_legal_moves(board, row, col)
                    for end_row, end_col in target_squares:
                        moves.append((row, col, end_row, end_col, None))

                    home_row = 7 if piece.colour == "white" else 0
                    if row == home_row and col == 4:
                        moves.append((row, col, home_row, 6, None))
                        moves.append((row, col, home_row, 2, None))

    return moves
