import sys
from .generator import SudokuGenerator

def main():
    print("Sudoku Generator")
    print("----------------")
    print("Select Difficulty:")
    print("1. Simple")
    print("2. Medium")
    print("3. Hard")
    
    choice = input("Enter choice (1-3): ").strip()
    
    diff_map = {'1': 'Simple', '2': 'Medium', '3': 'Hard'}
    difficulty = diff_map.get(choice, 'Simple')
    
    print(f"\nGenerating {difficulty} puzzle... (this might take a second)")
    
    gen = SudokuGenerator()
    puzzle, grade, solution = gen.generate(difficulty)
    
    print(f"\nGenerated Puzzle (Actual Grade: {grade}):")
    gen.print_puzzle(puzzle)
    
    print("\nCopy format (0 is empty):")
    print(str(puzzle).replace('],', '],\n'))
    
    print("\nSolution:")
    gen.print_puzzle(solution)

if __name__ == "__main__":
    main()
