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
