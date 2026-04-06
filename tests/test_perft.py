from chess_validator.board import Board
from chess_validator.perft import perft


def test_perft_starting_position_depth_1():
    board = Board()
    board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    assert perft(board, 1) == 20


def test_perft_starting_position_depth_2():
    board = Board()
    board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    assert perft(board, 2) == 400


def test_perft_kiwipete_depth_1():
    board = Board()
    board.load_fen("r3k2r/p1ppqpb1/bn2pnp1/2pPn3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")

    assert perft(board, 1) == 48


def test_perft_kiwipete_depth_2():
    board = Board()
    board.load_fen("r3k2r/p1ppqpb1/bn2pnp1/2pPn3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")

    assert perft(board, 2) == 2039
