
# Hive Board Game AI Documentation

This document outlines how I implemented Hive in Python and the methods I used to develop my AI.

TODO: Fill in details. This is currently an outline.

## Implementing Hive

### Keeping Track of the Board

- Coordinate system
- Stored in dictionary
- HexSpaces, EmptySpaces, Pieces
- All stored in HiveGameBoard
- BoardManager (maybe bring this up in AI?)

### Queen Bees
- Moves to any legal move surrounding it.
  - Talk about how legal moves are calculated

### Ants
- By default, can move to any open empty space
- If a group of empty spaces become enclosed, those spaces are marked and Ants cannot move there unless they have a direct connection into the group

### Grasshoppers
- Traverse the board in directions of any connected Pieces
- If an EmptySpace is found, it is added as a possible move
- If a Piece on the path is removed, the path beyond the Piece is removed as well. This also removes a possible move from the Grasshopper, but adds a new one where the Piece used to be.
- If a Piece is placed on an EmptySpace that a Grasshopper can move to, the path continues to traverse in the direction of the Grasshopper's movement until it reaches an EmptySpace. This EmptySpace becomes a new possible move for the Grasshopper. The space where the Piece was placed is not longer a possible move for the Grasshopper.

### Spiders
- Traverse EmptySpaces in the direction of all possible moves.
- Once a distance of three spaces is reached, a possible move is added.
- If an update occurs on a path, it is updated accordingly to match the new set of possible moves.

### Beetles
- Same as Queen Bee movement, but they also can move to surrounding Pieces
- Specific rules for moving on/off of Pieces.
- The Beetle is not limited by the "One Hive" rule while it is on top of Pieces.


## Implementing the AI
