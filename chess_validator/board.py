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
from .utilities import get_move_offset

class Board:
    """Stores the board grid, active turn, and en passant target square."""

    def __init__(self) -> None:
        """Initialise an empty 8x8 board with White to move."""
        
        self.grid: list[list[Piece | None]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        
        self.turn = "white"
        self.en_passant_target: tuple[int, int] | None = None

        self.castling_rights = {
            "white_kingside": True,
            "white_queenside": True,
            "black_kingside": True,
            "black_queenside": True,
        }


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


    def move_piece(self, start_row: int, start_col: int, end_row: int, end_col: int, promotion_type: str | None = None) -> bool:
        """
        Move a piece on the board and update turn state
        
        Return True if successful, otherwise False
        """
        
        if not validate_move(self, start_row, start_col, end_row, end_col, promotion_type):
            return False
        
        captured_piece = self.get_piece(end_row, end_col)
        self._apply_move_unchecked(start_row, start_col, end_row, end_col)
        self.update_castling_rights(start_row, start_col, end_row, end_col, captured_piece)
        self.update_en_passant_target(start_row, start_col, end_row, end_col)
        self.update_pawn_promotion(start_row, start_col, end_row, end_col, promotion_type)
        
        self.turn = "black" if self.turn == "white" else "white"        
        
        return True


    def _apply_move_unchecked(self, start_row: int, start_col: int, end_row: int, end_col: int) -> None:
        """Move a piece without validating legality or updating turn state."""

        piece = self.get_piece(start_row, start_col)

        if (
            piece is not None
            and piece.kind == "pawn"
            and start_col != end_col
            and self.is_empty(end_row, end_col)
            and self.en_passant_target == (end_row, end_col)
        ):
            self.set_piece(start_row, end_col, None)

        self.set_piece(start_row, start_col, None)
        self.set_piece(end_row, end_col, piece)

        if piece is not None and piece.kind == "king" and start_row == end_row and abs(end_col - start_col) == 2:
            self._move_castling_rook(end_row, end_col)


    def _move_castling_rook(self, row: int, king_end_col: int) -> None:
        """Move the rook to its castled square after the king has moved."""

        if king_end_col == 6:
            rook_start_col, rook_end_col = 7, 5
        elif king_end_col == 2:
            rook_start_col, rook_end_col = 0, 3
        else:
            return

        rook = self.get_piece(row, rook_start_col)
        self.set_piece(row, rook_start_col, None)
        self.set_piece(row, rook_end_col, rook)


    def update_castling_rights(self, start_row: int, start_col: int, end_row: int, end_col: int, captured_piece: Piece | None) -> None:
        """Update castling rights based on a move"""
        
        piece = self.get_piece(end_row, end_col)
        colour = piece.colour
        
        if piece.kind == "king":
            self.castling_rights[colour + "_kingside"] = False
            self.castling_rights[colour + "_queenside"] = False
        
        elif piece.kind == "rook":
            if colour == "white" and start_row == 7 and start_col == 7:
                self.castling_rights[colour + "_kingside"] = False
            elif colour == "white" and start_row == 7 and start_col == 0:
                self.castling_rights[colour + "_queenside"] = False
            elif colour == "black" and start_row == 0 and start_col == 7:
                self.castling_rights[colour + "_kingside"] = False
            elif colour == "black" and start_row == 0 and start_col == 0:
                self.castling_rights[colour + "_queenside"] = False

        if captured_piece is None or captured_piece.kind != "rook":
            return

        if captured_piece.colour == "white" and end_row == 7 and end_col == 7:
            self.castling_rights["white_kingside"] = False
        elif captured_piece.colour == "white" and end_row == 7 and end_col == 0:
            self.castling_rights["white_queenside"] = False
        elif captured_piece.colour == "black" and end_row == 0 and end_col == 7:
            self.castling_rights["black_kingside"] = False
        elif captured_piece.colour == "black" and end_row == 0 and end_col == 0:
            self.castling_rights["black_queenside"] = False


    def update_en_passant_target(self, start_row: int, start_col: int, end_row: int, end_col: int) -> None:
        """Update en passant target based on a move"""

        self.en_passant_target = None

        piece = self.get_piece(end_row, end_col)
        if piece is None or piece.kind != "pawn":
            return

        d_row, d_col = get_move_offset(start_row, start_col, end_row, end_col)
        if abs(d_row) == 2 and d_col == 0:
            self.en_passant_target = (start_row + (d_row // 2), start_col)


    def update_pawn_promotion(self, start_row: int, start_col: int, end_row: int, end_col: int, promotion_type: str) -> None:
        """Promote a pawn that has reached the back rank"""
        
        piece = self.get_piece(end_row, end_col)
        
        if piece is not None and piece.kind  == "pawn" and end_row in (0, 7):
            self.set_piece(end_row, end_col, Piece(piece.colour, promotion_type))
        
        
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


    def copy(self) -> "Board":
        """Return a copy of the board"""
        
        new_board = Board()
        new_board.turn = self.turn
        new_board.en_passant_target = self.en_passant_target
        new_board.castling_rights = self.castling_rights.copy()
        new_board.grid = [row[:] for row in self.grid]
        return new_board
