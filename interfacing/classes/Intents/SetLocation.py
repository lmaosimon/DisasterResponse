from interfacing.classes.Search import Search

class SouthEast():
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        data = kwargs['data']
        return sim.set_location("southeast", data)
        
class SouthWest():
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        data = kwargs['data']
        return sim.set_location("southwest", data)

class NorthEast():
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        data = kwargs['data']
        return sim.set_location("northeast", data)
        
class MidWest():
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        data = kwargs['data']
        return sim.set_location("midwest", data)

class SetLocation():
    def __call__(self, **kwargs):
        sim = kwargs['sim']
        loc = kwargs['loc']
        finder = Search()
        val = finder.search(loc)
        if val != -1:
            region, info = val
        else:
            sim.set_location("northeast", {'population': 8399000})
            return "Location does not exist. Simulation will go with a random location.", 0

        return sim.set_location(region, info)