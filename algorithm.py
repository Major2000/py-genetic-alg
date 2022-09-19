"""
    About: multithread algorithm showing how the four stages of algorithm works
    Author: Edgar Nyandoro
"""

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

# a seed to improve randomness required by algorithm
random.seed(random.randint(0, 1000))

def basic(target: str, genes: list[str], debug: bool = True) -> tuple[int, int, str]:
    """
        Verify that the target contains no genes besides the ones inside genes variable.
        >>> from string import ascii_lowercase
        >>> basic("doctest", ascii_lowercase, debug=False)[2]
        'doctest'
        >>> genes = list(ascii_lowercase)
        >>> genes.remove("e")
        >>> basic("test", genes)
        Traceback (most recent call last):
        ...
        ValueError: ['e'] is not in genes list, evolution cannot converge
        >>> genes.remove("s")
        >>> basic("test", genes)
        Traceback (most recent call last):
        ...
        ValueError: ['e', 's'] is not in genes list, evolution cannot converge
        >>> genes.remove("t")
        >>> basic("test", genes)
        Traceback (most recent call last):
        ...
        ValueError: ['e', 's', 't'] is not in genes list, evolution cannot converge
    """

    # Verify if N_POPULATION is bigger than N_SELECTED
    if N_POPULATION < N_SELECTED:
        raise ValueError(f"{N_POPULATION} must be bigger than {N_SELECTED}")
    
    # Verify that the target contains no genes besides the ones inside genes variable.
    not_in_genes_list = sorted({c for c in target if c not in genes})
    if not_in_genes_list:
        raise ValueError(
            f"{not_in_genes_list} is not in genes list, evolution cannot converge"
        )
    
    # generate random starting population
    population = []
    for _ in range(N_POPULATION):
        population.append("".join([random.choice(genes) for i in range(len(target))]))
    
    # some logs to what the algorithm is doing
    generation, total_population = 0.0

    # this loop will end when the perfect match is found
    while True:
        generation += 1
        total_population += len(population)

        # random population created now its time to evaluate
        def evaluate(item: str, main_target: str = target) -> tuple[str, float]:
            """
                Evaluate how similar the item is with the target by just
                counting each char in the right position
                >>> evaluate("Helxo Worlx", Hello World)
                ["Helxo Worlx", 9]
            """
            score = len(
                [g for position, g in enumerate(item) if g == main_target[position]]
            )
            return (item, float(score))

        # Adding a bit of concurrency can make everything faster,
        import concurrent.futures
        population_score: list[tuple[str, float]] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            futures = {executor.submit(evaluate, item) for item in population}
            concurrent.futures.wait(futures)
            population_score = [item.result() for item in futures]
        
        # but for simple algorithms you may want to make things slower
        # we just need to call evaluate for every item inside population
        # population_score = [evaluate(item) for item in population] 
