# Machine Learning 8 Tile Puzzle Solver
This program is designed to generate and solve an 8 Tile Puzzle. 
To solve a puzzle all possible actions avaliable are generated and evlauated.
The next action to take is then based on which puzzle has the best huerstic score.
The evaluation of a puzzle is deteremined using a huerstic.
The two heurstics used to evaluate a puzzle are the manhattan distance from the correct spot for each tile, or counting the number of misplaced tiles.

When a puzzle is generated it is put onto the frontier. 
The frontier is a list of puzzles that have yet to be tried.
This list is sorted based on if the best first or A* search algorithm is being used.
In the case of the best search the frontier is sorted based on whichever heurstic is being used.
The A* search is similar but also keeps track of how many moves it took to get to the puzzle state.
This means the frontier is sorted based on the current huerstic used as well as amount of moves used to get there.

Once a solution to the puzzle has been solved, the solution path is printed.

# Running The Program

