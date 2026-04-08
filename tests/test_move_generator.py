from chess_validator.board import Board
from chess_validator.move_generator import generate_legal_moves, generate_pseudo_legal_moves
from chess_validator.pieces import Piece
from .helpers import board_with_kings


def test_generate_pseudo_legal_moves_only_uses_side_to_move():
    board = Board()
    board.turn = "white"
    board.set_piece(4, 4, Piece("white", "knight"))
    board.set_piece(2, 2, Piece("black", "rook"))

    moves = generate_pseudo_legal_moves(board)

    assert set(moves) == {
        (4, 4, 2, 3, None),
        (4, 4, 2, 5, None),
        (4, 4, 3, 2, None),
        (4, 4, 3, 6, None),
        (4, 4, 5, 2, None),
        (4, 4, 5, 6, None),
        (4, 4, 6, 3, None),
        (4, 4, 6, 5, None),
    }


def test_generate_pseudo_legal_moves_expands_each_promotion_target():
    board = Board()
    board.turn = "white"
    board.set_piece(1, 4, Piece("white", "pawn"))
    board.set_piece(0, 5, Piece("black", "rook"))

    moves = generate_pseudo_legal_moves(board)

    assert {
        (1, 4, 0, 4, "queen"),
        (1, 4, 0, 4, "rook"),
        (1, 4, 0, 4, "bishop"),
        (1, 4, 0, 4, "knight"),
        (1, 4, 0, 5, "queen"),
        (1, 4, 0, 5, "rook"),
        (1, 4, 0, 5, "bishop"),
        (1, 4, 0, 5, "knight"),
    }.issubset(set(moves))


def test_generate_pseudo_legal_moves_adds_castling_candidates_for_home_king():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 4, Piece("white", "king"))

    moves = generate_pseudo_legal_moves(board)

    assert (7, 4, 7, 6, None) in moves
    assert (7, 4, 7, 2, None) in moves


def test_generate_legal_moves_filters_out_move_that_exposes_own_king():
    board = Board()
    board.turn = "white"
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(0, 7, Piece("black", "king"))
    board.set_piece(7, 3, Piece("white", "rook"))
    board.set_piece(7, 0, Piece("black", "rook"))

    moves = generate_legal_moves(board)

    assert (7, 3, 6, 3, None) not in moves


def test_generate_legal_moves_includes_castling_when_it_is_legal():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(7, 7, Piece("white", "rook"))

    moves = generate_legal_moves(board)

    assert (7, 4, 7, 6, None) in moves


def test_generate_legal_moves_excludes_castling_through_attacked_square():
    board = board_with_kings()
    board.turn = "white"
    board.set_piece(7, 4, Piece("white", "king"))
    board.set_piece(7, 7, Piece("white", "rook"))
    board.set_piece(0, 5, Piece("black", "rook"))

    moves = generate_legal_moves(board)

    assert (7, 4, 7, 6, None) not in moves
