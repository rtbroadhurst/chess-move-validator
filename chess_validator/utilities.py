"""Contains utility functions"""

def square_to_coords(square: str) -> tuple[int, int]:
    """
    Converts a square in chess notation (e.g. 'e4') to 0 indexed (row, column) coordinates.
    """
    
    square_row = square[1]
    square_column = square[0]
    
    if square_column < "a" or square_column > "h":
        raise ValueError("File must be between 'a' and 'h'.")

    if square_row < "1" or square_row > "8":
        raise ValueError("Rank must be between '1' and '8'.")

    row = 8 - int(square_row)
    column = ord(square_column) - ord("a")

    return row, column


def coords_to_square(row: int, column: int) -> str:
    """
    Converts 0 indexed (row, column) coordinates to a square in chess notation (e.g. 'e4').
    """

    if not (0 <= row < 8 and 0 <= column < 8):
        raise ValueError("Row and column must be between 0 and 7.")

    
    square_column = chr(ord("a") + column)
    square_row = str(8 - row)
    return f"{square_column}{square_row}"
