from Simulation.DisasterReader import DisasterReader
import unittest
import os
import re

class TestDisasterReader(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     os.chdir('..\..') #Disable for travis (needed for local run)
    
    # @classmethod
    # def tearDownClass(cls):
    #     os.chdir('Test\Disasters')
    
    def test_can_read_files(self):
        raised = False
        severities = [.01,.35,.70]
        try:
            for file in os.listdir("Disasters"):
                for severity in severities:
                    reader = DisasterReader(file[:-5])
                    for i in range(len(reader)):
                        reader.get_report(i)
                    reader.get_answer_key()
        except:
            raised = True
        self.assertFalse(raised)
    
                    
if __name__ == '__main__':
    unittest.main()