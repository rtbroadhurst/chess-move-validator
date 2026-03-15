"""Contains the board class, which stores the current board state."""

from .pieces import Piece

class Board:
    """Stores the board grid, active turn, and en passant target square."""

    def __init__(self) -> None:
        """Initialise an empty 8x8 board with White to move."""
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.turn = "white"
        self.en_passant_target = None


    def is_in_bounds(self, row: int, col: int) -> bool:
        """Return True if the given coordinates are on the board."""
        
        return 0 <= row < 8 and 0 <= col < 8


    def get_piece(self, row: int, col: int):
        """Return the piece at the given coordinates."""
        
        if not self.is_in_bounds(row, col):
            raise ValueError("Position is out of bounds.")
        return self.grid[row][col]


    def set_piece(self, row: int, col: int, piece) -> None:
        """Place a piece on the given coordinates."""
        
        if not self.is_in_bounds(row, col):
            raise ValueError("Position is out of bounds.")
        self.grid[row][col] = piece


    def is_empty(self, row: int, col: int) -> bool:
        """Return True if the square is empty."""
        
        return self.get_piece(row, col) is None


    def load_fen(self, fen: str) -> None:
        """
        Load a board position from FEN (Forsyth-Edwards Notation)

        Currently, only supports piece placement
        """
        
        # Splits the entire FEN code and takes the first section
        piece_placement = fen.split()[0]
        
        # Separates each rank
        ranks = piece_placement.split("/")

        if len(ranks) != 8:
            raise ValueError("FEN piece placement must contain 8 ranks.")

        kinds = {
            "p": "pawn",
            "r": "rook",
            "n": "knight",
            "b": "bishop",
            "q": "queen",
            "k": "king",
        }

        new_grid = []

        for rank in ranks:
            row = []

            for char in rank:
                if char.isdigit():
                    row.extend([None] * int(char))
                else:
                    color = "white" if char.isupper() else "black"
                    row.append(Piece(color, kinds[char.lower()]))

            if len(row) != 8:
                raise ValueError("Each FEN rank must contain 8 squares.")

            new_grid.append(row)

        self.grid = new_grid


    def print_board(self) -> None:
        """Print the current board layout."""
        
        print()
        for row in self.grid:
            for square in row:
                if square is None:
                    print(".", end=" ")
                else:
                    print(square.fen_symbol(), end=" ")
            print()
