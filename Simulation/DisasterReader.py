import json
import random
import numpy as np
from pathlib import Path


def round_sigfig(value, digits):
    if value == 0:
        return 0
    return float(f"{value:.{digits}g}")

class DisasterReader():
    def __init__(self, name, severity=None):
        if severity is None:
            self._severity = random.random()
        disaster_path = Path.cwd() / "Disasters" / f"{name}.json"
        if not disaster_path.exists():
            disaster_path = Path(__file__).resolve().parent.parent / "Disasters" / f"{name}.json"
        with disaster_path.open() as fid:
            data = fid.read()
        disasters = json.loads(data)
        disaster = int(self._severity * len(disasters)) # Pick from disasters based on severity
        self.answers = self._int_keys(disasters[disaster][1])
        self.reports = self._format_reports(disasters[disaster][0])
    
    def set_location(self, location):
        self._location = location
    
    def get_report(self, time_step):
        return self.reports[time_step]
    
    def get_answer_key(self):
        return self.answers
    
    def __len__(self):
        return len(self.reports)
    
    def _format_reports(self, reports):
        formatted_reports = {}
        for key, string in reports.items():
            new_key = int(key)
            start_indices = [i for i, letter in enumerate(string) if letter == '[']
            end_indices = [i for i, letter in enumerate(string) if letter == ']']
            if len(start_indices) != len(end_indices):
                raise ValueError("json not properly formatted: {} {}".format(key, string))
            while start_indices != []:
                substring = string[start_indices[0]:end_indices[0]+1]
                num = self._get_random(substring)
                string = string[:start_indices[0]] + str(num) + string[end_indices[0] + 1:]
                start_indices = [i for i, letter in enumerate(string) if letter == '[']
                end_indices = [i for i, letter in enumerate(string) if letter == ']']
            formatted_reports[new_key] = string
        return formatted_reports
    
    def _int_keys(self, reports):
        formatted_reports = {}
        for key, string in reports.items():
            formatted_reports[int(key)] = string
        return formatted_reports
                
    def _get_random(self, string):
        string = string[1:-1] # Get rid of brackets
        start = float(string.split(",")[0].strip())
        stop = float(string.split(",")[1].strip())
        step = float(string.split(",")[2].strip())
        num = float(random.choice(np.arange(start, stop, step)))
        num = round_sigfig(num, 2)
        if num > 1:
            num = int(num)
        return num
