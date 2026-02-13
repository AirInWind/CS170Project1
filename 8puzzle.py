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
    
    return neighbors

# check if goal state
def is_goal_state(puzzle):
    return puzzle == [1, 2, 3, 4, 5, 6, 7, 8, 0]

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
        
def test_print_puzzle():
    test_puzzle = [1, 2, 3, 4, 0, 5, 7, 8, 6]
    print_puzzle(test_puzzle)
    
    test_puzzle2 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    print_puzzle(test_puzzle2)
    
    test_puzzle3 = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    print_puzzle(test_puzzle3)

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
        
        test_print_puzzle() # Test the print function with different puzzles
        menu_choice = input("\nEnter your choice (1-3): ").strip()
        
        if menu_choice == "1":
            # Show predefined puzzles
            print("\n=== Predefined Puzzles ===")
            for key, (name, puzzle) in puzzles.items():
                print(f"{key}. {name}: {puzzle}")
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
            
        elif menu_choice == "2":
            print("\nWork in progress: Custom puzzle input not implemented yet.")
            
        elif menu_choice == "3":
            print("\nThank you for using 8-Puzzle Solver. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue
    
if __name__ == "__main__":
    main()