from sudoku.generator import SudokuGenerator
import time

def test_generation():
    gen = SudokuGenerator()
    
    print("Testing Simple Generation...")
    p1, g1, s1 = gen.generate('Simple')
    print(f"Requested: Simple, Got: {g1}")
    gen.print_puzzle(p1)
    
    print("\nTesting Medium Generation...")
    p2, g2, s2 = gen.generate('Medium')
    print(f"Requested: Medium, Got: {g2}")
    gen.print_puzzle(p2)
    
    # Hard might take longer or be rarer, let's try.
    print("\nTesting Hard Generation...")
    p3, g3, s3 = gen.generate('Hard')
    print(f"Requested: Hard, Got: {g3}")
    gen.print_puzzle(p3)

if __name__ == "__main__":
    test_generation()
