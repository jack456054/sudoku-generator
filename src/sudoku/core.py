import random

class SudokuCore:
    def __init__(self):
        self.rows = 9
        self.cols = 9

    def print_board(self, board):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(board[i][j])
                else:
                    print(str(board[i][j]) + " ", end="")

    def is_valid(self, board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False

        # Check col
        for x in range(9):
            if board[x][col] == num:
                return False

        # Check box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def solve_sudoku_backtracking(self, board):
        """Standard backtracking solver to find any solution."""
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty

        for i in range(1, 10):
            if self.is_valid(board, row, col, i):
                board[row][col] = i
                if self.solve_sudoku_backtracking(board):
                    return True
                board[row][col] = 0
        return False

    def count_solutions(self, board, limit=2):
        """Checks if the board has a unique solution. Returns number of solutions found up to limit."""
        empty = self.find_empty(board)
        if not empty:
            return 1
        
        row, col = empty
        count = 0
        
        for i in range(1, 10):
            if self.is_valid(board, row, col, i):
                board[row][col] = i
                count += self.count_solutions(board, limit)
                board[row][col] = 0
                if count >= limit:
                    return count
        return count

    def generate_full_board(self):
        """Generates a random full valid board."""
        board = [[0 for _ in range(9)] for _ in range(9)]
        # Fill diagonal 3x3 matrices independently first (they don't conflict)
        for i in range(0, 9, 3):
            self.fill_box(board, i, i)
        
        # Solve the rest
        self.solve_sudoku_backtracking(board)
        return board

    def fill_box(self, board, row, col):
        num = 0
        for i in range(3):
            for j in range(3):
                while True:
                    num = random.randint(1, 9)
                    if self.is_unused_in_box(board, row, col, num):
                        break
                board[row + i][col + j] = num

    def is_unused_in_box(self, board, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if board[row_start + i][col_start + j] == num:
                    return False
        return True
