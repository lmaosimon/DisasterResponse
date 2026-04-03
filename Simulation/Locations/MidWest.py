import abc
from numpy.random import choice
import math

class MidWest(abc.ABC):
    def __init__(self, date=None, population=10000):
        self._date = date
        self._population = population
        self._old_pop = population
        self._evacuated = False
    
    @property
    def population(self):
        return self._population

    def random(self):
        candidates = [key for key in self.disaster_probabilities()]
        probs = [self.disaster_probabilities()[key] for key in candidates]
        return choice(candidates, 1, p=probs)
    
    def disaster_probabilities(self):
        return {
            "hurricane": 0,
            "earthquake": .05,
            "tornado": .8,
            "pandemic": .1,
            "wildfire": .05
        }

    def evacuate(self):
        if not self._evacuated:
            self._old_pop = self._population
            self._population = math.ceil(self._population * 0.5)
            self._evacuated = True

    def reset(self):
        self._population = self._old_pop
        self._evacuated = False
    
    @property
    def large_damage(self):
        return 1500000
    
    @property
    def medium_damage(self):
        return 750000
    
    @property
    def small_damage(self):
        return 300000