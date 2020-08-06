import numpy as np
import copy as cp
from collections import namedtuple
from numpy.random import default_rng

Node = namedtuple("Node", "state hn gn fn actions row col parent")

#Counts the number of inversion in a puzzle.
#Starts at the back and moves forward.
#Returns true if the puzzle is invertible and false otherwise.
def inversion_count(puzzle):
    inverse_count = 0

    for i in range(8, 0, -1):
        for j in range(0, i):
            if puzzle[i] != 0:
                if puzzle[i] < puzzle[j]:
                    inverse_count += 1

    if inverse_count % 2 == 0:
        return True
    else:
        return False

#Counts the number of tiles not in the goal position.
def misplaced_tiles(puzzle):
    tile_count = 0
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle[i][j] != goal[i][j]:
                tile_count += 1

    return tile_count

#Calculates manhattan distance from where a tile currently is to where its goal position is.
def manhattan_dist_dif(puzzle):
    tot_dist = 0
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle[i][j] != goal[i][j]:
                if puzzle[i][j] == 0:
                    dist = abs(i - 0) + abs(j - 0)
                    tot_dist += dist
                elif puzzle[i][j] == 1:
                    dist = abs(i - 0) + abs(j - 1)
                    tot_dist += dist
                elif puzzle[i][j] == 2:
                    dist = abs(i - 0) + abs(j - 2)
                    tot_dist += dist
                elif puzzle[i][j] == 3:
                    dist = abs(i - 1) + abs(j - 0)
                    tot_dist += dist
                elif puzzle[i][j] == 4:
                    dist = abs(i - 1) + abs(j - 1)
                    tot_dist += dist
                elif puzzle[i][j] == 5:
                    dist = abs(i - 1) + abs(j - 2)
                    tot_dist += dist
                elif puzzle[i][j] == 6:
                    dist = abs(i - 2) + abs(j - 0)
                    tot_dist += dist
                elif puzzle[i][j] == 7:
                    dist = abs(i - 2) + abs(j - 1)
                    tot_dist += dist
                else:
                    dist = abs(i - 2) + abs(j - 2)
                    tot_dist += dist
    return tot_dist


def heuristics_3_helper(curr_row, curr_col, expected_row, expected_col):

    if curr_row != expected_row and curr_col != expected_col:
        return 2
    elif curr_row != expected_row or curr_col != expected_col:
        return 1
    return 0

#Made up heuristic, that is very similar to the manhattan distance.
#If the tile is not in the same row or column as its goal position then it will take at least 2 moves to get there
#If it is in one but not the other then at least one step will need to be taken.
#Otherwise it is in the correct spot.
def heuristics_3(puzzle):
    min_moves = 0
    for i in range (0, 3):
        for j in range (0, 3):
            if puzzle[i][j] != 0:
                if puzzle[i][j] == 1:
                    min_moves += heuristics_3_helper(i, j, 0, 1)
                elif puzzle[i][j] == 2:
                    min_moves += heuristics_3_helper(i, j, 0, 2)
                elif puzzle[i][j] == 3:
                    min_moves += heuristics_3_helper(i, j, 1, 0)
                elif puzzle[i][j] == 4:
                    min_moves += heuristics_3_helper(i, j, 1, 1)
                elif puzzle[i][j] == 5:
                    min_moves += heuristics_3_helper(i, j, 1, 2)
                elif puzzle[i][j] == 6:
                    min_moves += heuristics_3_helper(i, j, 2, 0)
                elif puzzle[i][j] == 7:
                    min_moves += heuristics_3_helper(i, j, 2, 1)
                else:
                    min_moves += heuristics_3_helper(i, j, 2, 2)
    return min_moves

#Returns the actions a puzzle can take and the row/col position of the blank
def available_actions(puzzle):
    row = -1
    col = -1
    actions = []

    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle[i][j] == 0:
                row = i
                col = j

    if row == 0:
        actions.append("down")

    elif row == 1:
        actions.append("up")
        actions.append("down")

    else:
        actions.append("up")

    if col == 0:
        actions.append("right")

    elif col == 1:
        actions.append("left")
        actions.append("right")

    else:
        actions.append("left")

    return actions, row, col

#Executes a given action for the given puzzle.
#Returns the new puzzle after the action has been performed.
def execute_action(action, row, col, puzzle):
    new_puzzle = cp.deepcopy(puzzle)
    if action == "up":
        temp = new_puzzle[row - 1][col]
        new_puzzle[row - 1][col] = 0
        new_puzzle[row][col] = temp

    elif action == "down":
        temp = new_puzzle[row + 1][col]
        new_puzzle[row + 1][col] = 0
        new_puzzle[row][col] = temp

    elif action == "left":
        temp = new_puzzle[row][col - 1]
        new_puzzle[row][col - 1] = 0
        new_puzzle[row][col] = temp

    else:
        temp = new_puzzle[row][col + 1]
        new_puzzle[row][col + 1] = 0
        new_puzzle[row][col] = temp

    return new_puzzle


#Checks if two given puzzles are the same
def same_puzzles(puzzle1, puzzle2):
    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle1[i][j] != puzzle2[i][j]:
                return False
    return True

#Checks if a given puzzle state has already been visited.
def been_visited(visited, puzzle):
    for i in range(0, visited.__len__()):
        if same_puzzles(visited[i],puzzle):
            return True
    return False

#Generates all of the nodes possible for a given puzzle state.
#For each action the puzzle can leggaly perform a new puzzle state is generated.
#If the state hasn't been visited then the node for the puzzle state is gcreated and added to the frontier.
#The new frontier is then sorted and returned.
def generate_nodes(parent, puzzle, frontier, visited, actions, row, col, alg, heuristic):
    for an_action in actions:
        new_puzz = execute_action(an_action,row,col,puzzle)
        if not been_visited(visited, new_puzz):

            if heuristic == 1:
                hn = misplaced_tiles(new_puzz)
            elif heuristic == 2:
                hn = manhattan_dist_dif(new_puzz)
            else:
                hn = heuristics_3(new_puzz)

            gn = parent.gn + 1
            fn = gn + hn
            new_actions, new_row, new_col = available_actions(new_puzz)
            new_node = Node(state=new_puzz, hn=hn, gn=gn, fn=fn, actions=new_actions, row=new_row, col=new_col, parent=parent)
            frontier.append(new_node)
    if alg == "greedy":
        #sorted by h(n) for greedy search
        frontier = sorted(frontier, key = lambda x:x[1])
    else:
        #sorted by f(n) for astar search
        frontier = sorted(frontier, key = lambda x:x[3])

    return frontier

#Checks if the puzzle has reached its goal state
def puzzle_finished(puzzle):
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle[i][j] != goal[i][j]:
                return False
    return True

#Best First/ Greedy Search algorithm
#Takes in a root puzzle state and desired heuristic function to evaluate by.
#Generates nodes based on the current puzzle state
#Pulls the node with the lowest h(n) from the frontier
#Adds the pulled node's state to the list of visted states.
#Has a cap of 5000 steps before the algorithm will give up looking for a solution.
def greedy_search(root, heuristic):
    greedy_frontier = []
    visited = []
    steps = 0
    greedy_frontier.append(root)
    next_node = greedy_frontier.pop(0)
    visited.append(root.state)
    while not puzzle_finished(next_node.state) and steps < 5000:
        greedy_frontier = generate_nodes(next_node, next_node.state, greedy_frontier, visited, next_node.actions, next_node.row, next_node.col, "greedy", heuristic)
        next_node = greedy_frontier.pop(0)
        visited.append(next_node.state)
        steps += 1
    return next_node, steps

#A* Search algorithm
#Takes in a root puzzle state and desired heuristic function to evaluate by.
#Generates nodes based on the current puzzle state
#Pulls the node with the lowest f(n) from the frontier
#Adds the pulled node's state to the list of visted states.
#Has a cap of 5000 steps before the algorithm will give up looking for a solution.
def astar_search(root, heuristic):
    astar_frontier = []
    visited = []
    steps = 0
    astar_frontier.append(root)
    next_node = astar_frontier.pop(0)
    visited.append(root.state)

    while not puzzle_finished(next_node.state) and steps < 5000:
        astar_frontier = generate_nodes(next_node, next_node.state, astar_frontier, visited, next_node.actions, next_node.row, next_node.col, "astar", heuristic)
        next_node = astar_frontier.pop(0)
        visited.append(next_node.state)
        steps += 1
    return next_node, steps


def puzzle_converter(puzzle):
    puzz_state = []
    for i in range(0,3):
        for j in range (0,3):
            if puzzle[i][j] == 0:
                puzz_state.append('b')
            else:
                puzz_state.append(puzzle[i][j])
    return puzz_state


def display_path(final_node):
    path = []
    curr_node = final_node
    puzz_state = puzzle_converter(curr_node.state)
    path.append(puzz_state)
    while curr_node.parent is not None:
        curr_node = curr_node.parent
        puzz_state = puzzle_converter(curr_node.state)
        path.append(puzz_state)

    path.reverse()

    for item in path:
        print(item, "->", end=" ")


#Generate puzzles until 5 invertible puzzles,
#have been solved by both search algorithms
#for all three heuristics
puzzles_tried = 0
while puzzles_tried < 5:
    print("Puzzles Tried Count:", puzzles_tried)
    rng = default_rng()
    a_puzzle = rng.choice(9, size=9, replace=False)
    invertible = inversion_count(a_puzzle)
    a_puzzle = a_puzzle.reshape(3, 3)
    hn_man = manhattan_dist_dif(a_puzzle)
    hn_tiles = misplaced_tiles(a_puzzle)
    hn_3 = heuristics_3(a_puzzle)
    first_actions, a_row, a_col = available_actions(a_puzzle)
    print("Puzzle to solve:\n", a_puzzle, "\n")

    if invertible:
        puzzles_tried += 1

        root_tiles = Node(state=a_puzzle, hn=hn_tiles, gn=0, fn=hn_tiles, actions=first_actions, row = a_row, col= a_col, parent = None)
        root_man = Node(state=a_puzzle, hn=hn_man, gn=0, fn=hn_man, actions=first_actions, row = a_row, col= a_col, parent = None)
        root_hn3 = Node(state=a_puzzle, hn=hn_3, gn=0, fn=hn_3, actions=first_actions, row = a_row, col= a_col, parent = None)

        greedy_tiles, greedy_tile_tries = greedy_search(root_tiles, 1)
        greedy_man, greedy_man_tries    = greedy_search(root_man, 2)
        greedy_hn3, greedy_hn3_tries    = greedy_search(root_hn3, 3)
        astar_tiles, astar_tile_tries   = astar_search(root_tiles, 1)
        astar_man, astar_man_tries      = astar_search(root_man, 2)
        astar_hn3, astar_hn3_tries      = astar_search(root_hn3, 3)

        print("Number of greedy misplaced tiles tries:", greedy_tile_tries)
        display_path(greedy_tiles)
        print()

        print("Number of greedy manhattan tries:", greedy_man_tries)
        display_path(greedy_man)
        print()

        print("Number of greedy hn3 tries:", greedy_hn3_tries)
        display_path(greedy_tiles)
        print()

        print("Number of astar misplaced tiles tries:", astar_tile_tries)
        display_path(astar_tiles)
        print()

        print("Number of astar manhattan tries:", astar_man_tries)
        display_path(astar_man)
        print()

        print("Number of astar hn3 tries:", astar_hn3_tries)
        display_path(astar_hn3)
        print()







