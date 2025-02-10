import time

class MinesweeperSolver:
    def __init__(self, grid):
        self.grid = grid
        self.n = len(grid)
        self.m = len(grid[0])
        self.solution = [['_' for _ in range(self.m)] for _ in range(self.n)]
        self.mines = set()

    def _get_adjacent_cells(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < self.n and 0 <= y + dy < self.m]

    def _valid_state(self):
        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.grid[i][j], int):
                    count = sum((ni, nj) in self.mines for ni, nj in self._get_adjacent_cells(i, j))
                    if count != self.grid[i][j]:
                        return False
        return True

    def _dfs(self, i=0, j=0):
        if i == self.n:
            return self._valid_state()
        
        next_i, next_j = (i, j + 1) if j + 1 < self.m else (i + 1, 0)
        
        if self.grid[i][j] == '*':
            self.mines.add((i, j))
            if self._dfs(next_i, next_j):
                return True
            self.mines.remove((i, j))
        
        return self._dfs(next_i, next_j)

    def solve(self):
        if not self._dfs():
            print("-1")
            return

        for i, j in self.mines:
            self.solution[i][j] = 'X'

        for row in self.solution:
            print(' '.join(row))

def read_grid():
    n = int(input("Nhập số hàng: "))
    m = int(input("Nhập số cột: "))
    grid = []
    
    print("Nhập lưới (dùng * cho ô chưa biết, số nguyên cho ô có số):")
    for _ in range(n):
        row = input().split()
        grid.append([int(x) if x.isdigit() else '*' for x in row])

    return grid

def main():
    grid = read_grid()
    start_time = time.time()
    solver = MinesweeperSolver(grid)
    print("Kết quả:")
    solver.solve()
    elapsed_time = time.time() - start_time
    print("Thời gian: " + str(elapsed_time))

if __name__ == "__main__":
    main()
