from Simulation.DisasterReader import DisasterReader
import unittest
import os
import re

class TestDisasterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # os.chdir('..\..') #Disable for travis (needed for local run)
        cls.reports = {
            "0": ["Test read with no special instances."],
            "1": ["Test read with ", " one special instance"],
            "2": ["Test at the end of the string "],
            "3": ["Test 14 ", " is returned"],
            "4": ["Test ", " sigfigs"],
            "5": ["Test ", " multiple "," specials "],
            "6": ["Blank test"],
            "7": ["Blank test"],
            "8": ["Blank test"],
            "9": ["Blank test"]
        }
        cls.ranges = {
            "0": [],
            "1": [1, 4, 2],
            "2": [.2, .4, .01],
            "3": [14, 15, 1],
            "4": [10, 20, .01],
            "5": [1, 10, .5, 1, 10, .5, 1, 10, .5],
            "6": [],
            "7": [],
            "8": [],
            "9": []
        }
        cls.answers = {
            "0": "wait",
            "1": "wait",
            "2": "wait",
            "3": "wait",
            "4": "wait",
            "5": "wait",
            "6": "wait",
            "7": "wait",
            "8": "wait",
            "9": "wait"
        }
        cls.file = 'test'
        os.chdir('Test') # So that test .json file is discovered (instead of top-level files)
        cls.disaster_reader = DisasterReader(cls.file)
    
    @classmethod
    def tearDownClass(cls):
        os.chdir('..')
    
    def test_runs(self):
        raised = False
        try:
            for i in range(len(TestDisasterReader.reports)):
                TestDisasterReader.disaster_reader.get_report(i)
        except:
            raised = True
        self.assertFalse(raised)
    
    def test_basic(self):
        string = TestDisasterReader.disaster_reader.get_report(0)
        self.assertEqual(string, TestDisasterReader.reports["0"][0])
    
    def test_contains_no_bracket_string(self):
        for i in range(len(TestDisasterReader.reports)):
            test = TestDisasterReader.disaster_reader.get_report(i)
            for actual in TestDisasterReader.reports[str(i)]:
                self.assertTrue(actual in test)
    
    def test_num_in_ranges(self):
        for i in range(len(TestDisasterReader.reports)):
            test_string = TestDisasterReader.disaster_reader.get_report(i)
            actuals = TestDisasterReader.reports[str(i)]
            ranges = TestDisasterReader.ranges[str(i)]
            for split_num in range(len(actuals) - 1):
                num = float(test_string.split(actuals[split_num])[1].split(actuals[split_num + 1])[0])
                self.assertTrue(num >= ranges[split_num*3])
                self.assertTrue(num <= ranges[split_num*3 + 1])
                    
if __name__ == '__main__':
    unittest.main()