# test for implemented woa on rastrigin function
import math
import random
import sys
import copy

# ---- fitness function ----
def fitness_fct(position):
    fitness_val = 0.0
    for i in range(len(position)):
        xi = position[i]
        fitness_val += (xi * xi) - (10 * math.cos(2 * math.pi * xi)) + 10
    return fitness_val

# whale class
class Whale:
    def __init__(self, fitness, dim, min_x, max_x, seed):
        self.rnd = random.Random(seed)
        self.position = [0.0 for i in range(dim)]

        for i in range(dim):
            self.position[i] = ((max_x - min_x) * self.rnd.random() + min_x)
        
        self.fitness = fitness(self.position) # current fitness


# WOA implementation
def woa(fitness, max_iter, n, dim, min_x, max_x):
    rnd = random.Random(0)

    # create n random whales
    population = [Whale(fitness=fitness, dim=dim, min_x=min_x, max_x=max_x, seed=i) for i in range(n)]

    # compute the value of best pos and best fitness in the whale population
    x_best = [0.0 for i in range(dim)]
    f_best = sys.float_info.max

    # check each whale
    for i in range(n):
        if population[i].fitness < f_best:
            f_best = population[i].fitness
            x_best = copy.copy(population[i].position)

    # main loop of woa
    iter = 0
    while iter < max_iter:

        # print the best every 10 iterations
        if (iter % 10 == 0 and iter > 1):
            print("Iteration = " + str(iter) + " best fitness = %.3f" % f_best)

        # linear decrease from 2 to 0
        a = 2 * (1 - iter / max_iter)
        a2 = -1 + iter * ((-1) / max_iter)

        for i in range(n):
            A = 2 * a * rnd.random() - a
            C = 2 * rnd.random()
            b = 1
            l = (a2 - 1) * rnd.random() + 1
            p = rnd.random()

            D = [0.0 for i in range(dim)]
            D1 = [0.0 for i in range(dim)]
            X_new = [0.0 for i in range(dim)]
            X_rand = [0.0 for i in range(dim)]

            if p < 0.5:
                if (abs(A) > 1):
                    for j in range(dim):
                        D[j] = abs(C * X_rand[j] - population[i].position[j])
                        X_new[j] = x_best[j] - A * D[j]
                else:
                    p = random.randint(0, n - 1)
                    while (p == 1):
                        p = random.randint(0, n - 1)

                    X_rand = population[p].position

                    for j in range(dim):
                        D[j] = abs(C * X_rand[j] - population[i].position[j])
                        X_new[j] = X_rand[j] - A * D[j]
            else:
                for j in range(dim):
                    D1[j] = abs(x_best[j] - population[i].position[j])
                    X_new[j] = D1[j] * math.exp(b * l) * math.cos(2 * math.pi * l + x_best[j])
            
            for j in range(dim):
                population[i].position[j] = X_new[j]

        for i in range(n):
            # if x_new < min_x or > max the clip it
            for j in range(dim):
                population[i].position[j] = max(population[i].position[j], min_x)
                population[i].position[j] = min(population[i].position[j], max_x)

            population[i].fitness = fitness(population[i].position)

            if (population[i].fitness < f_best):
                x_best = copy.copy(population[i].position)
                f_best = population[i].fitness

        iter += 1
    return x_best


# main for fct
print("\nBegin whale optimization algorithm on rastrigin function\n")
dim = 3
fitness = fitness_fct

print("Goal is to minimize Rastrigin's function in " + str(dim) + " variables")
print("Function has known min = 0.0 at (", end="")
for i in range(dim - 1):
    print("0, ", end="")
print("0)")

num_whales = 50
max_iter = 100

print("Setting num_whales = " + str(num_whales))
print("Setting max_iter    = " + str(max_iter))
print("\nStarting WOA algorithm\n")

best_position = woa(fitness, max_iter, num_whales, dim, -10.0, 10.0)

print("\nWOA completed\n")
print("\nBest solution found:")
print(["%.6f" % best_position[k] for k in range(dim)])
err = fitness(best_position)
print("fitness of best solution = %.6f" % err)

print("\nEnd WOA for rastrigin\n")