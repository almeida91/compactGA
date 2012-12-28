__author__ = 'igor'

from random import random

class Solution(object):
    def __init__(self, value):
        self.value = value
        self.fitness = 0

    def calculate_fitness(self, fitness_function):
        self.fitness = fitness_function(self.value)

def generate_candidate(vector):
    value = ""

    for p in vector:
        value += "1" if random() < p else "0"

    return Solution(value)

def generate_vector(size):
    return [0.5] * size

def compete(a, b):
    if a.fitness > b.fitness:
        return a, b
    else:
        return b, a

def update_vector(vector, winner, loser, population_size):
    for i in xrange(len(vector)):
        if winner[i] != loser[i]:
            if winner[i] == '1':
                vector[i] += 1.0 / float(population_size)
            else:
                vector[i] -= 1.0 / float(population_size)

def run(generations, size, population_size, fitness_function):
    vector = generate_vector(size)
    best = None

    for i in xrange(generations):
        s1 = generate_candidate(vector)
        s2 = generate_candidate(vector)

        s1.calculate_fitness(fitness_function)
        s2.calculate_fitness(fitness_function)

        winner, loser = compete(s1, s2)

        if best:
            if winner.fitness > best.fitness:
                best = winner
        else:
            best = winner

        update_vector(vector, winner.value, loser.value, population_size)

        print "generation: %d best value: %s best fitness: %f" % (i, best.value, float(best.fitness))


if __name__ == '__main__':
    f = lambda x: int(x, 2)
    run(100, 8, 100, f)