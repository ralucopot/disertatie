import math
import random
import sys
import copy
import matplotlib.pyplot as plt

class Whale:

    def __init__(self, num_households, charge_max, discharge_max, currentSoC, seed):
        self.ch_max = charge_max
        self.dis_max = discharge_max
        self.transf_energy = [0.0 for i in range(num_households)]
        self.fitness_fct = None
        self.fitness_value = sys.float_info.max
        self.SoC = list(currentSoC)
        self.rnd = random.Random(seed)

    def __str__(self):
        msg = f"Transfer energy array: {self.transf_energy} and fitness value: {self.fitness_value}"
        return msg

    def initRandomEnergy(self, num_households, charge_max, discharge_max):
        # assign random values
        rnd_instance = random.Random(0)
        for i in range(num_households):
            self.transf_energy[i] = ((charge_max - discharge_max) * self.rnd.random() + discharge_max)
            # if self.transf_energy[i] > charge_max:
            #     self.transf_energy[i] = charge_max
            # elif self.transf_energy[i] < discharge_max:
            #     self.transf_energy[i] = discharge_max



    def initWithZero(self, num_households):
        for i in range(num_households):
            self.transf_energy[i] = 0

    def checkTransfEnergy_option1(self, num_households):
        # 10 <= SoC <= 95; eff charge = 0.9
        # Option 1: set to 0
        for i in range(num_households):
            newSoC = 0
            if self.transf_energy[i] > 0:
                newSoC = self.SoC[i] + 0.9 * self.transf_energy[i]
                if newSoC > 95:
                    self.transf_energy[i] = 0
                else:
                    self.SoC[i] = newSoC
            elif self.transf_energy[i] < 0:
                newSoC = self.SoC[i] - 0.9 * abs(self.transf_energy[i])
                if newSoC < 10:
                    self.transf_energy[i] = 0
                else:
                    self.SoC[i] = newSoC


    def checkTransfEnergy_option2(self, num_households):
        # 10 <= SoC <= 95; eff charge = 0.9
        # Option 2: limit the SoC to the maximum/minimum allowed value
        for i in range(num_households):
            newSoC = 0
            if self.transf_energy[i] > 0:
                newSoC = self.SoC[i] + 0.9 * self.transf_energy[i]
                if newSoC > 95:
                    self.transf_energy[i] -= (newSoC - 95) / 0.9
                    self.SoC[i] = 95
                else:
                    self.SoC[i] = newSoC
            elif self.transf_energy[i] < 0:
                newSoC = self.SoC[i] - 0.9 * abs(self.transf_energy[i])
                if newSoC < 10:
                    self.transf_energy[i] += (10 - newSoC) / 0.9
                    self.SoC[i] = 10
                else:
                    self.SoC[i] = newSoC



class WOA:
    def __init__(self, num_iter, charge_max, discharge_max, fitnessFct = None):
        self.num_iter = num_iter
        self.charge_max = charge_max
        self.discharge_max = discharge_max
        self.fitnessFct = fitnessFct
        self.currentTime = 0


    def computeFitness(self, whale:Whale):
        fitVal = self.fitnessFct(whale.transf_energy)
        whale.fitness_value = fitVal

    

    def computeBest(self, population_size: int, num_households:int, charge_max:float, discharge_max:float, max_iter:int, currentSoC:list):

        # init random instance
        

        # Create the population of random whales
        population:Whale = [None for i in range(population_size)]
        for i in range(population_size):
            population[i] = Whale(num_households, charge_max, discharge_max, currentSoC, i)
            population[i].initRandomEnergy(num_households, charge_max, discharge_max)
            population[i].checkTransfEnergy_option2(num_households)
            # if isFirstRun:
            #     population[i].initWithZero(num_households)
            # else:
            #     # get values from previous run
            #     pass
            # Whale.initRandomEnergy(population[i], num_households, charge_max, discharge_max)


        # Define and initialize best individual
        best_whale = Whale(num_households, charge_max, discharge_max, currentSoC, 0)
        # print(best_whale)

        # find the best individual in the initial population
        for i in range(population_size):
            self.computeFitness(population[i])
            if population[i].fitness_value < best_whale.fitness_value:
                best_whale.fitness_value = population[i].fitness_value
                best_whale.transf_energy = copy.copy(population[i].transf_energy)

        curr_iter = 0
        A = 0.0
        C = 0.0
        D = [0.0 for i in range(num_households)]
        b = 1

        allFitness = []

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
                new_whale:Whale = Whale(num_households, charge_max, discharge_max, currentSoC, 0)
                # new_whale.checkTransfEnergy_option2(num_households)
                random_whale:Whale = Whale(num_households, charge_max, discharge_max, currentSoC, 0)
                random_whale.checkTransfEnergy_option2(num_households)

                if (p < 0.5):
                    if (abs(A) < 1):
                        for j in range(num_households):
                            D[j] = C * best_whale.transf_energy[j] - population[i].transf_energy[j]
                            new_whale.transf_energy[j] = best_whale.transf_energy[j] - A * D[j]
                    else:
                        rnd_idx = random.randrange(0, population_size - 1)
                        random_whale = copy.deepcopy(population[rnd_idx]) 
                        for j in range(num_households):
                            D[j] = C * random_whale.transf_energy[j] - population[i].transf_energy[j]
                            new_whale.transf_energy[j] = random_whale.transf_energy[j] - A * D[j]
                else:
                    for j in range(num_households):
                        D[j] = best_whale.transf_energy[j] - population[i].transf_energy[j]
                        new_whale.transf_energy[j] = D[j] * math.pow(math.e, (b + l)) * math.cos(2 * math.pi * l) + best_whale.transf_energy[j]

                new_whale.checkTransfEnergy_option2(num_households)
                population[i].transf_energy = list(new_whale.transf_energy)


            # Update transf_energy for current population 
            for i in range(population_size):
                # for j in range(num_households):
                    # Limit the transf_energy in the allowed interval
                    # new_whale.transf_energy[j] = max(discharge_max, new_whale.transf_energy[j])
                    # new_whale.transf_energy[j] = min(charge_max, new_whale.transf_energy[j])
                    # new_whale.checkTransfEnergy_option2(num_households)
                    # population[i].transf_energy[j] = new_whale.transf_energy[j]

                self.computeFitness(population[i])
                if (population[i].fitness_value < best_whale.fitness_value):
                    best_whale.fitness_value = population[i].fitness_value
                    best_whale.transf_energy = copy.copy(population[i].transf_energy)

            allFitness.append(best_whale.fitness_value)
            
            curr_iter += 1
        plt.figure(figsize=(8, 5))
        plt.plot(allFitness, color="red", marker='o')
        plt.title("Basic Array Plot")
        plt.xlabel("time")
        plt.ylabel("fitness value")
        plt.grid(True, alpha=0.3)
        plt.savefig(f"fitness_time_{self.currentTime}")
        self.currentTime += 1

        return best_whale