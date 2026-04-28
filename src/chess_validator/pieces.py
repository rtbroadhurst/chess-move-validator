"""Stores the code for the piece classes"""


class Piece:
    """Superclass for all pieces."""

    def __init__(self, colour: str, kind: str) -> None:
        self.colour = colour
        self.kind = kind

    def fen_symbol(self) -> str:
        """Return the FEN symbol for this piece."""

        symbols = {
            "pawn": "p",
            "rook": "r",
            "knight": "n",
            "bishop": "b",
            "queen": "q",
            "king": "k",
        }

        symbol = symbols[self.kind]

        if self.colour == "white":
            return symbol.upper()

        return symbol

    def display_symbol(self) -> str:
        """Return the Unicode character for this piece, used for board rendering."""

        symbols = {
            "white": {
                "pawn": "♙",
                "rook": "♖",
                "knight": "♘",
                "bishop": "♗",
                "queen": "♕",
                "king": "♔",
            },
            "black": {
                "pawn": "♟",
                "rook": "♜",
                "knight": "♞",
                "bishop": "♝",
                "queen": "♛",
                "king": "♚",
            },
        }

        return symbols[self.colour][self.kind]
