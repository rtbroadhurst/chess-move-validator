"""
Perft validation against the standard test positions.

Reference values: https://www.chessprogramming.org/Perft_Results

Depths are inentionally kept shallow enough to run quickly enough for repeated use.
"""

import pytest

from chess_validator.board import Board
from chess_validator.perft import perft

POSITIONS = {
    "startpos": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "kiwipete": "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "position3": "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
    "position4": "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
    "position5": "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
    "position6": "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
}

PERFT_CASES = [
    ("startpos", 1, 20),
    ("startpos", 2, 400),
    ("startpos", 3, 8_902),
    ("kiwipete", 1, 48),
    ("kiwipete", 2, 2_039),
    ("kiwipete", 3, 97_862),
    ("position3", 1, 14),
    ("position3", 2, 191),
    ("position3", 3, 2_812),
    ("position4", 1, 6),
    ("position4", 2, 264),
    ("position4", 3, 9_467),
    ("position5", 1, 44),
    ("position5", 2, 1_486),
    ("position5", 3, 62_379),
    ("position6", 1, 46),
    ("position6", 2, 2_079),
    ("position6", 3, 89_890),
]


@pytest.mark.parametrize(
    "position_name,depth,expected",
    PERFT_CASES,
    ids=[f"{name}-d{depth}" for name, depth, _ in PERFT_CASES],
)
def test_perft(position_name: str, depth: int, expected: int) -> None:
    board = Board()
    board.load_fen(POSITIONS[position_name])
    assert perft(board, depth) == expected
