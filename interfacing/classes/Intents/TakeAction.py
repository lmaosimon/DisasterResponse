class TakeAction():
    def __init__(self):
        pass
    
    def __call__(self, sim, action):
        msg = sim.take_action(action)
        sim.time_step() # only one action per turn, so this is the end of the turn
        return sim.get_report(), 0

