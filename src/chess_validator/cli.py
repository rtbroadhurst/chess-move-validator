"""Command-line interface for move validation and perft."""

import argparse
from chess_validator.board import Board
from chess_validator.perft import perft as calculate_perft
from chess_validator.utilities import square_to_coords
from chess_validator.validator import validate_move as is_valid_move

MENU_PROMPT = (
    "\nChoose an option:\n"
    "  1. Validate a move\n"
    "  2. Run perft\n"
    "  q. Quit\n"
    "> "
)

STARTING_POSITION_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def main() -> int:
    """CLI entry point."""

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    validate = subparsers.add_parser("validate")
    validate.add_argument("fen")
    validate.add_argument("move")

    perft = subparsers.add_parser("perft")
    perft.add_argument("fen")
    perft.add_argument("depth", type=int)

    args = parser.parse_args()

    if args.command == "validate":
        board = Board()
        fen = STARTING_POSITION_FEN if args.fen == "startpos" else args.fen

        try:
            board.load_fen(fen)
        except ValueError as exc:
            print(f"Invalid FEN: {exc}")
            return 1

        move = args.move.strip().lower()

        if len(move) not in (4, 5):
            print("Move must be in the form e2e4 or e7e8q.")
            return 1

        try:
            start_row, start_col = square_to_coords(move[:2])
            end_row, end_col = square_to_coords(move[2:4])
        except ValueError as exc:
            print(f"Invalid move: {exc}")
            return 1

        promotion_map = {
            "q": "queen",
            "r": "rook",
            "b": "bishop",
            "n": "knight",
        }

        promotion_type = None
        if len(move) == 5:
            promotion_type = promotion_map.get(move[4])
            if promotion_type is None:
                print("Invalid promotion piece.")
                return 1

        is_legal = is_valid_move(
            board,
            start_row,
            start_col,
            end_row,
            end_col,
            promotion_type,
        )

        print(is_legal)
        return 0

    if args.command == "perft":
        board = Board()
        fen = STARTING_POSITION_FEN if args.fen == "startpos" else args.fen

        try:
            board.load_fen(fen)
        except ValueError as exc:
            print(f"Invalid FEN: {exc}")
            return 1

        try:
            nodes = calculate_perft(board, args.depth)
        except ValueError as exc:
            print(exc)
            return 1

        print(f"Perft({args.depth}) = {nodes}")
        return 0

    return cli_interactive()


def cli_interactive():
    """Run the interactive CLI if no arguments are given"""

    while True:
        choice = input(MENU_PROMPT).strip().lower()

        if choice == "1":
            validate_move_cli()
        elif choice == "2":
            run_perft_cli()
        elif choice == "q":
            print("Goodbye.")
            return 0
        else:
            print("Enter 1, 2, or q.")


def validate_move_cli() -> bool:
    """Load a position and print whether a move is legal."""

    board = Board()
    fen = input("Enter FEN (leave blank for the starting position): ").strip()

    if not fen:
        fen = STARTING_POSITION_FEN

    try:
        board.load_fen(fen)
    except ValueError as exc:
        print(f"Invalid FEN: {exc}")
        return False

    board.print_board()

    try:
        start_row, start_col = read_square("Enter the start square (e.g. e2): ")
        end_row, end_col = read_square("Enter the destination square (e.g. e4): ")
    except ValueError as error:
        print(f"Invalid square: {error}")
        return False

    promotion_type = read_promotion_type()
    is_legal = is_valid_move(
        board,
        start_row,
        start_col,
        end_row,
        end_col,
        promotion_type,
    )

    print(is_legal)
    return is_legal


def run_perft_cli() -> int:
    """Load a FEN position and print the perft node count."""

    fen = input("Enter FEN (leave blank for the starting position): ").strip()
    if not fen:
        fen = STARTING_POSITION_FEN

    try:
        depth = int(input("Enter perft depth: ").strip())
    except ValueError:
        print("Depth must be an integer.")
        return 1

    board = Board()

    try:
        board.load_fen(fen)
    except ValueError as exc:
        print(f"Invalid FEN: {exc}")
        return 1

    try:
        nodes = calculate_perft(board, depth)
    except ValueError as exc:
        print(exc)
        return 1

    print(f"Perft({depth}) = {nodes}")
    return 0


def read_square(prompt: str) -> tuple[int, int]:
    """Read a chess square from input and convert it to board coordinates."""

    return square_to_coords(input(prompt).strip().lower())


def read_promotion_type() -> str | None:
    """Read an optional promotion piece."""

    promotion_type = input(
        "Promotion piece (queen, rook, bishop, knight, or leave blank): "
    ).strip().lower()

    return promotion_type or None


if __name__ == "__main__":
    main()