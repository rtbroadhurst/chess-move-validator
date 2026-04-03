"""Contains the board class, which stores the current board state

    Board coordinate system (a8 = (0, 0)):

        a   b   c   d   e   f   g   h
    +---+---+---+---+---+---+---+---+
    8 |0,0|0,1|0,2|0,3|0,4|0,5|0,6|0,7|
    7 |1,0|1,1|1,2|1,3|1,4|1,5|1,6|1,7|
    6 |2,0|2,1|2,2|2,3|2,4|2,5|2,6|2,7|
    5 |3,0|3,1|3,2|3,3|3,4|3,5|3,6|3,7|
    4 |4,0|4,1|4,2|4,3|4,4|4,5|4,6|4,7|
    3 |5,0|5,1|5,2|5,3|5,4|5,5|5,6|5,7|
    2 |6,0|6,1|6,2|6,3|6,4|6,5|6,6|6,7|
    1 |7,0|7,1|7,2|7,3|7,4|7,5|7,6|7,7|
    +---+---+---+---+---+---+---+---+
"""


from .pieces import Piece
from .validator import validate_move

class Board:
    """Stores the board grid, active turn, and en passant target square."""

    def __init__(self) -> None:
        """Initialise an empty 8x8 board with White to move."""
        self.grid: list[list[Piece | None]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.turn = "white"
        self.en_passant_target: str | None = None


    def is_in_bounds(self, row: int, col: int) -> bool:
        """Return True if the given coordinates are on the board."""
        
        return 0 <= row < 8 and 0 <= col < 8


    def get_piece(self, row: int, col: int) -> Piece | None:
        """Return the piece at the given coordinates."""
        
        if not self.is_in_bounds(row, col):
            raise ValueError("Position is out of bounds.")
        
        return self.grid[row][col]


    def set_piece(self, row: int, col: int, piece: Piece | None) -> None:
        """Place a piece on the given coordinates."""
        
        if not self.is_in_bounds(row, col):
            raise ValueError("Position is out of bounds.")
        self.grid[row][col] = piece


    def is_empty(self, row: int, col: int) -> bool:
        """Return True if the square is empty."""
        
        return self.get_piece(row, col) is None
    
    
    def find_king(self, colour: str) -> tuple[int, int]:
        """
        Return the king's coordinates as (row, column) for the given colour.
        
        Raise value error if no king of that colour exists
        """ 
        
                     
        for column in range(0, 8):
            for row in range(0, 8):
                piece = self.get_piece(row, column)
                if piece != None and piece.kind == "king" and piece.colour == colour:
                    return row, column
                
        raise ValueError(f"No {colour} king found on the board.")


    def move_piece(self, start_row: int, start_col: int, end_row: int, end_col: int):
        """
        Move a piece on the board
        
        Return True if successful, otherwise False
        """
        
        if not validate_move(self, start_row, start_col, end_row, end_col):
            return False
        
        piece = self.get_piece(start_row, start_col)
        self.set_piece(start_row, start_col, None)
        self.set_piece(end_row, end_col, piece)
        
        self.turn = "black" if self.turn == "white" else "white"
        
        return True
            
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
                    colour = "white" if char.isupper() else "black"
                    row.append(Piece(colour, kinds[char.lower()]))

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
