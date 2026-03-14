"""Contains code for the CLI"""

from board import Board

def main():
    board = Board()
    board.load_fen("8/8/8/8/8/8/8/8")
    board.print_board()
    board.load_fen("4k3/8/8/8/8/8/4P3/4K3")
    board.print_board()

    

if __name__ == "__main__":
    main()