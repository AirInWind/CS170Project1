import heapq
import copy

class SearchNode:
    def __init__(self, state, parent, cost, heuristic):
        self.parent = parent
        self.state = state
        self.g = cost               # g(n) = cost from start to current node
        self.h = heuristic          # h(n) = heuristic estimate from current node to goal
        self.f = cost + heuristic   # f(n) = g(n) + h(n)

# find blank index
def find_blank_index(puzzle):
    return puzzle.index(0)

# generate valid neighbors
def get_neighbors(puzzle):
    blank_index = find_blank_index(puzzle)
    blank_row, blank_col = divmod(blank_index, 3) # 3x3 puzzle assumption
    # check which row,col blank is in and generate neighbors accordingly
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dr, dc in directions:
        new_row = blank_row + dr
        new_col = blank_col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            swap_index = new_row * 3 + new_col
            new_puzzle = puzzle.copy()
            new_puzzle[blank_index], new_puzzle[swap_index] = new_puzzle[swap_index], new_puzzle[blank_index]
            neighbors.append(new_puzzle)
    
    return neighbors

# check if goal state
def is_goal_state(puzzle):
    return puzzle == [1, 2, 3, 4, 5, 6, 7, 8, 0]

def uniform_cost_search(puzzle):
    return 0

def heuristic_misplaced_tiles(puzzle):
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    misplaced_count = 0
    
    for i in range(len(puzzle)):
        if puzzle[i] != 0 and puzzle[i] != goal[i]: # don't count the blank tile
            misplaced_count += 1
            
    return misplaced_count

def heuristic_manhattan_distance(puzzle):
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    total_distance = 0
    
    for i in range(len(puzzle)):
        if puzzle[i] != 0: # skip the blank tile
            current_value = puzzle[i]
            goal_index = goal.index(current_value)
            
            # calculate row and column for current and goal positions in a 3x3 grid
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = divmod(goal_index, 3)
            
            # calculate Manhattan distance and add to total: row difference + column difference
            total_distance += abs(current_row - goal_row) + abs(current_col - goal_col)
            
    return total_distance

def general_search(puzzle, heuristic_fn):
    start_h = heuristic_fn(puzzle)
    start_node = SearchNode(state=puzzle, parent=None, cost=0, heuristic=start_h)
    queue = []
    tie_breaker = 0
    heapq.heappush(queue, (start_node.f, tie_breaker, start_node))
    best_g = {tuple(puzzle): 0} # track best g(n) for each state
    nodes_expanded = 0
    max_queue_size = 1
    max_depth_expanded = -1
    max_depth_states = []
    
    while queue:
        _, _, current_node = heapq.heappop(queue)
        if is_goal_state(current_node.state):
            print(f"Nodes expanded: {nodes_expanded}, Max queue size: {max_queue_size}")
            return current_node
        nodes_expanded += 1
        
        for neighbor in get_neighbors(current_node.state):
            t = tuple(neighbor)
            new_g = current_node.g + 1
            if t not in best_g or new_g < best_g[t]:
                h = heuristic_fn(neighbor)
                best_g[t] = new_g
                child_node = SearchNode(state=neighbor, parent=current_node, cost=new_g, heuristic=h)
                tie_breaker += 1
                heapq.heappush(queue, (child_node.f, tie_breaker, child_node))
            
            if len(queue) > max_queue_size:
                max_queue_size = len(queue)
    
    print("No solution found.")
    return None

def run_ucs(puzzle):
    print("\n=== Running Uniform Cost Search (h=0) ===")
    goal_node = general_search(puzzle, uniform_cost_search)
    if goal_node:
        print_solution_path(goal_node)
        
    return goal_node

def run_a_star_misplaced(puzzle):
    print("\n=== Running A* Search with Misplaced Tile Heuristic ===")
    goal_node = general_search(puzzle, heuristic_misplaced_tiles)
    if goal_node:
        print_solution_path(goal_node)
        
    return goal_node

def run_a_star_manhattan(puzzle):
    print("\n=== Running A* Search with Manhattan Distance Heuristic ===")
    goal_node = general_search(puzzle, heuristic_manhattan_distance)
    if goal_node:
        print_solution_path(goal_node)
        
    return goal_node

def print_puzzle(puzzle):
    print("\n+---+---+---+")
    for i in range(3):
        row = puzzle[i*3:(i+1)*3]
        print("|", end="")
        for tile in row:
            if tile == 0:
                print("   |", end="")
            else:
                print(f" {tile} |", end="")
        print("\n+---+---+---+")

# prints out the solution path from start to goal by following parent pointers
def print_solution_path(node):
    path = []
    while node is not None:
        path.append(node.state)
        node = node.parent
        
    print(f"\nSolution depth: {len(path) - 1}\n")
    for state in path:
        print_puzzle(state)
    return list(reversed(path))

def main():
    # Predefined puzzles
    puzzles = { #Minecraft inspired difficulty levels
        1: ("Peaceful", [1, 2, 3, 4, 5, 6, 7, 8, 0]),
        2: ("Easy", [1, 2, 3, 4, 5, 6, 0, 7, 8]),
        3: ("Normal", [1, 3, 6, 5, 0, 2, 4, 7, 8]),
        4: ("Hardcore", [1, 6, 7, 5, 0, 3, 4, 8, 2]),
        5: ("Extreme", [0, 7, 2, 4, 6, 1, 3, 5, 8]),
    }
    
    print("Welcome to the 8-Puzzle Solver!")
    
    while True:
        print("\n=== Main Menu ===")
        print("1. Use a predefined puzzle")
        print("2. Enter your own puzzle")
        print("3. Exit")
        
        menu_choice = input("\nEnter your choice (1-3): ").strip()
        
        if menu_choice == "1":
            # Show predefined puzzles
            print("\n=== Predefined Puzzles ===")
            for key, (name, puzzle) in puzzles.items():
                print(f"{key}. {name}: {puzzle}") # display puzzle options
            print("0. Go back to menu")
            
            puzzle_choice = input("\nSelect a puzzle (0-5): ").strip()
            
            if puzzle_choice == "0":
                continue
            
            if puzzle_choice not in ['1', '2', '3', '4', '5']:
                print("Invalid choice.")
                continue
            
            puzzle = puzzles[int(puzzle_choice)][1]
            puzzle_name = puzzles[int(puzzle_choice)][0]
            print(f"\nSelected: {puzzle_name}")
            print(f"puzzle: {puzzle}")
            run_a_star_manhattan(puzzle)
            run_a_star_misplaced(puzzle)
            run_ucs(puzzle)
            
        elif menu_choice == "2":
            print("\nWork in progress: Custom puzzle input not implemented yet.")
            
        elif menu_choice == "3":
            print("\nThank you for using 8-Puzzle Solver. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue
        
        # Run algorithms on the selected puzzle
        
    
if __name__ == "__main__":
    main()