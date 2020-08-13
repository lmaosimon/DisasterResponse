
class Hurricane():
    def __init__(self):
        pass
    
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.set_disaster("hurricane")


class Sun():
    def __init__(self):
        pass

    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.set_disaster("sun")

class Invasion():
    def __init__(self):
        pass

    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.set_disaster("invasion")


class Asteroid():
    def __init__(self):
        pass

    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.set_disaster("asteroid")
    
class Earthquake():
    def __init__(self):
        pass
    
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.set_disaster("earthquake")
        
class Tornado():
    def __init__(self):
        pass
    
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.set_disaster("tornado")
        
class Pandemic():
    def __init__(self):
        pass
    
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.set_disaster("pandemic")
        
class Wildfire():
    def __init__(self):
        pass
    
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.set_disaster("wildfire")

class RandomDisaster():
    def __init__(self):
        pass

    def __call__(self, **kwargs):
        sim = kwargs['sim']
        return sim.random()
