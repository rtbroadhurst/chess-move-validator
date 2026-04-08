# chess-move-validator
A Python project for validating legal chess moves, includes full ruleset and perft testing to ensure correctness.

## Features
- Legal move validation for all pieces
- King safety
- Special rules: castling, en passant, promotion
- FEN parsing
- Perft testing, and pytest for validation

## Project Structure 
- 'Board' - Board state representation and manipulation
- 'Validator' - Move validation pipeline
- 'Movement Rules/' - Piece-specific movement logic
- 'Attacks' - Square attack detection used for check and castling validation
- 'King Safety' - Checks whether a king is in check after a move
- 'Move Generator' - Generates pseudo-legal and fully legal moves from a position
- 'Perft' - Implements perft for validation
- 'Pieces' - Minimal piece class and FEN symbol conversion
- 'Utilities' - Shared helper functions (e.g. coordinates to square conversions)
- 'CLI' - Command-line entry point for move validation and perft testing.
- 'Tests' - Unit tests covering board state, validation, movement rules, attack logic, move generation, perft,
  utilities, and CLI.
  
## Validation Flow

Move validation is orchestrated in `validator.py` as a pipeline:

1. **Basic Checks**
   - Ensure coordinates are in bounds
   - Ensure the source square contains a piece
   - Ensure the piece belongs to the current player
   - Prevent capturing own pieces
   - Ensure that the start square and end square are different

2. **Piece-Specific Rules**
   - Match the correct movement rule based on piece type.
   - Contained in the 'movement_rules' folder.
   - Handles piece specific rules.

3. **Promotion Validation**
   - Detect if a pawn reaches the final rank
   - Require a valid promotion type (`queen`, `rook`, `bishop`, `knight`)

4. **King Safety Check**
   - Apply the move on a copied board state (making then undoing move would be more efficient however)
   - Evaluate whether the current player's king is left in check
   - Reject moves that result in an illegal position

A move that passes each stage is considered valid.

## Perft Results

Perft is used to verify the correctness of move generation by counting the number of legal positions reachable at a given depth.

Reference results are taken from:
[Chess Programming Wiki – Perft Results](https://www.chessprogramming.org/Perft_Results)

---

### Starting Position

**FEN:** `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`

| Depth | Expected Nodes | Actual Nodes | Match |
|------|---------------|-------------|-------|
| 1    | 20            | 20          | **Yes** |
| 2    | 400           | 400         | **Yes** |
| 3    | 8,902         | 8,902       | **Yes** |
| 4    | 197,281       | 197,281     | **Yes** |
| 5    | 4,865,609     | 4,865,609   | **Yes** |

---

### Position 2 (Kiwipete)

**FEN:** `r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1`

| Depth | Expected Nodes | Actual Nodes | Match |
|------|---------------|-------------|-------|
| 1    | 48            | 48          | **Yes** |
| 2    | 2,039         | 2,039       | **Yes** |
| 3    | 97,862        | 97,862      | **Yes** |
| 4    | 4,085,603     | 4,085,603   | **Yes** |---

---

### Position 5

**FEN:** `rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8`

| Depth | Expected Nodes | Actual Nodes | Match |
|------|---------------:|-------------:|:-----:|
| 1    | 44             | 44           | **Yes** |
| 2    | 1,486          | 1,486        | **Yes** |
| 3    | 62,379         | 62,379       | **Yes** |
| 4    | 2,103,487      | 2,103,487    | **Yes** |
| 5    | 89,941,194     | 89,941,194   | **Yes** |

---
