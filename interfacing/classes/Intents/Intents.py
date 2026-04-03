from interfacing.classes.Intents.TakeAction import TakeAction
from interfacing.classes.Intents.SimulationActions import ResetSimulation, NewSimulation, ConfirmSettings
from interfacing.classes.Intents.SetDisaster import Hurricane, Pandemic, Tornado, Earthquake, Wildfire, RandomDisaster, Invasion, Asteroid, Sun
from interfacing.classes.Intents.SetLocation import NorthEast, SouthEast, MidWest, SouthWest, SetLocation
# from interfacing.classes.Intents.NewSimulation import NewSimulation

class Intents():
    def __init__(self):
        self.intents = {
            # The string 'New_Simulation' is from MyFirstSkill.Intents #New_Simulation
            # It is important that the strings match what's on the website exactly
            # 'New_Simulation': NewSimulation(),
            'Random': RandomDisaster(),
            'retry_simulation': ResetSimulation(),
            'another_simulation': NewSimulation(),
            'deny_settings': NewSimulation(),
            'confirm_settings': ConfirmSettings(),
            'New_Simulation': NewSimulation(),
            # 'ShelterInPlace': OrderShelterInPlace(),
            # 'StateEmergency': DeclareEmergency(),
            # 'StateAid': ApplyForStateAid(),
            # 'FederalAid': ApplyForFederalAid(),
            # 'wait': Wait(),
            # 'evacuation': OrderEvacuation(),
            'Hurricane': Hurricane(),
            'Sun_Dissipating': Sun(),
            'Asteroid': Asteroid(),
            'Invasion': Invasion(),
            'Pandemic': Pandemic(),
            'Tornado': Tornado(),
            'Earthquake': Earthquake(),
            'Wildfire': Wildfire(),
            'NewYork': NorthEast(),
            'NewOrleans': SouthEast(),
            'OklahomaCity': MidWest(),
            'LosAngeles': SouthWest(),
            'set_location': SetLocation()
        }
        self.take_action = TakeAction()

    def pass_intent(self, loc=None, **kwargs):
        intent = kwargs['intent']
        sim = kwargs['sim']
        location = loc
        if intent not in self.intents.keys():
            return self.take_action(sim=sim, action=intent)
        # Runs the code in [Intent].__call__
        return self.intents[intent](sim=sim, loc=location)
    
