from Simulation.Objects import Locations
from Simulation.DisasterReader import DisasterReader
from interfacing.classes.Search import Search

import random
import os

class Simulation():
    """
    Example code:
        sim = Simulation()
        sim.disaster = 'hurricane'
        sim.location = 'southeast'
        
    """
    
    def __init__(self):
        """
        Starts a simulation.

        """
        self._location_name = None
        self._disaster_name = None
        self._disaster = None
        self._location = None
        self._last_score = None
        self._reports = {}
        self.actions_taken = []
        self.current_time_step = 0
        self.last_seed = random.random()
        random.seed(self.last_seed)
        
    def take_action(self, action, *args, **kwargs):
        self.actions_taken.append(action)
    
    def time_step(self):
        self.current_time_step += 1
    
    def is_complete(self):
        if self._disaster is None:
            return False
        else:
            return self.current_time_step >= len(self._disaster)
    
    def get_feedback(self):
        if not self.is_complete():
            return False # Simulation is not over!!!
        msg = []
        answers = self._answer_key()
        cnt = 0

        for step, answer in answers.items():
            try:
                if step - 1 > len(self.actions_taken) or self.actions_taken[step] != answers[step]:
                    cnt += 1
                    msg.append(f'When prompted with: {self._disaster.get_report(step)}\nYou should have performed action: {answer}\n')
            except IndexError:
                print(f"The index that caused the problem was step {step}")
                print(answers)
                print(self.actions_taken)
        if self._last_score is not None:
            if cnt < self._last_score:
                msg.append('You made less mistakes than your last simulation. Good Job!.\n')
            self._last_score = cnt
        else:
            self._last_score = cnt
        if cnt == 0:
            msg.append('Great job! You correctly responded to the simulation.\n')
        return msg, 0
    
    def get_report(self):
        if not self.is_complete():
            return self._disaster.get_report(self.current_time_step)

    def retry(self):
        self.actions_taken = []
        self._reports = {}
        self.current_time_step = 0
        self._location.reset()
        random.seed(self.last_seed)
        return self.set_disaster(self._disaster_name)
    
    def actions(self): # I have disasters set up to accept this format; changing it makes the code ugly
        actions = {}         # Cheap and lazy fix to format things in the way I want.
        for step in range(len(self.actions_taken)):
            action = self.actions_taken[step]
            if action in actions.keys():
                prev = actions[action]
                prev.append(step)
            else:
                actions[action] = [step]
            """for action in self.actions_taken[step]:
                actions[action] = step"""
        return actions

    def full_reset(self):
        self._location_name = None
        self._disaster_name = None
        self._disaster = None
        self._location = None
        self.actions_taken = []
        self._reports = {}
        self.current_time_step = 0
        self.last_seed = random.random()
        random.seed()

    def random(self):
        disaster = self._location.random()[0]
        # self._disaster = Disasters[self._disaster_name].value()
        return self.set_disaster(disaster)

    def _answer_key(self):
        return self._disaster.get_answer_key()
    
    @property
    def location(self):
        return self._location_name
    
    def set_location(self, value, data):
        if self.disaster is not None and self.disaster == "hurricane":
            if value != "southeast" and value != "southwest":
                return "You've chosen hurricane but selected a landlocked town." \
                    + os.linesep + "Please choose another disaster or location.", 1
        pop = int(data['population'])
        self._location_name = value
        self._location = Locations[value].value(population=pop)
        if self._disaster is not None:
            self._disaster.set_location(self._location)
        return None, 0
    
    @property
    def disaster(self):
        return self._disaster_name
    
    def set_disaster(self, value):
        if self.location is not None and self.location != "southeast" and self.location != "southwest":
            if value == "hurricane":
                return "You've chosen hurricane but selected a landlocked town." \
                    + os.linesep + "Please choose another location.", 1
        self._disaster_name = value
        self._disaster = DisasterReader(value)
        return None, 0