def possible(grid, x, y, n):
    """To check whether n can be inserted at position (x, y)."""
    for i in range(9):
        if grid[x][i] == n:
            return False
    for i in range(9):
        if grid[i][y] == n:
            return False
    for i in range(int(x/3) * 3, int(x/3) * 3 + 3):
        for j in range(int(y/3) * 3, int(y/3) * 3 + 3):
            if grid[i][j] == n:
                return False
    return True

def findNextCell(grid, x, y):
        for i in range(x,9):
                for j in range(y,9):
                        if grid[i][j] == 0:
                                return i, j
        for i in range(0,9):
                for j in range(0,9):
                        if grid[i][j] == 0:
                                return i, j
        return -1,-1

def solveSudoku(grid, x=0, y=0):
        x, y = findNextCell(grid, x, y)
        if x == -1:
                return True
        for n in range(1,10):
                if possible(grid, x, y, n):
                        grid[x][y] = n
                        if solveSudoku(grid, x, y):
                                return True
                        grid[x][y] = 0
        return False