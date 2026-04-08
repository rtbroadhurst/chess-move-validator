# Chess Move Validator

A Python project for validating legal chess moves, supporting the full ruleset and using perft testing to verify correctness.

## Features

- Legal move validation for all pieces
- King safety checking
- Special rules: castling, en passant, and promotion
- FEN parsing
- Perft testing and pytest based validation

## Project Structure

- `board.py` - Board state representation and manipulation
- `validator.py` - Move validation orchestrator 
- `movement_rules/` - Piece specific movement logic
- `attacks.py` - Square attack detection used for check and castling validation
- `king_safety.py` - Checks whether a king is in check after a move
- `move_generator.py` - Generates pseudo-legal and fully legal moves from a board state
- `perft.py` - Implements perft for validation
- `pieces.py` - Minimal piece class and FEN symbol conversion
- `utilities.py` - Shared helper functions such as coordinate to square conversion
- `cli.py` - Command line entry point for move validation and perft testing
- `tests/` - Unit tests covering board state, validation, movement rules, attack logic, move generation, perft, utilities, and CLI

## Validation Flow

Move validation is orchestrated in `validator.py` as a pipeline:

1. **Basic Checks**
   - Ensure coordinates are in bounds
   - Ensure the source square contains a piece
   - Ensure the piece belongs to the current player
   - Prevent capturing your own pieces
   - Ensure the start square and end square are different

2. **Piece-Specific Rules**
   - Dispatch to the correct movement rule based on piece type
   - Implemented in the `movement_rules/` module
   - Handles movement geometry and path blocking

3. **Promotion Validation**
   - Detect whether a pawn reaches the final rank
   - Require a valid promotion type: `queen`, `rook`, `bishop`, or `knight`

4. **King Safety Check**
   - Apply the move on a copied board state
   - Evaluate whether the current player's king is left in check
   - Reject moves that result in an illegal position

A move that passes every stage is considered fully legal.

## Perft Results

Perft is used to verify the correctness of move generation by counting the number of legal positions reachable at a given depth.

Reference results are taken from:
[Chess Programming Wiki – Perft Results](https://www.chessprogramming.org/Perft_Results)

### Starting Position

**FEN:** `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`

| Depth | Expected Nodes | Actual Nodes | Match |
|------|---------------|-------------|-------|
| 1    | 20            | 20          | **Yes** |
| 2    | 400           | 400         | **Yes** |
| 3    | 8,902         | 8,902       | **Yes** |
| 4    | 197,281       | 197,281     | **Yes** |
| 5    | 4,865,609     | 4,865,609   | **Yes** |

### Position 2 (Kiwipete)

**FEN:** `r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1`

| Depth | Expected Nodes | Actual Nodes | Match |
|------|---------------|-------------|-------|
| 1    | 48            | 48          | **Yes** |
| 2    | 2,039         | 2,039       | **Yes** |
| 3    | 97,862        | 97,862      | **Yes** |
| 4    | 4,085,603     | 4,085,603   | **Yes** |

### Notes

- All results match expected values up to the listed depths
- Confirms correct handling of chess rules

### Position 5

**FEN:** `rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8`

| Depth | Expected Nodes | Actual Nodes | Match |
|------|---------------|-------------|-------|
| 1    | 44            | 44          | **Yes** |
| 2    | 1,486         | 1,486       | **Yes** |
| 3    | 62,379        | 62,379      | **Yes** |
| 4    | 2,103,487     | 2,103,487   | **Yes** |
| 5    | 89,941,194    | 89,941,194  | **Yes** |


## Performance

I prioritised clarity and correctness when writing this program.

In particular, king safety validation and the perft implementation use board copying rather than a make/unmake approach. This reduces the chance of errors, but has a significant impact on performance. This tradeoff was made to prioritise correctness and simplicity during initial development.

If I were to continue developing the project, improving this would be the main focus.

## Testing

The project includes unit tests written with `pytest` to verify board state handling, movement rules, attack detection, move generation, and perft results.
