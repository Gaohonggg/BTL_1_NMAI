from queue import Queue
import copy
import time


class Problem(object):

    # Class đại diện cho Sudoku, giúp xác định các hành động hợp lệ và kiểm tra điều kiện đích.

    def __init__(self, initial):
        self.initial = initial  # Bảng Sudoku ban đầu
        self.type = len(initial)  # Xác định kích thước bảng (6x6 hoặc 9x9)
        # Xác định chiều cao của từng khối nhỏ (2 với 6x6, 3 với 9x9)
        self.height = int(self.type/3)

    # Trả về tập hợp các số hợp lệ từ các giá trị không xuất hiện trong bảng đã sử dụng
    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    # Return ô trống đầu tiên (marked with 0)
    def get_spot(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column

    def actions(self, state):
        # Xác định tập hợp các số hợp lệ có thể được đặt trên bảng
        number_set = range(1, self.type+1)
        in_column = []  # Danh sách các giá trị hợp lệ trong cột vị trí
        in_block = []  # Danh sách các giá trị hợp lệ trong góc phần tư của vị trí

        # Nhận chỗ trống đầu tiên
        row, column = self.get_spot(self.type, state)

       # Lọc các giá trị hợp lệ dựa trên hàng
        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)

       # Lọc các giá trị hợp lệ dựa trên cột
        for column_index in range(self.type):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)

       # Lọc các giá trị hợp lệ dựa trên góc phần tư
        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3

        for block_row in range(0, self.height):
            for block_column in range(0, 3):
                in_block.append(state[row_start + block_row]
                                [column_start + block_column])
        options = self.filter_values(options, in_block)

        for number in options:
            yield number, row, column

    # Trả về bảng đã cập nhật sau khi thêm giá trị hợp lệ mới
    def result(self, state, action):

        play = action[0]
        row = action[1]
        column = action[2]

    # Thêm giá trị hợp lệ mới vào bảng
        new_state = copy.deepcopy(state)
        new_state[row][column] = play

        return new_state

    # Sử dụng tổng của từng hàng, cột và góc phần tư để xác định tính hợp lệ của trạng thái bảng

    def goal_test(self, state):
        # Tổng dự kiến ​​của mỗi hàng, cột hoặc góc phần tư.
        total = sum(range(1, self.type+1))
       # Kiểm tra hàng và cột và trả về false nếu tổng số không hợp lệ
        for row in range(self.type):
            if (len(state[row]) != self.type) or (sum(state[row]) != total):
                return False

            column_total = 0
            for column in range(self.type):
                column_total += state[column][row]

            if (column_total != total):
                return False

       # Kiểm tra các góc phần tư và trả về false nếu tổng số không hợp lệ
        for column in range(0, self.type, 3):
            for row in range(0, self.type, self.height):

                block_total = 0
                for block_row in range(0, self.height):
                    for block_column in range(0, 3):
                        block_total += state[row +
                                             block_row][column + block_column]

                if (block_total != total):
                    return False

        return True


class Node:

    def __init__(self, state, action=None):
        self.state = state
        self.action = action

    # Sử dụng từng hành động để tạo trạng thái bảng mới
    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

   # Trả về nút với trạng thái bảng mới
    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        return Node(next, action)


def BFS(problem):
    # Tạo nút ban đầu của cây vấn đề chứa bảng gốc
    node = Node(problem.initial)
   # Kiểm tra xem bảng gốc có đúng không và trả lại ngay nếu hợp lệ
    if problem.goal_test(node.state):
        return node

    frontier = Queue()
    frontier.put(node)

    # Lặp lại cho đến khi tất cả các nút được khám phá hoặc tìm thấy giải pháp
    while (frontier.qsize() != 0):

        node = frontier.get()
        for child in node.expand(problem):
            if problem.goal_test(child.state):
                return child

            frontier.put(child)

    return None


def solve_bfs(board):
    print("\nSolving with BFS...")
    start_time = time.time()

    problem = Problem(board)
    solution = BFS(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print("Found solution")
        for row in solution.state:
            print(row)
    else:
        print("No possible solutions")

    print("Elapsed time: " + str(elapsed_time))
