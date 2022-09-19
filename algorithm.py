
# multithread algorithm showing how the four stages of algorithm works

from __future__ import annotations

import random


# maximum size of population, the bigger could be faster but more memory demanding
N_POPULATION = 200

"""
    Number of elements selected in every generation for evolution the selection takes
    place from the best to the worst of that generation must be smaller than N_POPULATION
"""
N_SELECTED = 50

"""
    Probability that an element of a generation can mutate changing one of its genes this
    guarantees that all genes will be used during evolution
"""
MUTATION_PROBABILITY = 0.4

