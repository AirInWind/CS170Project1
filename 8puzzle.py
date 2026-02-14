import heapq

N = 3
goal = list(range(1, N*N)) + [0]
goal_pos = {value: idx for idx, value in enumerate(goal)}

class SearchNode:
    def __init__(self, state, parent, cost, heuristic, move='Start'):
        self.parent = parent
        self.state = state
        self.g = cost               # g(n) = cost from start to current node
        self.h = heuristic          # h(n) = heuristic estimate from current node to goal
        self.f = cost + heuristic   # f(n) = g(n) + h(n)
        self.move = move            # store the move that led to this state

# find blank index
def find_blank_index(puzzle):
    return puzzle.index(0)

# generate valid neighbors
def get_neighbors(puzzle):
    blank_index = find_blank_index(puzzle)
    blank_row, blank_col = divmod(blank_index, N) # 3x3 puzzle assumption
    # check which row,col blank is in and generate neighbors accordingly
    neighbors = []
    directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]  # Up, Down, Left, Right
    
    for dr, dc, move in directions: # calculate new row and column for the blank tile after the move
        new_row = blank_row + dr #
        new_col = blank_col + dc

        if 0 <= new_row < N and 0 <= new_col < N:
            swap_index = new_row * N + new_col
            new_puzzle = puzzle.copy()
            new_puzzle[blank_index], new_puzzle[swap_index] = new_puzzle[swap_index], new_puzzle[blank_index] # swap blank with the adjacent tile
            neighbors.append((new_puzzle, move)) # return both the new state and the move that led to it
    return neighbors

# check if goal state
def is_goal_state(puzzle, goal):
    return puzzle == goal

def uniform_cost_search(puzzle):
    return 0

def heuristic_misplaced_tiles(puzzle):
    misplaced_count = 0
    
    for i in range(N*N):
        if puzzle[i] != 0 and puzzle[i] != goal[i]: # don't count the blank tile
            misplaced_count += 1
    return misplaced_count

def heuristic_manhattan_distance(puzzle):
    total_distance = 0
    
    for i in range(N*N):
        if puzzle[i] != 0: # skip the blank tile
            current_value = puzzle[i]
            goal_index = goal_pos[current_value] # get the goal position for this tile
            
            # calculate row and column for current and goal positions in a 3x3 grid
            current_row, current_col = divmod(i, N)
            goal_row, goal_col = divmod(goal_index, N)
            
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
        _, _, current_node = heapq.heappop(queue) # ignore f and tie_breaker for now and store the node itself in the queue for easier access to its attributes
        if is_goal_state(current_node.state, goal):
            print(f"Nodes expanded: {nodes_expanded}, Max queue size: {max_queue_size}") # print stats when goal is found
            return current_node
        nodes_expanded += 1
        
        for neighbor, move in get_neighbors(current_node.state): # generate neighbors and the move that led to them
            t = tuple(neighbor) # convert to tuple for hashing in best_g
            new_g = current_node.g + 1
            if t not in best_g or new_g < best_g[t]:
                h = heuristic_fn(neighbor)
                best_g[t] = new_g # update best g(n) for this state
                child_node = SearchNode(state=neighbor, parent=current_node, cost=new_g, heuristic=h, move=move)
                tie_breaker += 1 # increment tie breaker for each new node to ensure unique ordering in the priority queue
                heapq.heappush(queue, (child_node.f, tie_breaker, child_node))
            
            if len(queue) > max_queue_size: # track max queue size
                max_queue_size = len(queue)
    
    print("No solution found.")
    return None

# call general_search with the appropriate heuristic function based on user choice and print the solution path if found
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
    puzzle_wall = len(str(N * N - 1)) # calculate width based on largest tile number
    line = "+" + ("-" * (puzzle_wall + 2) + "+") * N
    print(line)
    for r in range(N):
        row_str = '|'
        for c in range(N):
            value = puzzle[r * N + c]
            if value == 0:
                cell = ' ' * (puzzle_wall) # represent blank tile with spaces
            else:
                cell = f"{value:>{puzzle_wall}}" # right-align the tile number
            
            row_str += f" {cell} |"
        print(row_str)
        print(line)
    
    print() # extra newline for spacing

# prints out the solution path from start to goal by following parent pointers
def print_solution_path(node):
    path = []
    while node is not None:
        path.append(node) # store the node itself to access move, g, h, f later
        node = node.parent
    
    path.reverse() # reverse to get path from start to goal
        
    print(f"\nSolution depth: {path[-1].g}\n")
    for step in path:
        print(f"Move: {step.move}   g(n)={step.g}  h(n)={step.h}  f(n)={step.f}")
        print_puzzle(step.state)
    return path

def main():
    global N, goal, goal_pos # make these global so they can be accessed in heuristic functions
    
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
        
        N = input("Enter the size of the puzzle (N for NxN, e.g. 3 for 3x3) or n/no to exit: ").strip()
        
        if N.lower() in ['n', 'no']:
            print("Exiting the program.")
            break
        
        try:
            N = int(N) # convert to integer
            if N < 2:
                print("Invalid size. Please enter an integer greater than or equal to 2.")
                continue

        except ValueError:
            print("Invalid input. Please enter an integer.")
            continue
        
        goal = list(range(1, N*N)) + [0] # goal state for NxN puzzle
        goal_pos = {value: idx for idx, value in enumerate(goal)} # precompute goal positions for heuristic calculations
        if N == 3:
            print("1. Use a predefined puzzle")
            print("2. Enter your own puzzle")
            print("3. Exit")
        else:
            print("1. Use a predefined puzzle (only available for 3x3)")
            print("2. Enter your own puzzle")
            print("3. Exit")
        
        menu_choice = input("\nEnter your choice (1-3): ").strip()
        
        if menu_choice == "1" and N == 3:
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

            puzzle = puzzles[int(puzzle_choice)][1] # get the selected puzzle state
            puzzle_name = puzzles[int(puzzle_choice)][0] # get the selected puzzle name for display
            print(f"\nSelected: {puzzle_name}")
            print(f"puzzle: {puzzle}")

            search_choice = input("\nSelect search algorithm:\n1. Uniform Cost Search\n2. A* with Misplaced Tile Heuristic\n3. A* with Manhattan Distance Heuristic\nEnter choice (1-3): ").strip()
            if search_choice not in ['1', '2', '3']:
                print("Invalid choice.")
                continue
            if search_choice == '1':
                run_ucs(puzzles[int(puzzle_choice)][1]) # run UCS on the selected puzzle
            elif search_choice == '2':
                run_a_star_misplaced(puzzles[int(puzzle_choice)][1]) # run A* with misplaced tile heuristic on the selected puzzle
            elif search_choice == '3':
                run_a_star_manhattan(puzzles[int(puzzle_choice)][1]) # run A* with Manhattan distance heuristic on the selected puzzle
        elif menu_choice == "1" and N != 3:
            print("Predefined puzzles are only available for 3x3 puzzles.")
            
        elif menu_choice == "2":
            puzzle_input = input(f"\nEnter your puzzle as {N}*{N} (0 for blank), separated by spaces (e.g. '1 2 3 4 5 6 7 8 0'): ").strip()
            try:
                puzzle = list(map(int, puzzle_input.split()))
            except ValueError:
                print("Invalid input. Please enter numbers only.")
                continue
            
            if len(puzzle) != N*N:
                print(f"Invalid input. Please enter exactly {N*N} numbers.")
                continue
            
            if puzzle.count(0) != 1:
                print("Invalid puzzle. There must be exactly one blank tile (0).")
                continue
            
            if sorted(puzzle) != list(range(N*N)):
                print(f"Invalid puzzle. Please enter numbers from 0 to {N*N - 1} without duplicates.")
                continue
            
            search_choice = input("\nSelect search algorithm:\n1. Uniform Cost Search\n2. A* with Misplaced Tile Heuristic\n3. A* with Manhattan Distance Heuristic\nEnter choice (1-3): ").strip()
            if search_choice not in ['1', '2', '3']:
                print("Invalid choice.")
                continue
            if search_choice == '1':
                run_ucs(puzzle) # run UCS on the user-entered puzzle
            elif search_choice == '2':
                run_a_star_misplaced(puzzle) # run A* with misplaced tile heuristic on the user-entered puzzle
            elif search_choice == '3':
                run_a_star_manhattan(puzzle) # run A* with Manhattan distance heuristic on the user-entered puzzle
                
        elif menu_choice == "3":
            print("\nThank you for using 8-Puzzle Solver. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue
    
if __name__ == "__main__":
    main()