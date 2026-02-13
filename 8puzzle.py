import heapq

def main():
    # Predefined puzzles
    puzzles = {
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
                print(f"{key}. {name}: {puzzle}")
            print("0. Go back to menu")
            
            puzzle_choice = input("\nSelect a puzzle (0-5): ").strip()
            
            if puzzle_choice == "0":
                continue
            
            if puzzle_choice not in ['1', '2', '3', '4', '5']:
                print("Invalid choice.")
                continue
            
            board = puzzles[int(puzzle_choice)][1]
            puzzle_name = puzzles[int(puzzle_choice)][0]
            print(f"\nSelected: {puzzle_name}")
            print(f"Board: {board}")
            
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