from GeneticAlgorithm import GeneticAlgorithm
import random
import time
from typing import List

class OneMaxGA(GeneticAlgorithm):
    """
    Genetic algorithm for solving the One-Max problem.
    Inherits from the GeneticAlgorithm abstract base class.
    """

    def __init__(self, population_size: int, chromosome_length: int, crossover_prob:float, mutation_rate: float, elitism_num: int):
        """
        Initialize the OneMaxGA instance.

        Args:
            population_size (int): Size of the population.
            chromosome_length (int): Length of each chromosome (bit string).
            mutation_rate (float): Probability of mutation for each bit.
        """
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.crossover_prob = crossover_prob
        self.mutation_rate = mutation_rate
        self.elitism_num = elitism_num
        self.population = self.initialize_population()

    def create_individual(self) -> List[int]:
        """
        Create a new individual (random bit string).

        Returns:
            List[int]: A newly created individual.
        """
        return [random.randint(0, 1) for _ in range(self.chromosome_length)]    
    
    def initialize_population(self) -> List[List[int]]:
        """
        Initialize the population with random bit strings.

        Returns:
            List[List[int]]: Initial population.
        """

        return [self.create_individual() for _ in range(self.population_size)]

    def evaluate_fitness(self, chromosome: List[int]) -> int:
        """
        Evaluate the fitness of an individual (sum of 1s in the bit string).

        Args:
            chromosome (List[int]): The bit string representing an individual.

        Returns:
            int: Fitness value.
        """
        fitness = 0 
        for bit in chromosome:
            if bit :
                fitness += 1
        
        return fitness
    
    def calculate_cumulative_probabilities(self) -> List[float]:
        """
        Calculate cumulative probabilities for each individual.

        Returns:
            List[float]: Cumulative probabilities.
        """
        total_fitness = 0
        cumulative_probabilities = []
        for individual in self.population :
            total_fitness += self.evaluate_fitness(individual)

        Probability_of_each_individual = []
        for individual in self.population :
            Probability_of_each_individual.append(self.evaluate_fitness(individual)/total_fitness)

        for i in range(len(Probability_of_each_individual)):
            if i == 0:
                cumulative_probabilities.append(Probability_of_each_individual[0])
            elif i == len(Probability_of_each_individual)-1:
                cumulative_probabilities.append(1.0)
            else:
                cumulative_probabilities.append(cumulative_probabilities[i-1] + Probability_of_each_individual[i])
        
        return cumulative_probabilities
        

    def select_parents(self) -> List[List[int]]:
        """
        Select parents based on cumulative probabilities.

        Returns:
            List[List[int]]: Selected parents.
        """
        cumulative_probabilities = self.calculate_cumulative_probabilities()
        selected_parents = random.choices(self.population, cum_weights = cumulative_probabilities, k = 2)
        return selected_parents

    def crossover(self, parent1: List[int], parent2: List[int]) -> tuple[List[int] , List[int]]:
        """
        Perform one-point crossover between two parents.

        Args:
            parent1 (List[int]): First parent chromosome.
            parent2 (List[int]): Second parent chromosome.

        Returns:
            List[List[int]]: Two offspring chromosomes.
        """
        
        position = 2
        new_parent1 = []
        new_parent2 = []
        if random.uniform(0, 1) < self.crossover_prob:
            for i in range(len(parent1)):
                if i < position:
                    new_parent1.append(parent1[i])
                    new_parent2.append(parent2[i])
                else:
                    new_parent1.append(parent2[i])
                    new_parent2.append(parent1[i])
            return new_parent1 , new_parent2
        else:
            return parent1, parent2
    

    def mutate(self, chromosome: List[int]) -> List[int]:
        """
        Apply bit flip mutation to an individual.

        Args:
            chromosome (List[int]): The chromosome to be mutated.

        Returns:
            List[int]: The mutated chromosome.
        """
        mutated_chromosome = chromosome.copy()
        for i in range(self.chromosome_length):
            if random.uniform(0, 1) < self.mutation_rate:
                if mutated_chromosome[i] == 1:
                    mutated_chromosome[i] = 0
                else:
                    mutated_chromosome[i] = 1
        return mutated_chromosome

    def elitism(self) -> List[List[int]]:
        """
        Apply elitism to the population (keep the best two individuals).

        Args:
            new_population (List[List[int]]): The new population after crossover and mutation.
        """
        sorted_population = sorted(self.population, key=self.evaluate_fitness, reverse=True)
        return sorted_population[:2]


    def run(self, max_generations):
        for generation in range(max_generations):
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents()
                offspring1, offspring2 = self.crossover(parent1, parent2)
                offspring1 = self.mutate(offspring1)
                offspring2 = self.mutate(offspring2)
                new_population.extend([offspring1, offspring2])

            new_population = new_population[0:self.population_size-self.elitism_num] # make sure the new_population is the same size of original population - the best individuals we will append next
            best_individuals = self.elitism()
            new_population.extend(best_individuals)
            self.population = new_population


        best_solution = max(self.population, key=self.evaluate_fitness)
        return best_solution

if __name__ == "__main__":
    population_size = 200
    chromosome_length = 40
    crossover_prob = 0.7
    mutation_rate = 0.07
    elitism_num = 2
    max_generations = 150
    start = time.time()
    onemax_ga = OneMaxGA(population_size, chromosome_length,crossover_prob, mutation_rate,elitism_num)

    best_solution = onemax_ga.run(max_generations)
    ga_time = time.time()-start
    print("GA Solution Time:",round(ga_time,1),'Seconds')


    print(f"Best solution: {best_solution}")
    print(f"Fitness: {onemax_ga.evaluate_fitness(best_solution)}")