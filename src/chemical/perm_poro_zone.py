class PermPoroZone(object):
    def __init__(self, permporo):
        self.permporo = permporo

class PermPoro(object):
    def __init__(self, law_type, a_param, b_param):
        self.law_type = law_type
        self.a_param = a_param
        self.b_param = b_param