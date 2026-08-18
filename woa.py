import math
import random
import sys
import copy
import matplotlib.pyplot as plt



def generateNewValue(SoC, initSoC, energyTrans, minSoC, maxSoC, currentBatt, battCapacity):
        newSoC = SoC
        energy = energyTrans
        max = battCapacity - currentBatt
        min = -currentBatt
        # newBatt = currentBatt + energy
        while newSoC > 95 or newSoC < 10:
            if int(min) >= int(max):
                return (initSoC, 0)
            energy = random.randrange(int(min), int(max))
            # energy = checkBattery(currentBatt, battCapacity, energy)
            # newBatt = currentBatt + energy
            if energy > 0:
                newSoC = initSoC + 0.9 * energy
                newMax = max - (newSoC - 95) / 0.9
                if newMax < max:
                    max = newMax
                # max -= (newSoC - 95) / 0.9
            elif energy < 0:
                newSoC = initSoC - 0.9 * abs(energy)
                newMin = min + (10 - newSoC) / 0.9
                if newMin > min:
                    min = newMin
            else:
                return (initSoC, energy)
                # min += (10 - newSoC) / 0.9
        return (newSoC, energy)


def checkBattery(currentBatt, battCapacity, energyTrans, oldSoC):
    energy = energyTrans
    newBatt = currentBatt + energy
    newSoC = 0
    if newBatt > (battCapacity * 0.95) or newBatt < (battCapacity * 0.01):
        if energy == 0:
            return (energy, oldSoC)
        elif energy > 0:
            newBatt = battCapacity * 0.95
            newSoC = 95
        else:
            newBatt = battCapacity * 0.01  
            newSoC = 10           
        energy = newBatt - currentBatt
    return (energy, newSoC)



class Whale:

    def __init__(self, num_households, charge_max, discharge_max, currentSoC, seed):
        self.ch_max = charge_max
        self.dis_max = discharge_max
        self.transf_energy = [0.0 for i in range(num_households)]
        self.fitness_fct = None
        self.fitness_value = sys.float_info.max
        self.SoC = list(currentSoC)
        self.rnd = random.Random(seed)
        self.cost = [0.0 for i in range(num_households)]

    def __str__(self):
        msg = f"Transfer energy array: {self.transf_energy} and fitness value: {self.fitness_value}"
        return msg

    def initRandomEnergy(self, num_households, charge_max, discharge_max):
        # assign random values
        rnd_instance = random.Random(0)
        for i in range(num_households):
            self.transf_energy[i] = ((charge_max[i] - discharge_max[i]) * self.rnd.random() + discharge_max[i])





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

    



    def checkTransfEnergy_option3(self, num_households, currentBatt, battCapacity):
        # 10 <= SoC <= 95; eff charge = 0.9
        # Option 2: limit the SoC to the maximum/minimum allowed value
        for i in range(num_households):
            newSoC = 0
            newBatt = currentBatt[i] + self.transf_energy[i] 
            if self.transf_energy[i] > 0:
                newSoC = self.SoC[i] + 0.9 * self.transf_energy[i]
                if newSoC > 95 or newBatt > (0.95 * battCapacity[i]):
                    (self.SoC[i], self.transf_energy[i]) = generateNewValue(newSoC, self.SoC[i], self.transf_energy[i], self.ch_max, self.dis_max, currentBatt[i], battCapacity[i])

                else:
                    self.SoC[i] = newSoC
            elif self.transf_energy[i] < 0:
                newSoC = self.SoC[i] - 0.9 * abs(self.transf_energy[i])
                if newSoC < 10 or newBatt < (0.01 * battCapacity[i]):
                    (self.SoC[i], self.transf_energy[i]) = generateNewValue(newSoC, self.SoC[i], self.transf_energy[i], self.ch_max, self.dis_max, currentBatt[i], battCapacity[i])
                else:
                    self.SoC[i] = newSoC
        
        # for i in range(num_households):

    def checkTransfEnergy_option4(self, num_households, currentBatt):
        for i in range(num_households):
            curr_max_discharge = self.dis_max[i] - currentBatt[i] 
            curr_max_charge = self.ch_max[i] - currentBatt[i]
            newBattLevel = currentBatt[i] + self.transf_energy[i]
            isValueChanged = False
            while (newBattLevel > self.ch_max[i]) or (newBattLevel < self.dis_max[i]):
                isValueChanged = True
                newTransf = random.uniform(curr_max_discharge, curr_max_charge)
                newBattLevel = currentBatt[i] + newTransf

            if not isValueChanged:
                continue
            if newTransf == 0:
                self.transf_energy[i] = 0
                continue
            if (newTransf > 0):
                newSoC = self.SoC[i] + 0.9 * newTransf
            elif newTransf < 0:
                newSoC = self.SoC[i] - 0.9 * abs(newTransf)
            self.SoC[i] = newSoC
            self.transf_energy[i] = newTransf

                






class WOA:
    def __init__(self, num_iter, maxSoC, minSoC, fitnessFct = None):
        self.num_iter = num_iter
        self.maxSoC = maxSoC
        self.minSoC = minSoC
        self.fitnessFct = fitnessFct
        self.currentTime = 0
        self.cost = 0


    def computeFitness(self, whale:Whale):
        fitVal = self.fitnessFct(whale.transf_energy)
        whale.fitness_value = fitVal

    

    def computeBest(self, population_size: int, num_households:int, maxSoC:float, minSoC:float, max_iter:int, currentSoC:list, currentBatt:list, battCapacity:list):

        # init random instance
        f = open("initEnergy.txt", "w")
        tolerance = 1e-5

        # Create the population of random whales
        population:Whale = [None for i in range(population_size)]
        charge_max = []
        discharge_max = []
        for i in range(num_households):
            charge_max_i = (maxSoC * battCapacity[i]) / 100
            discharge_max_i = (minSoC * battCapacity[i]) / 100
            charge_max.append(charge_max_i)
            discharge_max.append(discharge_max_i)

        for i in range(population_size):
            population[i] = Whale(num_households, charge_max, discharge_max, currentSoC, i)
            population[i].initRandomEnergy(num_households, charge_max, discharge_max)
            # population[i].checkTransfEnergy_option3(num_households, currentBatt, battCapacity)
            population[i].checkTransfEnergy_option4(num_households, currentBatt)
            print("Initial energy\n", file=f)
            print(population[i].transf_energy,file=f)
            

        f.close()
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

        old_fitness = 0
        same_fitness_num_iter = 300
        num_repeats = same_fitness_num_iter

        while curr_iter < max_iter:

            old_fitness = best_whale.fitness_value
            
            for i in range(population_size):
                # Initialize parameters
                l = random.uniform(-1.0, 1.0)
                p = random.uniform(0.0, 1.0)
                r_1 = random.uniform(0.0, 1.0)
                r_2 = random.uniform(0.0, 1.0)
                # a = 2 * (1 - curr_iter / max_iter) #linear
                a = 2 * (1 - (curr_iter / max_iter)**2) #quadratic
                # a = 2 * np.exp(-3 * (curr_iter / max_iter)) # exponential decay
                A = 2 * a - r_1 * a 
                C = 2 * r_2
                new_whale:Whale = Whale(num_households, charge_max, discharge_max, currentSoC, 0)
                random_whale:Whale = Whale(num_households, charge_max, discharge_max, currentSoC, 0)

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

                new_whale.checkTransfEnergy_option4(num_households, currentBatt)

                population[i].transf_energy = list(new_whale.transf_energy)


            # Update transf_energy for current population 
            for i in range(population_size):
                for j in range(num_households):
                    if (population[i].transf_energy[j] + currentBatt[j] > (battCapacity[j] * maxSoC / 100) or 
                        population[i].transf_energy[j] + currentBatt[j] < (battCapacity[j] * minSoC / 100)):
                        raise Exception("Violated battery constrains")
                self.computeFitness(population[i])
                if (population[i].fitness_value < best_whale.fitness_value):
                    best_whale.fitness_value = population[i].fitness_value
                    best_whale.transf_energy = copy.copy(population[i].transf_energy)

            allFitness.append(best_whale.fitness_value)

            errorFactor = abs(best_whale.fitness_value) - abs(old_fitness)
            if abs(errorFactor) < 1e-20:
                num_repeats -= 1
                if num_repeats == 0:
                    break
            else:
                num_repeats = same_fitness_num_iter


            # if abs(abs(best_whale.fitness_value) - abs(old_fitness)) < 1e-100 and curr_iter > 100:
                # break
            
            curr_iter += 1
        plt.figure(figsize=(8, 5))
        plt.plot(allFitness, color="red", marker='o')
        plt.title(f"Fitness at time {self.currentTime}")
        plt.xlabel("time")
        plt.ylabel("fitness value")
        plt.grid(True, alpha=0.3)
        plt.savefig(f"fitness_time_{self.currentTime}")
        self.currentTime += 1

        return best_whale