# import math
# import random
# import sys
# import copy


# # Compute the best for t = 1; then, keep the best population as the initial one for t = 2
# # and update the relevant variables
# # So pretend for now that the data can be represented as an array
# # fitness= w_1 F_"cost" +w_2 F_"track" +w_3 F_bat+F_"pen"  


# # global variables - to be updated
# w1 = w2 = w3 = 1
# buy_price = 1
# sell_price = 1
# grid_energy = 2
# target_energy = 1
# e_bat = 1
# eff_charge = 1
# eff_discharge = 1
# batt_cost = batt_capacity = 1
# k_slope = 1

# # Get the state of charge for the next time interval
# def getNextSoC(prevSoC, e_bat):
#     nextSoC = 0
#     if (e_bat >= 0):
#         nextSoC = prevSoC + (eff_charge * e_bat)
#     else:
#         nextSoC = prevSoC - (eff_discharge * abs(e_bat))
#     return nextSoC


# # Compute the cost for the current time interval
# def costFct(grid_energy):
#     cost = 0
#     if (grid_energy >= 0):
#         cost = grid_energy * buy_price
#     else:
#         cost = abs(grid_energy) * (sell_price) * (-1)
#     return cost 


# # Compute the tracking component for the current time interval
# def trackFct(grid_energy):
#     track = pow((grid_energy - target_energy), 2)  
#     return track


# # Compute the battery penalty function, based on the current and previous SoC
# def batFct(prevSoC, curSoC):
#     batt = abs(k_slope / 100) * ((prevSoC - curSoC) / batt_capacity) * batt_cost
#     return batt






# def computeFitness():
#     f_cost = costFct(grid_energy)
#     f_track = trackFct(grid_energy)
#     f_bat = batFct(0, 1)
#     f_pen = 0
#     fitness = w1 * f_cost + w2 * f_track + w3 * f_bat + f_pen
#     return fitness

# def simulateSoC():
#     pass  


# # X = {e_i}, i = 1, ..., N
# class Whale:

#     def __init__(self, num_households:int, seed:int):

#         self.rnd = random.Random(seed)
#         # init the transferred energy as an array 
#         self.transf_energy = [0.0 for i in range(num_households)]
#         self.fitness_value = sys.float_info.max

#     def initRandomEnergy(self, num_households, charge_max, discharge_max):

#         # assign random values
#         for i in range(num_households):
#             self.transf_energy[i] = ((charge_max - discharge_max) * self.rnd.random() + discharge_max)
#             # TODO: check if in allowed interval
#             # TODO: simulate SoC and correct initial values

#     def computeFitness(self) -> float:
#         # fitness = 0
#         self.fitness_value = computeFitness()




# def whaleOptimization(population_size: int, num_households:int, charge_max:float, discharge_max:float, max_iter:int):

#     # init random instance
#     rnd_instance = random.Random(0)

#     # Create the population of random whales
#     population:Whale = [None for i in range(population_size)]
#     for i in range(population_size):
#         population[i] = Whale(num_households, i)
#         population[i].initRandomEnergy(num_households, charge_max, discharge_max)
#         # Whale.initRandomEnergy(population[i], num_households, charge_max, discharge_max)


#     # Define and initialize best individual
#     best_whale = Whale(num_households, 0)
#     print(best_whale)

#     # find the best individual in the initial population
#     for i in range(population_size):
#         population[i].computeFitness()
#         if population[i].fitness_value < best_whale.fitness_value:
#             best_whale.fitness_value = population[i].fitness_value
#             best_whale.transf_energy = copy.copy(population[i].transf_energy)

#     curr_iter = 0
#     A = 0.0
#     C = 0.0
#     D = [0.0 for i in range(num_households)]
#     b = 1

#     while curr_iter < max_iter:
        
#         for i in range(population_size):
#             # Initialize parameters
#             l = random.uniform(-1.0, 1.0)
#             p = random.uniform(0.0, 1.0)
#             r_1 = random.uniform(0.0, 1.0)
#             r_2 = random.uniform(0.0, 1.0)
#             a = 2 * (1 - curr_iter / max_iter)
#             A = 2 * a - r_1 * a 
#             C = 2 * r_2
#             new_whale:Whale = Whale(num_households, i)
#             random_whale:Whale = Whale(num_households, i)

#             if (p < 0.5):
#                 if (abs(A) < 1):
#                     for j in range(num_households):
#                         D[j] = C * best_whale.transf_energy[j] - population[i].transf_energy[j]
#                         new_whale.transf_energy[j] = best_whale.transf_energy[j] - A * D[j]
#                 else:
#                     rnd_idx = random.randrange(0, population_size - 1)
#                     random_whale = population[rnd_idx]
#                     for j in range(num_households):
#                         D[j] = C * random_whale.transf_energy[j] - population[i].transf_energy[j]
#                         new_whale.transf_energy[j] = random_whale.transf_energy[j] - A * D[j]
#             else:
#                 for j in range(num_households):
#                     D[j] = best_whale.transf_energy[j] - population[i].transf_energy[j]
#                     new_whale.transf_energy[j] = D[j] * math.pow(math.e, (b + l)) * math.cos(2 * math.pi * l) + best_whale.transf_energy[j]

#         # Update transf_energy for current population
#         for i in range(population_size):
#             for j in range(num_households):
#                 # Limit the transf_energy in the allowed interval
#                 new_whale.transf_energy[j] = max(discharge_max, new_whale.transf_energy[j])
#                 new_whale.transf_energy[j] = min(charge_max, new_whale.transf_energy[j])
#                 population[i].transf_energy[j] = new_whale.transf_energy[j]

#             population[i].computeFitness()
#             if (population[i].fitness_value < best_whale.fitness_value):
#                 best_whale.fitness_value = population[i].fitness_value
#                 best_whale.transf_energy = copy.copy(population[i].transf_energy)
#         curr_iter += 1

#     return best_whale



            

# # # linear decrease from 2 to 0
# # a = 2 * (1 - iter / max_iter)
# # a2 = -1 + iter * ((-1) / max_iter)

# if __name__ == "__main__":
#     best = whaleOptimization(10, 5, 10, -10, 100)
#     print(best)

  