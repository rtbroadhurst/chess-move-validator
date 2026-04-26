import pytest

import chess_validator.board as board_module
from chess_validator.board import Board
from chess_validator.pieces import Piece


def test_board_starts_with_expected_defaults():
    board = Board()

    assert len(board.grid) == 8
    assert all(len(row) == 8 for row in board.grid)
    assert all(square is None for row in board.grid for square in row)
    assert board.turn == "white"
    assert board.en_passant_target is None
    assert board.half_move_clock == 0
    assert board.full_move_number == 1


def test_is_in_bounds():
    board = Board()

    assert board.is_in_bounds(0, 0) is True
    assert board.is_in_bounds(7, 7) is True
    assert board.is_in_bounds(4, 2) is True
    assert board.is_in_bounds(-1, 0) is False
    assert board.is_in_bounds(0, -1) is False
    assert board.is_in_bounds(8, 0) is False
    assert board.is_in_bounds(0, 8) is False


def test_get_piece_returns_none_for_empty_square():
    board = Board()

    assert board.get_piece(3, 3) is None


def test_get_piece_raises_for_out_of_bounds_position():
    board = Board()

    with pytest.raises(ValueError):
        board.get_piece(8, 0)


def test_set_piece_stores_piece_on_board():
    board = Board()
    knight = Piece("white", "knight")

    board.set_piece(2, 5, knight)

    assert board.get_piece(2, 5) is knight


def test_set_piece_can_clear_a_square():
    board = Board()
    board.set_piece(2, 5, "N")

    board.set_piece(2, 5, None)

    assert board.get_piece(2, 5) is None


def test_set_piece_raises_for_out_of_bounds_position():
    board = Board()

    with pytest.raises(ValueError):
        board.set_piece(-1, 0, Piece("white", "king"))


def test_is_empty_reports_square_state():
    board = Board()

    assert board.is_empty(1, 1) is True
    board.set_piece(1, 1, Piece("white", "pawn"))
    assert board.is_empty(1, 1) is False


def test_find_king_returns_coordinates_for_matching_colour():
    board = Board()
    board.set_piece(0, 4, Piece("black", "king"))
    board.set_piece(7, 4, Piece("white", "king"))

    assert board.find_king("white") == (7, 4)
    assert board.find_king("black") == (0, 4)


def test_move_piece_returns_false_and_leaves_board_unchanged_for_invalid_move(
    monkeypatch,
):
    board = Board()
    pawn = Piece("white", "pawn")
    board.set_piece(6, 4, pawn)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: False)

    moved = board.move_piece(6, 4, 5, 4)

    assert moved is False
    assert board.get_piece(6, 4) is pawn
    assert board.get_piece(5, 4) is None
    assert board.turn == "white"


def test_move_piece_moves_piece_and_switches_turn_for_valid_move(monkeypatch):
    board = Board()
    pawn = Piece("white", "pawn")
    board.set_piece(6, 4, pawn)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    moved = board.move_piece(6, 4, 5, 4)

    assert moved is True
    assert board.get_piece(6, 4) is None
    assert board.get_piece(5, 4) is pawn
    assert board.turn == "black"


def test_move_piece_sets_en_passant_target_after_double_pawn_move(monkeypatch):
    board = Board()
    pawn = Piece("white", "pawn")
    board.set_piece(6, 4, pawn)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    board.move_piece(6, 4, 4, 4)

    assert board.en_passant_target == (5, 4)


def test_move_piece_clears_en_passant_target_after_non_double_move(monkeypatch):
    board = Board()
    pawn = Piece("white", "pawn")
    board.set_piece(6, 4, pawn)
    board.en_passant_target = (2, 3)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    board.move_piece(6, 4, 5, 4)

    assert board.en_passant_target is None


def test_move_piece_removes_captured_pawn_for_en_passant(monkeypatch):
    board = Board()
    white_pawn = Piece("white", "pawn")
    black_pawn = Piece("black", "pawn")
    board.set_piece(3, 4, white_pawn)
    board.set_piece(3, 5, black_pawn)
    board.en_passant_target = (2, 5)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    board.move_piece(3, 4, 2, 5)

    assert board.get_piece(2, 5) is white_pawn
    assert board.get_piece(3, 5) is None


def test_move_piece_promotes_pawn_to_requested_piece(monkeypatch):
    board = Board()
    board.turn = "white"
    pawn = Piece("white", "pawn")
    board.set_piece(1, 4, pawn)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    moved = board.move_piece(1, 4, 0, 4, "queen")

    promoted_piece = board.get_piece(0, 4)

    assert moved is True
    assert promoted_piece is not None
    assert promoted_piece.colour == "white"
    assert promoted_piece.kind == "queen"


def test_move_piece_replaces_destination_piece_when_move_is_valid(monkeypatch):
    board = Board()
    rook = Piece("white", "rook")
    knight = Piece("black", "knight")
    board.set_piece(7, 0, rook)
    board.set_piece(4, 0, knight)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    moved = board.move_piece(7, 0, 4, 0)

    assert moved is True
    assert board.get_piece(7, 0) is None
    assert board.get_piece(4, 0) is rook
    assert board.castling_rights["white_queenside"] is False


def test_move_piece_updates_castling_rights_after_king_moves(monkeypatch):
    board = Board()
    king = Piece("white", "king")
    board.set_piece(7, 4, king)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    board.move_piece(7, 4, 6, 4)

    assert board.castling_rights["white_kingside"] is False
    assert board.castling_rights["white_queenside"] is False


def test_move_piece_also_moves_rook_when_castling(monkeypatch):
    board = Board()
    king = Piece("white", "king")
    rook = Piece("white", "rook")
    board.set_piece(7, 4, king)
    board.set_piece(7, 7, rook)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    moved = board.move_piece(7, 4, 7, 6)

    assert moved is True
    assert board.get_piece(7, 6) is king
    assert board.get_piece(7, 5) is rook
    assert board.get_piece(7, 7) is None


def test_move_piece_only_revokes_rook_rights_from_home_square(monkeypatch):
    board = Board()
    rook = Piece("white", "rook")
    board.set_piece(4, 7, rook)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    board.move_piece(4, 7, 4, 6)

    assert board.castling_rights["white_kingside"] is True
    assert board.castling_rights["white_queenside"] is True


def test_move_piece_revokes_castling_rights_when_home_rook_is_captured(monkeypatch):
    board = Board()
    white_rook = Piece("white", "rook")
    black_rook = Piece("black", "rook")
    board.turn = "black"
    board.set_piece(7, 7, white_rook)
    board.set_piece(0, 7, black_rook)

    monkeypatch.setattr(board_module, "validate_move", lambda *args: True)

    board.move_piece(0, 7, 7, 7)

    assert board.castling_rights["white_kingside"] is False
    assert board.castling_rights["white_queenside"] is True


def test_update_castling_rights_revokes_black_kingside_for_home_rook_move():
    board = Board()
    rook = Piece("black", "rook")
    board.set_piece(0, 7, rook)
    board._apply_move_unchecked(0, 7, 1, 7)

    board.update_castling_rights(0, 7, 1, 7, None)

    assert board.castling_rights["black_kingside"] is False
    assert board.castling_rights["black_queenside"] is True


def test_update_castling_rights_revokes_black_queenside_for_home_rook_capture():
    board = Board()
    white_bishop = Piece("white", "bishop")
    black_rook = Piece("black", "rook")
    board.set_piece(0, 0, black_rook)
    board.set_piece(1, 1, white_bishop)
    captured_piece = board.get_piece(0, 0)
    board._apply_move_unchecked(1, 1, 0, 0)

    board.update_castling_rights(1, 1, 0, 0, captured_piece)

    assert board.castling_rights["black_kingside"] is True
    assert board.castling_rights["black_queenside"] is False


def test_update_castling_rights_ignores_non_rook_capture_on_home_square():
    board = Board()
    white_bishop = Piece("white", "bishop")
    black_knight = Piece("black", "knight")
    board.set_piece(1, 1, white_bishop)
    board.set_piece(0, 7, black_knight)
    captured_piece = board.get_piece(0, 7)
    board._apply_move_unchecked(1, 1, 0, 7)

    board.update_castling_rights(1, 1, 0, 7, captured_piece)

    assert board.castling_rights["black_kingside"] is True
    assert board.castling_rights["black_queenside"] is True


def test_apply_move_unchecked_moves_piece_without_switching_turn():
    board = Board()
    rook = Piece("white", "rook")
    board.set_piece(7, 0, rook)

    board._apply_move_unchecked(7, 0, 4, 0)

    assert board.get_piece(7, 0) is None
    assert board.get_piece(4, 0) is rook
    assert board.turn == "white"


def test_copy_returns_board_with_independent_grid_lists():
    board = Board()
    rook = Piece("white", "rook")
    board.set_piece(7, 0, rook)
    board.turn = "black"
    board.en_passant_target = (5, 4)
    board.half_move_clock = 7
    board.full_move_number = 12
    board.castling_rights["white_queenside"] = False

    copied_board = board.copy()
    copied_board.set_piece(7, 0, None)
    copied_board.set_piece(4, 0, rook)
    copied_board.castling_rights["black_kingside"] = False

    assert copied_board is not board
    assert copied_board.grid is not board.grid
    assert copied_board.grid[7] is not board.grid[7]
    assert board.get_piece(7, 0) is rook
    assert board.get_piece(4, 0) is None
    assert copied_board.turn == "black"
    assert copied_board.en_passant_target == (5, 4)
    assert copied_board.half_move_clock == 7
    assert copied_board.full_move_number == 12
    assert copied_board.castling_rights["white_queenside"] is False
    assert board.castling_rights["black_kingside"] is True


def test_copy_preserves_piece_objects_in_squares():
    board = Board()
    king = Piece("white", "king")
    board.set_piece(7, 4, king)

    copied_board = board.copy()

    assert copied_board.get_piece(7, 4) is king


def test_load_fen_loads_empty_board():
    board = Board()

    board.load_fen("8/8/8/8/8/8/8/8")

    assert all(square is None for row in board.grid for square in row)


def test_load_fen_places_pieces_on_expected_squares():
    board = Board()

    board.load_fen("4k3/8/8/8/8/8/4P3/4K3")

    black_king = board.get_piece(0, 4)
    white_pawn = board.get_piece(6, 4)
    white_king = board.get_piece(7, 4)

    assert isinstance(black_king, Piece)
    assert black_king.colour == "black"
    assert black_king.kind == "king"

    assert isinstance(white_pawn, Piece)
    assert white_pawn.colour == "white"
    assert white_pawn.kind == "pawn"

    assert isinstance(white_king, Piece)
    assert white_king.colour == "white"
    assert white_king.kind == "king"

    assert board.get_piece(3, 3) is None


def test_load_fen_loads_full_state_fields():
    board = Board()

    board.load_fen("r3k2r/8/8/8/8/8/8/R3K2R b Kq e3 4 7")

    assert board.turn == "black"
    assert board.castling_rights["white_kingside"] is True
    assert board.castling_rights["white_queenside"] is False
    assert board.castling_rights["black_kingside"] is False
    assert board.castling_rights["black_queenside"] is True
    assert board.en_passant_target == (5, 4)
    assert board.half_move_clock == 4
    assert board.full_move_number == 7


def test_load_fen_raises_when_field_count_is_invalid():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("8/8/8/8/8/8/8/8 w - - 0")


def test_load_fen_raises_when_rank_count_is_invalid():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("8/8/8/8/8/8/8")


def test_load_fen_raises_when_rank_width_is_invalid():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("9/8/8/8/8/8/8/8")


def test_load_fen_raises_when_active_colour_is_invalid():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("8/8/8/8/8/8/8/8 x - - 0 1")


def test_load_fen_raises_when_castling_rights_are_invalid():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("8/8/8/8/8/8/8/8 w Kx - 0 1")


def test_load_fen_raises_when_halfmove_clock_is_negative():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("8/8/8/8/8/8/8/8 w - - -1 1")


def test_load_fen_raises_when_fullmove_number_is_less_than_one():
    board = Board()

    with pytest.raises(ValueError):
        board.load_fen("8/8/8/8/8/8/8/8 w - - 0 0")
