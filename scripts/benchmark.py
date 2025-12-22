import time
from sudoku.generator import SudokuGenerator

def benchmark():
    gen = SudokuGenerator()
    
    start = time.time()
    # Generate 5 Simple
    print("Generating 5 Simple...")
    for _ in range(5):
        gen.generate('Simple')
    mid1 = time.time()
    print(f"Simple took: {mid1 - start:.2f}s")
    
    # Generate 2 Medium
    print("Generating 2 Medium...")
    for _ in range(2):
        gen.generate('Medium')
    mid2 = time.time()
    print(f"Medium took: {mid2 - mid1:.2f}s")

if __name__ == "__main__":
    benchmark()
