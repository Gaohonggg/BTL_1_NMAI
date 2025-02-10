import random as random
import time
import os

POPULATION_SIZE = 1000

MAX_GENERATION = 1000

MUTATION_PROBABILITY = 0.1

CROSSOVER_PROBABILITY = 0.95


def make_gene(initial_gene):
    mapp = {}
    gene = list(range(1, 10))
    random.shuffle(gene)
    for i in range(9):
        mapp[gene[i]] = i
    for i in range(9):
        if initial_gene[i] != 0 and gene[i] != initial_gene[i]:
            temp = gene[i], gene[mapp[initial_gene[i]]]
            gene[mapp[initial_gene[i]]], gene[i] = temp
            mapp[initial_gene[i]], mapp[temp[0]] = i, mapp[initial_gene[i]]
    return gene


def make_chromosome(initial_chromosome):
    chromosome = []
    for i in range(9):
        chromosome.append(make_gene(initial_chromosome[i]))
    return chromosome


def create_first_generation(initial_chromosome):
    if initial_chromosome is None:
        initial_chromosome = [[0] * 9] * 9
    population = []
    for _ in range(POPULATION_SIZE):
        population.append(make_chromosome(initial_chromosome))
    return population


def calc_score(chromosome):
    score = 0
    for i in range(9):
        seen = {}
        for j in range(9):
            if chromosome[j][i] in seen:
                seen[chromosome[j][i]] += 1
            else:
                seen[chromosome[j][i]] = 1
        for key in seen:
            score -= (seen[key] - 1)

    for m in range(3):
        for n in range(3):
            seen = {}
            for i in range(3 * n, 3 * (n + 1)):
                for j in range(3 * m, 3 * (m + 1)):
                    if chromosome[j][i] in seen:
                        seen[chromosome[j][i]] += 1
                    else:
                        seen[chromosome[j][i]] = 1
            for key in seen:
                score -= (seen[key] - 1)
    return score


def get_mating_pool(population):
    score_list = []
    pool = []
    for chromosome in population:
        score = calc_score(chromosome)
        score_list.append((score, chromosome))
    score_list.sort()
    weight = list(range(1, len(score_list) + 1))
    for _ in range(len(population)):
        ch = random.choices(score_list, weight)[0]
        pool.append(ch[1])
    return pool


def crossover(ch1, ch2):
    new_child_1 = []
    new_child_2 = []
    for i in range(9):
        x = random.randint(0, 1)
        if x == 1:
            new_child_1.append(ch1[i])
            new_child_2.append(ch2[i])
        elif x == 0:
            new_child_2.append(ch1[i])
            new_child_1.append(ch2[i])
    return new_child_1, new_child_2


def mutation(chromosome, mutation_probability, initial):
    for i in range(9):
        x = random.randint(0, 100)
        if x < mutation_probability * 100:
            chromosome[i] = make_gene(initial[i])
    return chromosome


def create_new_generation(population, initial, pm, pc):
    new_population = []
    i = 0
    while i < len(population):
        ch1 = population[i]
        ch2 = population[(i + 1) % len(population)]
        x = random.randint(0, 100)
        if x < pc * 100:
            ch1, ch2 = crossover(ch1, ch2)
        new_population.append(mutation(ch1, pm, initial))
        new_population.append(mutation(ch2, pm, initial))
        i += 2
    return new_population


def genetic_algorithm(initial_chromosome):
    population = create_first_generation(initial_chromosome)

    for _ in range(MAX_GENERATION):
        mating_pool = get_mating_pool(population)
        random.shuffle(mating_pool)
        population = create_new_generation(
            mating_pool, initial_chromosome, MUTATION_PROBABILITY, CROSSOVER_PROBABILITY
        )
        score_list = [calc_score(chromosome) for chromosome in population]
        max_score = max(score_list)
        if max_score == 0:
            break
    return population

 

def read_file(file_address):
    initial_chromosome = []
    file = open(file_address, 'r')
    for row in file:
        temp = row.split()
        initial_chromosome.append([int(c) for c in temp])
    
    print( initial_chromosome )
    return initial_chromosome


def print_chromosome(chromosome):
    for i in range(9):
        for j in range(9):
            print(chromosome[i][j], end=" ")
        print("")

def main():
    file_address = os.path.join(os.getcwd(), "sudoku", "testcases", "test_2.txt")
    initial_chromosome = read_file(file_address)

    start = time.time()
    population = genetic_algorithm(initial_chromosome)
    end = time.time()

    print("Execution time: ", end - start, " seconds")

    score_list = [calc_score(chromosome) for chromosome in population]
    m = max(score_list)

    for chromosome in population:
        if calc_score(chromosome) == m:
            print_chromosome(chromosome)
            break


if __name__ == "__main__":
    main()