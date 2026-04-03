from Simulation.Simulation import Simulation
from interfacing.classes.Intents.SetDisaster import Earthquake, Pandemic, Tornado, Hurricane, Wildfire
import unittest
import os

class TestSetDisaster(unittest.TestCase):
    # Basically, running this locally puts it in a bad directory
    # But fixing it locally will break Travis CI on github
    # ---------- UNCOMMENT FOR LOCAL TESTING --------#
    # def setUp(self):
    #     os.chdir('..\..\..\..')
    
    # def tearDown(self):
    #     os.chdir('Test/Interfacing/classes/intents')
    
    def test_set_earthquake(self):
        sim = Simulation()
        dis = Earthquake()
        dis(sim=sim)
        self.assertEqual(sim.disaster, "earthquake")
        
    
if __name__ == '__main__':
    unittest.main()
