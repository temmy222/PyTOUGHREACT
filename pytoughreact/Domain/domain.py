import sys

sys.path.append(".")
from Grid.grid import Grid


class Domain(object):
    def __init__(self, grid, rock_type, perm, porosity, initial_pressure, initial_temp, density, conductivity=None,
                 specific_heat=None):
        self.density = density
        self.initial_pressure = initial_pressure
        self.initial_temp = initial_temp
        self.specific_heat = specific_heat
        self.conductivity = conductivity
        assert isinstance(perm, dict)
        self.perm = perm
        self.poro = porosity
        assert isinstance(rock_type, list)
        self.rock_type = rock_type
        assert isinstance(grid, Grid)
        self.Grid = grid

    def getDefaultIncond(self, pressure, temperature):
        answer = [pressure, temperature]
        return answer

    def addRelPerm(self, typeNum, values):
        assert isinstance(values, list)
        answer_dict = {'type': typeNum, 'parameters': values}
        return answer_dict

    def addCapPres(self, typeNum, values):
        assert isinstance(values, list)
        answer_dict = {'type': typeNum, 'parameters': values}
        return answer_dict
