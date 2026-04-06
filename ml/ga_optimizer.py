import random
import numpy as np


class MissionOptimizer:
    """
    Simplified Genetic Algorithm Trajectory Optimizer.
    Finds an optimal orbital altitude (km) minimizing a cost function.
    """

    def __init__(self, pop_size=50):
        self.pop_size = pop_size
        self.alt_min = 160.0
        self.alt_max = 8000.0

    def _eval(self, alt):
        """Cost function: Delta-V proxy + environment penalties."""
        cost = abs(alt - 550.0) * 0.001 + 1.0
        if alt < 300:
            cost += 2.0
        if 1000 < alt < 6000:
            cost += 3.0
        return cost

    def run(self):
        """Run genetic algorithm and return (best_altitude, best_cost)."""
        population = [random.uniform(self.alt_min, self.alt_max)
                      for _ in range(self.pop_size)]

        for _generation in range(15):
            # Evaluate
            fitness = [(alt, self._eval(alt)) for alt in population]
            fitness.sort(key=lambda x: x[1])

            # Select top half
            survivors = [f[0] for f in fitness[:self.pop_size // 2]]

            # Reproduce with crossover and mutation
            offspring = []
            while len(offspring) < self.pop_size:
                p1 = random.choice(survivors)
                p2 = random.choice(survivors)
                child = (p1 + p2) / 2.0
                # Mutate
                if random.random() < 0.2:
                    child += random.gauss(0, 100.0)
                child = max(self.alt_min, min(self.alt_max, child))
                offspring.append(child)

            population = offspring

        # Return best individual
        best_alt = min(population, key=self._eval)
        best_cost = self._eval(best_alt)
        return best_alt, best_cost
