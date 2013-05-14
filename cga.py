# "THE BEER-WARE LICENSE" (Revision 42):
# <cmte.igor.almeida@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.

__author__ = 'igor'

from random import random


class Solution(object):
    """
    A solution for the given problem, it is composed of a binary value and its fitness value
    """
    def __init__(self, value):
        self.value = value
        self.fitness = 0

    def calculate_fitness(self, fitness_function):
        self.fitness = fitness_function(self.value)


def generate_candidate(vector):
    """
    Generates a new candidate solution based on the probability vector
    """
    value = ""

    for p in vector:
        value += "1" if random() < p else "0"

    return Solution(value)


def generate_vector(size):
    """
    Initializes a probability vector with given size
    """
    return [0.5] * size


def compete(a, b):
    """
    Returns a tuple with the winner solution
    """
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
    # this is the probability for each solution bit be 1
    vector = generate_vector(size)
    best = None

    # I stop by the number of generations but you can define any stop param
    for i in xrange(generations):
        # generate two candidate solutions, it is like the selection on a conventional GA
        s1 = generate_candidate(vector)
        s2 = generate_candidate(vector)

        # calculate fitness for each
        s1.calculate_fitness(fitness_function)
        s2.calculate_fitness(fitness_function)

        # let them compete, so we can know who is the best of the pair
        winner, loser = compete(s1, s2)

        if best:
            if winner.fitness > best.fitness:
                best = winner
        else:
            best = winner

        # updates the probability vector based on the success of each bit
        update_vector(vector, winner.value, loser.value, population_size)

        print "generation: %d best value: %s best fitness: %f" % (i + 1, best.value, float(best.fitness))




if __name__ == '__main__':
    f = lambda x: int(x, 2)
    run(1000, 32, 10, f)