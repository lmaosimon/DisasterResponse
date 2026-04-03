class ConfirmSettings():
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        msg = sim.get_report()
        return msg, 0

class NewSimulation():
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.full_reset(), 0

class ResetSimulation():
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.retry()

