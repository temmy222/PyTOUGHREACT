from t2data import mulgrid
import t2data
from exceptions.custom_error import RequiredInputException, RelativePermeabilityTypeError
from t2grids import t2grid
from numerical.physical_model_numericals import PhysicalNumericals
import constants.grid_constants as grid_constants
import constants.rel_perm_constants as rel_perm_constants
from model.relative_permeability import RelativePermeability


class PhysicalModel(object):
    def __init__(self, model_title) -> None:
        self.data = t2data()
        self.data.title = model_title
        

    def createGrid(self, grid):
        if grid:
            geo = mulgrid().rectangular(grid.x_dimension, grid.y_dimension, grid.z_dimension, grid.grid_top)
            self.geo = geo
        else:
            raise RequiredInputException(grid_constants.GRID_NAME)         
        return geo

    def convertGrid(self):
        self.data.grid = t2grid().fromgeo(self.geo)

    def storeGridData(self, file_name):
        if self.geo:
            self.geo.write(file_name)

    def specifyGravity(self, gravity =9.81):
        self.gravity = gravity

    def initialConditions(self, temperature, pressure):
        self.temperature = temperature
        self.pressure = pressure

    def defineNumericals(self):
        numerical = PhysicalNumericals()
        self.numerical = numerical

    def relative_permeability(self, type_rel, parameters):
        rel_perm_def = RelativePermeability(type_rel, parameters)
        rel_perm = rel_perm_def.rel_perm_converter()
        self.rel_perm = rel_perm

    def domain_parameters(self, rock_type, perm, porosity, initial_pressure, initial_temp, density, conductivity=None, specific_heat=None):
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
