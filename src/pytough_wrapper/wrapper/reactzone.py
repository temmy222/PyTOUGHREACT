class t2zone(object):
    def __init__(self, name='default', water=None, mineral=None, gas=None, permporo=None, adsorption=None, decay=None, cation=None):
        self.name = name
        self.cation = cation
        self.decay = decay
        self.adsorption = adsorption
        self.permporo = permporo
        self.water = water
        self.mineral_zone = mineral
        self.gas = gas

    def __repr__(self):
        return self.name