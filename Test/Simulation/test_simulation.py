from Simulation.Simulation import Simulation
import unittest
import os

class TestSimulation(unittest.TestCase):
    # def setUp(self):
    #     os.chdir('..\..')
    
    # def tearDown(self):
    #     os.chdir('Test/Simulation')
    
    def test_location(self):
        sim = Simulation()
        data = {'population':1000}
        sim.set_location('midwest',data)
        self.assertEqual('midwest', sim.location)
    
    def test_disaster(self):
        sim = Simulation()
        sim.set_disaster('earthquake')
        data = {'population':1000}
        sim.set_location('midwest',data)
        sim.get_report()
        self.assertEqual('earthquake', sim.disaster)
        
    def test_stores_action(self):
        sim = Simulation()
        sim.set_disaster('hurricane')
        sim.take_action('apply_for_federal_aid')
        sim.time_step()
        sim.take_action('declare_emergency')
        self.assertEqual({'apply_for_federal_aid': [0], 'declare_emergency': [1]}, sim.actions())


if __name__ == '__main__':
    unittest.main()