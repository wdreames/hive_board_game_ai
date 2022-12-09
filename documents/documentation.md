
# Hive Board Game AI Documentation

William Reames

This document gives an overview regarding how I implemented Hive within Python and explains how I implemented my AI.

## Implementing Hive

### Keeping Track of the Board

The first challenge I came across was determining a way to implement the hexagon-based game board within Python. The solution I ended up implementing was to give each hexagon a coordinate, and store it as if it were on a regular 2D plane. 

This image shows how each hexagon can be given a specific coordinate on a plane:

![image of hexagon board](../images/hexagon_grid.png)

This image shows how each Piece would be stored within my Python implementation. In this case, the Piece would be located at (0, 0), and the displayed coordinates surrounding it would be the six sides of that piece:

![image of piece coordinate representation](../images/piece_coordinate.png)

Furthermore, I also implemented both Pieces and EmptySpaces. The EmptySpaces were extremely important in simplifying my implementation. EmptySpaces allowed me to more easily understand where players could place new Pieces along with knowing where Pieces could be moved.

As for storing this information, I stored each space object into a dictionary that related the coordinate of the space to the object at that location. This was also separated into two dictionaries: one for Pieces, and one for EmptySpaces. This allowed easy access to a space object if its location is already known. For example, each space contains sets of the surrounding Pieces and surrounding EmptySpaces. This way each space has easy access to all of its surrounding locations. This diagram helps display the class structure used to implement the game:

![Class UML Diagram](../images/hive_class_diagram.png)

### Performing Actions on the Game Board

There are two different actions a player can perform on a given turn: placing pieces or moving pieces. To implement this, each Piece was given two important functions: `set_location_to(new_location)` and `remove()`. In order to place a Piece, a new Piece object would be created, then its `set_location_to(new_location)` function would be called. Moreover, if a player would like to move a piece, the Piece would call its `remove()` function, followed by its `set_location_to(new_location)` function. 

To determine where a player could place new Pieces, each EmptySpace on the board would keep track of the number of connected white Pieces and the number of connected black Pieces. Therefore, if an EmptySpace was only connected to white Pieces, white could place a new Piece there. On the other hand, if an EmptySpace was only connected to black pieces, black could place a new Piece there.

As for determining where Pieces could be moved, each Piece had its own `calc_possible_moves()` function, which could be called to updated its set of possible moves listed within the HiveGameBoard. This function was implemented within each of the Piece subclasses.

### Universal Movement Rules

There are two movement rules within Hive that apply to all Pieces on the board: freedom of movement and the "one hive" rule. 

#### Freedom of Movement

The freedom of movement rule states that pieces must slide on the board rather than be picked up off of it (although this does not apply to Grasshoppers or Beetles since they jump on or hop over Pieces). The following images help demonstrate this rule:

![Freedom of Movement Example 1](../images/freedom_of_mvt1.png)

![Freedom of Movement Example 2](../images/freedom_of_mvt2.png)

To implement this, I kept track of certain "sliding rules". Whenever a Piece was set to a new location (whether by being placed as a new piece or by moving to that location), it would check if other Pieces exist in certain locations. If it found a Piece at any of these locations, the spaces in between the two Pieces would be marked as unable to slide to each other. Then, if either of these Pieces are removed later in the game, the two spaces between them are updated so that they are marked as being able to slide to each other again. The sequence of images below help show how this works. Note, though, that these images are meant to demonstrate this rule specifically, and do not display all the Pieces or EmptySpaces that would usually be found on a game board:

![Sliding Rule Example Slide 1](../images/sliding_rule_ex1.png)
1: A subset of a board state containing two Pieces and one EmptySpace

![Sliding Rule Example Slide 2](../images/sliding_rule_ex2.png)
2: A new Piece is placed

![Sliding Rule Example Slide 3](../images/sliding_rule_ex3.png)
3: The new Piece finds another Piece in one of the specified locations

![Sliding Rule Example Slide 4](../images/sliding_rule_ex4.png)
4: The two spaces between those Pieces are marked as not being able to slide to each other

![Sliding Rule Example Slide 5](../images/sliding_rule_ex5.png)
5: A Piece that was preventing sliding between two pieces was removed

![Sliding Rule Example Slide 6](../images/sliding_rule_ex6.png)
6: The two spaces between those Pieces are marked as being able to slide to each other again

#### The "One Hive" Rule

The "one hive" rule states that all Pieces must be connected to each other at all times. For example, in the below image, the black Ant is unable to move, since doing so would split the hive into two separate groups:

![One Hive Rule Example 1](../images/one_hive_rule.png)

To implement this, each Piece contained a `can_move` boolean value. If this rule would prevent a Piece from moving, this value was set to False. Otherwise, the `can_move` value would be set to True.

There were two methods that I used to determine whether a Piece could move. For starters, if a Piece (a) was placed with only one connection to another Piece (b), the connected Piece (b) would be locked based on this rule. This is because the connected Piece (b) is the only connection the new Piece (a) has to the rest of the Hive. However, the inverse of this rule is not true. For example, the black Piece in the image below is only connected to one Piece. If the black piece were removed, the Piece it was connected to would still need to be locked based on the "one hive" rule.

![One Hive Rule Example 2](images/one_hive_rule2.png)

Beyond the one simplification of locking Pieces if a new piece is placed with one connected Piece, the rest of the "one hive" rule was implemented through the use of a graph algorithm. In this case, I treated every Piece as a node in a graph with the connections on each side of the Piece being edges. Then, I searched for articulation points, or any points that would disconnect the graph if they were removed through the use of Tarjan's algorithm. After determining which Pieces were articulation points, I set each Piece's `can_move` value accordingly. More information about Tarjan's algorithm can be found [here](https://www.geeksforgeeks.org/tarjan-algorithm-find-strongly-connected-components/).

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


## Conclusion
- lessons learned
- description of work completed

## Acknowledgments
- Charles
- printing hex board: https://inventwithpython.com/bigbookpython/project35.html
- Tarjan's algorithm: https://www.geeksforgeeks.org/tarjan-algorithm-find-strongly-connected-components/
