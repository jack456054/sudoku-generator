import random
import copy
from .core import SudokuCore
from .solver import SudokuSolver

class SudokuGenerator:
    def __init__(self):
        self.core = SudokuCore()
        self.solver = SudokuSolver(self.core)

    def generate(self, difficulty='Simple'):
        """
        Generates a puzzle of the given difficulty.
        Difficulty: 'Simple', 'Medium', 'Hard'
        """
        diff_levels = {'Simple': 1, 'Medium': 2, 'Hard': 3, 'Expert': 4}
        target_level = diff_levels[difficulty]
        
        # Retry loop to find specific difficulty
        max_attempts = 100 if difficulty == 'Hard' else 20
        best_puzzle = None
        best_grade = 'Simple'
        best_solution = None
        
        for attempt in range(max_attempts):
            # 1. Generate full board
            full_board = self.core.generate_full_board()
            puzzle = copy.deepcopy(full_board)
            
            # 2. List of all cell coordinates, shuffled

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        # 3. Remove cells and check
        for r, c in cells:
            removed_num = puzzle[r][c]
            puzzle[r][c] = 0
            
            # Check uniqueness
            # count_solutions backtracks and restores board, so no deepcopy needed if implemented correctly
            if self.core.count_solutions(puzzle) != 1:
                puzzle[r][c] = removed_num # Put it back, not unique
                continue
            
            # Check Grade
            grade = self.solver.grade_puzzle(puzzle)
            
            # Logic:
            # - If grade matches target, we COULD stop, but we might want to remove more to make it minimal?
            # - Actually, usually we remove as much as possible while maintaining uniqueness.
            # - BUT, simply removing more might make it harder.
            # - We want to stop when we HIT the target difficulty? Or keep going?
            # - If we want 'Medium', and current is 'Simple', we keep removing.
            # - If current is 'Medium', we are good! But we could remove more to see if it stays Medium? 
            #   Often making it sparser pushes it to Hard.
            # - If current is 'Hard' and we want 'Medium', we went too far! Put it back.
            
            diff_levels = {'Simple': 1, 'Medium': 2, 'Hard': 3, 'Expert': 4}
            current_level = diff_levels[grade]
            target_level = diff_levels[difficulty]
            
            if current_level > target_level:
                puzzle[r][c] = removed_num # Too hard
            
            # If current_level <= target_level, we keep the number removed (it's valid).
            # We want to continue to make it sparser.
            
            # However, we only consider it a "success" for the specific difficulty if it matches exactly.
            if current_level == target_level:
                 # Found a valid candidate for our target.
                 # Store it, but DO NOT stop. We want to remove more if possible.
                 best_grade = grade
                 best_puzzle = copy.deepcopy(puzzle)
                 best_solution = full_board
            
            # If current_level < target_level (e.g. have Simple, want Medium), we keep removing 
            # in hopes it becomes Medium.
            
            # Maintain the "best we found so far" logic from before, but prioritized.
            if best_puzzle is None:
                 # Backup: if we never hit target, keep the hardest one below target?
                 # Or just whatever we have.
                 pass

        # After loop, return puzzle. If we are here, we finished the board without hitting target exactly 
        # (or loop finished).
        # But wait, this is inside attempt loop.
        # Check end of attempt
        final_grade = self.solver.grade_puzzle(puzzle)
        if final_grade == difficulty:
             return puzzle, final_grade, full_board
        
        # If this attempt failed to provide target, we continue next attempt
        if best_puzzle is None or diff_levels.get(final_grade, 0) > diff_levels.get(best_grade, 0):
             best_puzzle = puzzle
             best_grade = final_grade
             best_solution = full_board
             
        # End of attempt loop
        
        if best_puzzle is None:
             # Fallback if everything failed (shouldn't happen with 0 grade)
             # But best_puzzle catches at least something. 
             # Initial best_puzzle is None.
             # Initial attempt will set it.
             return puzzle, final_grade, full_board

        return best_puzzle, best_grade, best_solution

    def print_puzzle(self, board):
        self.core.print_board(board)
