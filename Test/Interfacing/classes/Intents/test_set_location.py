from Simulation.Simulation import Simulation
from interfacing.classes.Intents.SetLocation import NorthEast, SouthEast, MidWest, SouthWest
import unittest

class TestSetLocation(unittest.TestCase):
        
    def test_set_northeast(self):
        sim = Simulation()
        loc = NorthEast()
        data = {'population': 1000}
        loc(sim=sim, data=data)
        self.assertEqual(sim.location, "northeast")

    def test_set_southeast(self):
        sim = Simulation()
        loc = SouthEast()
        data = {'population': 1000}
        loc(sim=sim, data=data)
        self.assertEqual(sim.location, "southeast")

    def test_set_midwest(self):
        sim = Simulation()
        loc = MidWest()
        data = {'population': 1000}
        loc(sim=sim, data=data)
        self.assertEqual(sim.location, "midwest")

    def test_set_southwest(self):
        sim = Simulation()
        loc = SouthWest()
        data = {'population': 1000}
        loc(sim=sim, data=data)
        self.assertEqual(sim.location, "southwest")
        
    
if __name__ == '__main__':
    unittest.main()