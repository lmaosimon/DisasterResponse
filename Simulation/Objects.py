from Simulation.Locations.SouthWest import SouthWest
from Simulation.Locations.SouthEast import SouthEast
from Simulation.Locations.NorthEast import NorthEast
from Simulation.Locations.MidWest import MidWest
from enum import Enum

        
class Locations(Enum):
    southwest = SouthWest
    southeast = SouthEast
    northeast = NorthEast
    midwest = MidWest


