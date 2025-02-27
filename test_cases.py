from Blind_Search_Sudoku import solve_bfs
from Blind_Search_Sudoku import solve_dfs

print("\n\nTest 6x6..")
puzzle = [
    [6, 2, 0, 5, 0, 3],
    [0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 3, 0],
    [0, 6, 0, 0, 2, 0],
    [0, 0, 0, 3, 4, 6],
    [3, 0, 6, 0, 0, 0]]

print("Problem:")
for row in puzzle:
    print(row)

solve_bfs(puzzle)
solve_dfs(puzzle)

print("\n\nTest 6x6..")
puzzle = [
    [0, 2, 0, 4, 0, 6],
    [0, 0, 6, 0, 2, 0],
    [2, 0, 0, 0, 3, 1],
    [6, 0, 3, 0, 1, 0],
    [0, 3, 0, 6, 0, 4],
    [4, 0, 1, 0, 5, 0]
]

print("Problem:")
for row in puzzle:
    print(row)

solve_bfs(puzzle)
solve_dfs(puzzle)

print("\n\nTest 9x9..")
puzzle = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
          [3, 0, 1, 0, 0, 9, 0, 0, 0],
          [7, 0, 0, 0, 0, 4, 6, 2, 0],
          [0, 0, 0, 0, 0, 5, 0, 0, 6],
          [2, 0, 0, 3, 0, 0, 5, 0, 0],
          [0, 7, 0, 6, 0, 0, 8, 0, 0],
          [0, 5, 0, 4, 7, 0, 0, 0, 0],
          [0, 6, 0, 0, 0, 0, 2, 4, 5],
          [8, 0, 0, 0, 0, 0, 0, 7, 0]]

print("Problem:")
for row in puzzle:
    print(row)

solve_bfs(puzzle)
solve_dfs(puzzle)

print("\n\nTest 9x9...")
puzzle = [[3, 0, 0, 4, 1, 5, 2, 0, 0],
          [4, 0, 9, 7, 6, 0, 0, 0, 1],
          [0, 6, 0, 0, 2, 8, 4, 0, 0],
          [1, 0, 0, 0, 8, 0, 0, 5, 7],
          [0, 4, 5, 3, 0, 0, 0, 0, 0],
          [8, 0, 2, 1, 0, 0, 6, 0, 0],
          [0, 5, 0, 0, 0, 0, 0, 0, 6],
          [9, 0, 4, 0, 0, 0, 1, 3, 5],
          [6, 1, 0, 5, 0, 0, 7, 2, 8]]

print("Problem:")
for row in puzzle:
    print(row)

solve_bfs(puzzle)
solve_dfs(puzzle)
