import abc
from numpy.random import choice
import math

class SouthWest(abc.ABC):
    def __init__(self, date=None, population=100000):
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
            "hurricane": .4,
            "earthquake": .4,
            "tornado": 0,
            "pandemic": .1,
            "wildfire": .1
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
        return ["300 miles southwest of the coastline, projected to land due south of town", "NorthEast in the Pacific Ocean", "approaching the coast of Baja California", "hits the coastline 100 miles south of town", "inland", "away from town"]
    
    @property
    def close_hurricane_progression(self):
        return ["200 miles southwest of the coastline, projected to make contact near town", "NorthEast in the Pacific Ocean", "approaching the coast due 10 miles South of town", "rapidly approaches the city", "making landfall within 10 miles of city limits"]
    
    
    