import abc
import math

class Location(abc.ABC):
    def __init__(self, disaster=None):
        self._disaster = disaster
        self._population = 0
        self._old_pop = 0
    
    @property
    def population(self):
        pass

    @abc.abstractmethod
    def random(self):
        pass
    
    @abc.abstractmethod
    def disaster_probabilities(self):
        """
        Normalized array of probabilities based on enum Disaster.Disasters 
        
        Returns
        -------
        Dictionary of disasters and their respective probabilities

        """
        pass

    @abc.abstractmethod
    def evacuate(self):
        pass

    @abc.abstractmethod
    def reset(self):
        pass
    
    @property
    def large_damage(self):
        pass
    
    @property
    def medium_damage(self):
        pass
    
    @property
    def small_damage(self):
        pass

    @abc.abstractmethod
    def evacuate(self):
        self._population = math.ceil(self._population * 0.5)