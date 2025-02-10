import random
import copy

# Kích thước Sudoku
N = 9
block_size = 3


def get_block_indices(block_row, block_col):
    """
    Lấy danh sách các chỉ số (i, j) của một khối 3x3 theo vị trí (block_row, block_col)
    """
    indices = []
    for i in range(block_row * block_size, (block_row + 1) * block_size):
        for j in range(block_col * block_size, (block_col + 1) * block_size):
            indices.append((i, j))
    return indices

def initialize_individual(puzzle, fixed):
    """
    Khởi tạo một cá thể (individual) từ puzzle ban đầu:
    - Ở mỗi khối 3x3, giữ các ô cố định và điền ngẫu nhiên các số còn thiếu sao cho khối có đủ số từ 1 đến 9.
    """
    individual = copy.deepcopy(puzzle)
    for block_row in range(block_size):
        for block_col in range(block_size):
            indices = get_block_indices(block_row, block_col)
            fixed_nums = [individual[i][j] for (i, j) in indices if fixed[i][j]]
            missing = [num for num in range(1, 10) if num not in fixed_nums]
            random.shuffle(missing)
            for (i, j) in indices:
                if not fixed[i][j]:
                    individual[i][j] = missing.pop()
    return individual

def fitness(individual):
    """
    Tính số xung đột (conflict) trên hàng và cột.
    Giá trị càng nhỏ thì cá thể càng tốt (0 nghĩa là giải được Sudoku).
    """
    conflicts = 0
    # Kiểm tra xung đột trên hàng
    for row in individual:
        conflicts += (len(row) - len(set(row)))
    # Kiểm tra xung đột trên cột
    for col in range(N):
        column = [individual[row][col] for row in range(N)]
        conflicts += (len(column) - len(set(column)))
    return conflicts

def selection(population, fitnesses, tournament_size=3):
    """
    Lựa chọn theo phương pháp Tournament:
    - Với mỗi lượt, chọn ngẫu nhiên tournament_size cá thể và chọn cá thể có fitness tốt nhất.
    """
    selected = []
    pop_size = len(population)
    for _ in range(pop_size):
        candidates = random.sample(range(pop_size), tournament_size)
        best = min(candidates, key=lambda idx: fitnesses[idx])
        selected.append(copy.deepcopy(population[best]))
    return selected

def crossover(parent1, parent2, fixed, crossover_rate=0.9):
    """
    Lai tạo theo cấp khối:
    - Với mỗi khối 3x3, với xác suất crossover_rate, lấy khối từ parent2 thay cho parent1 (chỉ áp dụng cho ô không cố định).
    """
    child = copy.deepcopy(parent1)
    for block_row in range(block_size):
        for block_col in range(block_size):
            if random.random() < crossover_rate:
                indices = get_block_indices(block_row, block_col)
                for (i, j) in indices:
                    if not fixed[i][j]:
                        child[i][j] = parent2[i][j]
    return child

def mutate(individual, fixed, mutation_rate=0.1):
    """
    Đột biến:
    - Trong mỗi khối 3x3, với xác suất mutation_rate, chọn ngẫu nhiên 2 ô không cố định và hoán đổi giá trị.
    """
    for block_row in range(block_size):
        for block_col in range(block_size):
            if random.random() < mutation_rate:
                indices = get_block_indices(block_row, block_col)
                mutable = [(i, j) for (i, j) in indices if not fixed[i][j]]
                if len(mutable) >= 2:
                    (i1, j1), (i2, j2) = random.sample(mutable, 2)
                    individual[i1][j1], individual[i2][j2] = individual[i2][j2], individual[i1][j1]
    return individual

def local_improvement(individual, fixed, iterations=10):
    """
    Cải thiện cục bộ cá thể bằng cách hoán đổi ngẫu nhiên các ô không cố định trong cùng 1 khối nếu giúp giảm số xung đột.
    - Thực hiện tối đa 'iterations' vòng lặp cải thiện.
    """
    current = copy.deepcopy(individual)
    current_fitness = fitness(current)
    improved = True
    while improved and iterations > 0:
        improved = False
        for block_row in range(block_size):
            for block_col in range(block_size):
                indices = get_block_indices(block_row, block_col)
                non_fixed = [(i, j) for (i, j) in indices if not fixed[i][j]]
                if len(non_fixed) < 2:
                    continue
                # Kiểm tra tất cả các cặp hoán đổi trong khối
                for idx1 in range(len(non_fixed)):
                    for idx2 in range(idx1+1, len(non_fixed)):
                        (i1, j1) = non_fixed[idx1]
                        (i2, j2) = non_fixed[idx2]
                        new_ind = copy.deepcopy(current)
                        new_ind[i1][j1], new_ind[i2][j2] = new_ind[i2][j2], new_ind[i1][j1]
                        new_fit = fitness(new_ind)
                        if new_fit < current_fitness:
                            current = new_ind
                            current_fitness = new_fit
                            improved = True
                            break
                    if improved:
                        break
                if improved:
                    break
        iterations -= 1
    return current

def genetic_algorithm(puzzle, max_generations=1000, population_size=200, 
                      mutation_rate=0.1, crossover_rate=0.9, elitism_rate=0.05,
                      local_search_rate=0.3, local_iterations=10):
    """
    Thuật toán di truyền giải Sudoku nâng cấp:
    - fixed: ma trận boolean đánh dấu các ô cố định.
    - population: khởi tạo dân số sao cho ở mỗi khối 3x3 chứa đủ số từ 1 đến 9.
    - Áp dụng elitism để bảo toàn các cá thể tốt qua các thế hệ.
    - Lai ghép và đột biến được điều chỉnh qua các xác suất.
    - Sau đột biến, với xác suất local_search_rate, thực hiện bước cải thiện cục bộ trên cá thể.
    """
    fixed = [[True if puzzle[i][j] != 0 else False for j in range(N)] for i in range(N)]
    population = [initialize_individual(puzzle, fixed) for _ in range(population_size)]
    best_fitness = float('inf')
    best_individual = None
    generation = 0

    while generation < max_generations:
        fitnesses = [fitness(ind) for ind in population]

        # Nếu có cá thể đạt fitness = 0, tức giải được Sudoku
        if 0 in fitnesses:
            index = fitnesses.index(0)
            print("Giải được Sudoku tại thế hệ", generation)
            return population[index]

        min_fit = min(fitnesses)
        if min_fit < best_fitness:
            best_fitness = min_fit
            best_individual = copy.deepcopy(population[fitnesses.index(min_fit)])
            print("Thế hệ", generation, "- Fitness tốt nhất:", best_fitness)
        
        else:
            print("Thế hệ ", generation)

        # Elitism: giữ lại một số cá thể tốt nhất của thế hệ hiện tại
        elite_count = max(1, int(elitism_rate * population_size))
        sorted_population = [ind for _, ind in sorted(zip(fitnesses, population), key=lambda x: x[0])]
        elites = [copy.deepcopy(ind) for ind in sorted_population[:elite_count]]

        # Lựa chọn theo tournament
        selected = selection(population, fitnesses)
        next_population = []
        for i in range(0, population_size - elite_count, 2):
            parent1 = selected[i]
            parent2 = selected[(i+1) % population_size]
            child1 = crossover(parent1, parent2, fixed, crossover_rate)
            child2 = crossover(parent2, parent1, fixed, crossover_rate)
            child1 = mutate(child1, fixed, mutation_rate)
            child2 = mutate(child2, fixed, mutation_rate)
            # Áp dụng cải thiện cục bộ với xác suất local_search_rate
            if random.random() < local_search_rate:
                child1 = local_improvement(child1, fixed, local_iterations)
            if random.random() < local_search_rate:
                child2 = local_improvement(child2, fixed, local_iterations)
            next_population.extend([child1, child2])

        population = elites + next_population[:population_size - elite_count]
        generation += 1

    print("Không tìm được lời giải sau", max_generations, "thế hệ. Fitness tốt nhất đạt được:", best_fitness)
    return best_individual

if __name__ == "__main__":

    puzzle = [
    [7, 0, 6, 0, 0, 0, 0, 8, 0],
    [0, 0, 2, 1, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 7],
    [0, 9, 0, 0, 0, 0, 3, 5, 0],
    [8, 0, 0, 5, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 2, 7, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 8, 0, 9],
    [0, 0, 0, 0, 0, 8, 4, 0, 0]
    ]

    
    solution = genetic_algorithm(puzzle)
    print("\nLời giải tìm được:")
    for row in solution:
        print(row)