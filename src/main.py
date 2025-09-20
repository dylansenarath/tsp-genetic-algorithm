import random
import math
from pathlib import Path

# Read our input file
# Resolve path to data/input.txt relative to project root
here = Path(__file__).resolve().parent.parent
data_file = here / "data" / "input.txt"

with open(data_file, "r") as file:
    f = file.readlines()


# Covert the input file into a list
newList = []
for line in f[1:]:  # Skips first line with number of cities
    newList.append(tuple(map(int, line.split())))  # # line.split() converts our input into a list of strings
    # map function allows us to convert that list of strings into integers
    # tuple saves the set of coordinates from each line into a single variable that can be accessed individually later

# Convert number of cities into an integer
num_cities = int(f[0].strip())


def adjust_parameters_based_on_complexity(num_cities):
    if num_cities <= 10:  # Class 1 (easy)
        population_size = 50
        num_generations = 100
        mutation_rate = 0.05
        num_elites = 1
    elif num_cities <= 50:  # Class 2 (medium)
        population_size = 150
        num_generations = 200
        mutation_rate = 0.1
        num_elites = 2
    elif num_cities <= 100:  # Class 3 (hard)
        population_size = 300
        num_generations = 500
        mutation_rate = 0.15
        num_elites = 3
    else:  # Class 4 (complex)
        population_size = 500
        num_generations = 1000
        mutation_rate = 0.2
        num_elites = 5

    return population_size, num_generations, mutation_rate, num_elites


def create_initial_population(size, cities):
    initial_population = []  # Create a list of possible paths initialized to 0
    for _ in range(size):
        path = cities.copy()  # Create variable with path initially set to original set of coordinates
        random.shuffle(path)  # Randomly shuffle the city list (**could introduce random seed**)
        initial_population.append(path)  # Add newly shuffled list to our initial population
    return initial_population


# Calculate distance between two points using Euclidian formula
def calculate_distance(city1, city2):
    return math.sqrt((city2[0] - city1[0]) ** 2 + (city2[1] - city1[1]) ** 2 + (city2[2] - city1[2]) ** 2)


# Calculates fitness value for a given path based on its total distance to traverse cities
def calculate_fitness(path):
    total_distance = 0
    for i in range(len(path)-1):  # Iterate through every city. Range function starts at 0, so we stop at the length - 1
        total_distance += calculate_distance(path[i], path[i+1])  # Add distance between adjacent cities to our total
    total_distance += calculate_distance(path[-1], path[0])  # Add distance to return to the start to our total
    return total_distance  # Return the total distance as a representation of the 'fitness' for that path


# Ranks the paths in our population in ascending order based on fitness score (lower is better)
def rank_population(path_population):
    ranks = []
    for i in range(len(path_population)):
        fitness = calculate_fitness(path_population[i])
        ranks.append((i, fitness))  # Appends a tuple to our rank list including an identifier and the fitness level
    ranks.sort(key=lambda x: x[1])  # Sort items by fitness from lowest to highest.
    return ranks


# Select parents based on their fitness relative to the rest of the group, based on roulette wheel selection.
def create_mating_pool(pop, ranks):
    mating_pool = []
    total_fitness = 0
    for _, fitness in ranks:  # Iterates over the tuples in our rank list, accessing their fitness value
        total_fitness += fitness  # Add the individual's fitness to the total
    for _ in range(len(pop)):  # Run parent selection an equal amount of times to the size of our population
        rand = random.uniform(0, total_fitness)  # Pick a random number between 0 and the total of fitness scores
        current_sum = 0  # Set roulette wheel at starting point 0
        for index, fitness in ranks:  # Iterate through our rank list
            current_sum += fitness  # Add current element's fitness to the sum
            if current_sum > rand:  # Check to see if the sum has surpassed the random fixed point
                mating_pool.append(pop[index])  # If so, select it as a parent
                break  # Leave current loop and start again to find new parent
    return mating_pool  # Return list of selected parents


def crossover(parent1, parent2, start_index, end_index):
    # Could improve efficiency using child = [None] * len(parent1)
    child = []
    for i in range(len(parent1)):
        child.append(None)
    for i in range(start_index, end_index + 1):  # Iterates through subarray in parent1
        child[i] = parent1[i]  # Copies each index in range from parent over to child
    current_pos = 0  # Initializes an index to track where we are in parent 2 to fill remaining "None" positions
    for i in range(len(child)):  # Iterates over values in child to check if they are filled
        if child[i] is None:
            while parent2[current_pos] in child:  # Loops through parent2 until it finds a city not already in child
                current_pos += 1
            child[i] = parent2[current_pos]  # When a city is found that is not already in child, it is inserted
            current_pos += 1  # Move on to next city in Parent2
    return child


def mutate(path, mutation_rate=0.1):  # Setting default mutation rate to 10% ensures mutation even if not specified
    if random.random() < mutation_rate:  # random.random give random number from 0.0 to 1.0
        start = random.randint(0, len(path) - 2)  # Picks a starting index between 0 and the second to last element
        end = random.randint(start + 1, len(path) - 1)  # Picks an end point at least 1 element away from start
        path[start:end+1] = reversed(path[start:end+1])  # Reverses subsegment of our path.
        # The +1 is required in our above equation because it uses slicing which does not include the last index
    return path


def next_generation(current_population, ranks, elites=1):
    new_parents = create_mating_pool(current_population, ranks)
    next_gen = []

    for i in range(elites):
        next_gen.append(current_population[ranks[i][0]])

    for i in range(elites, len(new_parents), 2):
        parent1 = new_parents[i % len(new_parents)]
        parent2 = new_parents[(i+1) % len(new_parents)]
        child = crossover(parent1, parent2, 1, len(parent1) // 2)
        next_gen.append(mutate(child))

    return next_gen


# ******** MAIN LOOP *********

# Adjust parameters based on problem size (complexity)
population_size, num_generations, mutation_rate, num_elites = adjust_parameters_based_on_complexity(num_cities)

population = create_initial_population(population_size, newList)

for generation in range(num_generations):
    rank_list = rank_population(population)
    population = next_generation(population, rank_list, num_elites)

# Output the best fitness and corresponding path
print(f"{rank_list[0][1]:.3f}")
for city in population[0]:
    print(f"{city[0]} {city[1]} {city[2]}")

