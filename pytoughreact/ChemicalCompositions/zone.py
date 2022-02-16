class Zone(object):
    def __init__(self, Water, Mineral, Gas, PermPoro, Adsorption, Decay, Cation):
        self.Cation = Cation
        self.Decay = Decay
        self.Adsorption = Adsorption
        self.PermPoro = PermPoro
        self.Water = Water
        self.Mineral = Mineral
        self.Gas = Gas

class PermPoro(object):
    def __init__(self, law_type, a_param, b_param):
        self.law_type = law_type
        self.a_param = a_param
        self.b_param = b_param
