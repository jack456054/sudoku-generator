import copy

class SudokuSolver:
    def __init__(self, core):
        self.core = core

    def get_candidates(self, board):
        """Returns a 9x9 grid of sets containing possible candidates for each cell."""
        candidates = [[set() for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for num in range(1, 10):
                        if self.core.is_valid(board, r, c, num):
                            candidates[r][c].add(num)
        return candidates

    def apply_naked_singles(self, board, candidates):
        """Finds cells with only 1 candidate."""
        progress = False
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0 and len(candidates[r][c]) == 1:
                    num = candidates[r][c].pop()
                    board[r][c] = num
                    progress = True
        return progress

    def apply_hidden_singles(self, board, candidates):
        """Finds numbers that can only go in one spot in a row, col, or box."""
        progress = False
        
        # Rows
        for r in range(9):
            counts = {num: [] for num in range(1, 10)}
            for c in range(9):
                if board[r][c] == 0:
                    for cand in candidates[r][c]:
                        counts[cand].append(c)
            for num, cols in counts.items():
                if len(cols) == 1:
                    c = cols[0]
                    board[r][c] = num
                    candidates[r][c] = set()
                    progress = True

        # Cols
        if not progress:
            for c in range(9):
                counts = {num: [] for num in range(1, 10)}
                for r in range(9):
                    if board[r][c] == 0:
                        for cand in candidates[r][c]:
                            counts[cand].append(r)
                for num, rows in counts.items():
                    if len(rows) == 1:
                        r = rows[0]
                        board[r][c] = num
                        candidates[r][c] = set()
                        progress = True
        
        # Boxes
        if not progress:
            for box_r in range(0, 9, 3):
                for box_c in range(0, 9, 3):
                    counts = {num: [] for num in range(1, 10)}
                    for i in range(3):
                        for j in range(3):
                            r, c = box_r + i, box_c + j
                            if board[r][c] == 0:
                                for cand in candidates[r][c]:
                                    counts[cand].append((r, c))
                    for num, locs in counts.items():
                        if len(locs) == 1:
                            r, c = locs[0]
                            board[r][c] = num
                            candidates[r][c] = set()
                            progress = True
        return progress

    def apply_pointing_pairs(self, board, candidates):
        """
        If in a box all candidates for number N are in the same row/col,
        remove N from the rest of that row/col.
        """
        changes = False
        for box_r in range(0, 9, 3):
            for box_c in range(0, 9, 3):
                # Count pattern of candidates in this box
                num_positions = {n: [] for n in range(1, 10)}
                for i in range(3):
                    for j in range(3):
                        r, c = box_r + i, box_c + j
                        if board[r][c] == 0:
                            for cand in candidates[r][c]:
                                num_positions[cand].append((r, c))
                
                for num, positions in num_positions.items():
                    if not positions:
                        continue
                        
                    # Check if all in same row
                    rows = set(r for r, c in positions)
                    if len(rows) == 1:
                        row = list(rows)[0]
                        # Remove from rest of row
                        for c in range(9):
                             # if c is outside this box
                            if not (box_c <= c < box_c + 3):
                                if board[row][c] == 0 and num in candidates[row][c]:
                                    candidates[row][c].remove(num)
                                    changes = True
                    
                    # Check if all in same col
                    cols = set(c for r, c in positions)
                    if len(cols) == 1:
                        col = list(cols)[0]
                        # Remove from rest of col
                        for r in range(9):
                            # if r is outside this box
                            if not (box_r <= r < box_r + 3):
                                if board[r][col] == 0 and num in candidates[r][col]:
                                    candidates[r][col].remove(num)
                                    changes = True
        return changes

    def apply_x_wing(self, board, candidates):
        """
        X-Wing: for a candidate number, if there are only 2 possible positions in a row and they form a rectangle with another row,
        we can eliminate that candidate from the columns of the rectangle. (And vice-versa for columns).
        """
        changes = False

        # Row-based X-Wing
        # Find rows where 'num' appears exactly twice
        for num in range(1, 10):
            rows_with_two = []
            for r in range(9):
                cols = []
                for c in range(9):
                    if board[r][c] == 0 and num in candidates[r][c]:
                        cols.append(c)
                if len(cols) == 2:
                    rows_with_two.append((r, set(cols)))
            
            # Check for pairs of rows sharing the same 2 columns
            for i in range(len(rows_with_two)):
                for j in range(i + 1, len(rows_with_two)):
                    r1, cols1 = rows_with_two[i]
                    r2, cols2 = rows_with_two[j]
                    if cols1 == cols2:
                        # FOUND X-WING in rows r1, r2 and columns cols1
                        c1, c2 = list(cols1)
                        for r_elim in range(9):
                            if r_elim != r1 and r_elim != r2:
                                if board[r_elim][c1] == 0 and num in candidates[r_elim][c1]:
                                    candidates[r_elim][c1].remove(num)
                                    changes = True
                                if board[r_elim][c2] == 0 and num in candidates[r_elim][c2]:
                                    candidates[r_elim][c2].remove(num)
                                    changes = True
        
        # Col-based X-Wing (omitted for brevity unless needed for "Hard" strictness, but usually Row-based is enough to catch X-wing patterns if we also rotate... or just implement)
        # Implementing Col-based for completeness
        for num in range(1, 10):
            cols_with_two = []
            for c in range(9):
                rows = []
                for r in range(9):
                    if board[r][c] == 0 and num in candidates[r][c]:
                        rows.append(r)
                if len(rows) == 2:
                    cols_with_two.append((c, set(rows)))
            
            for i in range(len(cols_with_two)):
                for j in range(i + 1, len(cols_with_two)):
                    c1, rows1 = cols_with_two[i]
                    c2, rows2 = cols_with_two[j]
                    if rows1 == rows2:
                        r1, r2 = list(rows1)
                        for c_elim in range(9):
                            if c_elim != c1 and c_elim != c2:
                                if board[r1][c_elim] == 0 and num in candidates[r1][c_elim]:
                                    candidates[r1][c_elim].remove(num)
                                    changes = True
                                if board[r2][c_elim] == 0 and num in candidates[r2][c_elim]:
                                    candidates[r2][c_elim].remove(num)
                                    changes = True

        return changes

    def compute_candidates_fresh(self, board):
        return self.get_candidates(board)

    def is_solved(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return False
        return True

    def grade_puzzle(self, original_board):
        """
        Tries to solve the puzzle and returns key difficulty used.
        Returns: 'Simple', 'Medium', 'Hard', or 'Expert'
        """
        board = copy.deepcopy(original_board)
        candidates = self.compute_candidates_fresh(board)
        
        needed_medium = False
        needed_hard = False

        while not self.is_solved(board):
             # 1. Try Simple (Single Pass until stuck)
             progress_simple = True
             while progress_simple:
                 progress_simple = False
                 if self.apply_naked_singles(board, candidates):
                     candidates = self.compute_candidates_fresh(board) 
                     progress_simple = True
                 elif self.apply_hidden_singles(board, candidates):
                     candidates = self.compute_candidates_fresh(board)
                     progress_simple = True
             
             if self.is_solved(board):
                 break

             # If stuck, try Medium
             if self.apply_pointing_pairs(board, candidates):
                 needed_medium = True
                 continue
            
             # If stuck, try Hard
             if self.apply_x_wing(board, candidates):
                 needed_hard = True
                 continue
            
             # If stuck completely
             break
        
        if self.is_solved(board):
            if needed_hard:
                return 'Hard'
            elif needed_medium:
                return 'Medium'
            else:
                return 'Simple'
        else:
            return 'Expert'
