import abc
from numpy.random import choice
import math

class SouthEast(abc.ABC):
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
            "hurricane": .5,
            "earthquake": .2,
            "tornado": 0,
            "pandemic": .3,
            "wildfire": 0
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
        return 1000000
    
    @property
    def medium_damage(self):
        return 500000
    
    @property
    def small_damage(self):
        return 100000
    
    @property
    def distant_hurricane_progression(self):
        return ["off the coast of Northern Africa", "Northwest in the North ATL Ocean", "nearing the northeastern Caribbean Sea", "approaches Puerto Rico", "heading northwest towards eastern Florida.", "heading northeast out into the Atlantic."]
    
    @property
    def close_hurricane_progression(self):
        return ["off the coast of Northern Africa", "Northwest in the North ATL Ocean", "nearing the northeastern Carribean Sea", "approaches Florida", "making landfall in south Florida"]
    
    