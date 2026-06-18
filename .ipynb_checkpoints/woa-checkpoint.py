import math
import random
import sys
import copy

class Whale:

    def __init__(self, population_size, num_households, charge_max, discharge_max,):
        self.num_whale = population_size
        self.ch_max = charge_max
        self.dis_max = discharge_max
        self.transf_energy = [0.0 for i in range(num_households)]
        self.fitness_value = sys.float_info.max

    def initRandomEnergy(self, num_households, charge_max, discharge_max):

        # assign random values
        for i in range(num_households):
            self.transf_energy[i] = ((charge_max - discharge_max) * self.rnd.random() + discharge_max)


class WOA:
    def __init__(self, num_iter, charge_max, discharge_max, fitnessFct):
        self.num_iter = num_iter
        self.charge_max = charge_max
        self.discharge_max = discharge_max
        self.fitnessFct = fitnessFct

    def computeBest(self, population_size: int, num_households:int, charge_max:float, discharge_max:float, max_iter:int):

        # init random instance
        rnd_instance = random.Random(0)

        # Create the population of random whales
        population:Whale = [None for i in range(population_size)]
        for i in range(population_size):
            population[i] = Whale(num_households, i)
            population[i].initRandomEnergy(num_households, charge_max, discharge_max)
            # Whale.initRandomEnergy(population[i], num_households, charge_max, discharge_max)


        # Define and initialize best individual
        best_whale = Whale(num_households, 0)
        print(best_whale)

        # find the best individual in the initial population
        for i in range(population_size):
            population[i].computeFitness()
            if population[i].fitness_value < best_whale.fitness_value:
                best_whale.fitness_value = population[i].fitness_value
                best_whale.transf_energy = copy.copy(population[i].transf_energy)

        curr_iter = 0
        A = 0.0
        C = 0.0
        D = [0.0 for i in range(num_households)]
        b = 1

        while curr_iter < max_iter:
            
            for i in range(population_size):
                # Initialize parameters
                l = random.uniform(-1.0, 1.0)
                p = random.uniform(0.0, 1.0)
                r_1 = random.uniform(0.0, 1.0)
                r_2 = random.uniform(0.0, 1.0)
                a = 2 * (1 - curr_iter / max_iter)
                A = 2 * a - r_1 * a 
                C = 2 * r_2
                new_whale:Whale = Whale(num_households, i)
                random_whale:Whale = Whale(num_households, i)

                if (p < 0.5):
                    if (abs(A) < 1):
                        for j in range(num_households):
                            D[j] = C * best_whale.transf_energy[j] - population[i].transf_energy[j]
                            new_whale.transf_energy[j] = best_whale.transf_energy[j] - A * D[j]
                    else:
                        rnd_idx = random.randrange(0, population_size - 1)
                        random_whale = population[rnd_idx]
                        for j in range(num_households):
                            D[j] = C * random_whale.transf_energy[j] - population[i].transf_energy[j]
                            new_whale.transf_energy[j] = random_whale.transf_energy[j] - A * D[j]
                else:
                    for j in range(num_households):
                        D[j] = best_whale.transf_energy[j] - population[i].transf_energy[j]
                        new_whale.transf_energy[j] = D[j] * math.pow(math.e, (b + l)) * math.cos(2 * math.pi * l) + best_whale.transf_energy[j]

            # Update transf_energy for current population
            for i in range(population_size):
                for j in range(num_households):
                    # Limit the transf_energy in the allowed interval
                    new_whale.transf_energy[j] = max(discharge_max, new_whale.transf_energy[j])
                    new_whale.transf_energy[j] = min(charge_max, new_whale.transf_energy[j])
                    population[i].transf_energy[j] = new_whale.transf_energy[j]

                population[i].computeFitness()
                if (population[i].fitness_value < best_whale.fitness_value):
                    best_whale.fitness_value = population[i].fitness_value
                    best_whale.transf_energy = copy.copy(population[i].transf_energy)
            curr_iter += 1

        return best_whale