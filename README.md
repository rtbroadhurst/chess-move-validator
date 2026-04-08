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
