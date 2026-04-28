"""Command-line interface for move validation and perft."""

import argparse
from chess_validator.board import Board
from chess_validator.perft import perft as calculate_perft
from chess_validator.utilities import square_to_coords
from chess_validator.validator import validate_move as is_valid_move

MENU_PROMPT = (
    "\nChoose an option:\n"
    "  1. Play moves from a position\n"
    "  2. Run perft\n"
    "  q. Quit\n"
    "> "
)

MOVE_HELP = (
    "Enter moves in long algebraic notation (e.g. e2e4, g1f3, e1g1).\n"
    "For promotions append the piece letter: e7e8q, e7e8n, etc.\n"
    "Commands: 'help' shows this message, 'q' returns to the menu."
)

STARTING_POSITION_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

PROMOTION_MAP = {
    "q": "queen",
    "r": "rook",
    "b": "bishop",
    "n": "knight",
}


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
        return run_validate_command(args)

    if args.command == "perft":
        return run_perft_command(args)

    return cli_interactive()


def run_validate_command(args) -> int:
    """One-shot move validation from CLI arguments."""

    board = Board()
    fen = STARTING_POSITION_FEN if args.fen == "startpos" else args.fen

    try:
        board.load_fen(fen)
    except ValueError as exc:
        print(f"Invalid FEN: {exc}")
        return 1

    try:
        start_row, start_col, end_row, end_col, promotion_type = parse_move(args.move)
    except ValueError as exc:
        print(f"Invalid move: {exc}")
        return 1

    is_legal = is_valid_move(
        board, start_row, start_col, end_row, end_col, promotion_type
    )
    print(is_legal)
    return 0


def run_perft_command(args) -> int:
    """One-shot perft from CLI arguments."""

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


def cli_interactive() -> int:
    """Run the interactive CLI if no arguments are given."""

    while True:
        choice = input(MENU_PROMPT).strip().lower()

        if choice == "1":
            play_moves_cli()
        elif choice == "2":
            run_perft_cli()
        elif choice == "q":
            print("Goodbye.")
            return 0
        else:
            print("Enter 1, 2, or q.")


def play_moves_cli() -> None:
    """Load a position and play moves through it, validating each one."""

    board = Board()
    fen = input("Enter FEN (leave blank for the starting position): ").strip()

    if not fen:
        fen = STARTING_POSITION_FEN

    try:
        board.load_fen(fen)
    except ValueError as exc:
        print(f"Invalid FEN: {exc}")
        return

    print(MOVE_HELP)
    board.print_board()

    while True:
        move_input = input("Move> ").strip().lower()

        if not move_input:
            continue

        if move_input == "q":
            return

        if move_input == "help":
            print(MOVE_HELP)
            continue

        try:
            start_row, start_col, end_row, end_col, promotion_type = parse_move(
                move_input
            )
        except ValueError as exc:
            print(f"Invalid input: {exc}")
            continue

        is_legal = is_valid_move(
            board, start_row, start_col, end_row, end_col, promotion_type
        )

        if not is_legal:
            print("Illegal move.")
            continue

        board.move_piece(start_row, start_col, end_row, end_col, promotion_type)
        board.print_board()


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


def parse_move(move: str) -> tuple[int, int, int, int, str | None]:
    """Parse a move string into board coordinates and promotion."""

    move = move.strip().lower()

    if len(move) not in (4, 5):
        raise ValueError("move must be in the form e2e4 or e7e8q")

    start_row, start_col = square_to_coords(move[:2])
    end_row, end_col = square_to_coords(move[2:4])

    promotion_type: str | None = None
    if len(move) == 5:
        promotion_type = PROMOTION_MAP.get(move[4])
        if promotion_type is None:
            raise ValueError("promotion piece must be q, r, b, or n")

    return start_row, start_col, end_row, end_col, promotion_type


if __name__ == "__main__":
    main()
