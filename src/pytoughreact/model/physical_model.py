'''
MIT License

Copyright (c) [2022] [Temitope Ajayi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from t2data import mulgrid
import t2data
from pytoughreact.exceptions.custom_error import RequiredInputException
from t2grids import t2grid
from pytoughreact.numerical.physical_model_numericals import PhysicalNumericals
import pytoughreact.constants.grid_constants as grid_constants
from pytoughreact.model.relative_permeability import RelativePermeability


class PhysicalModel(object):
    def __init__(self, model_title) -> None:
        self.data = t2data()
        self.data.title = model_title

    def createGrid(self, grid):
        """ Creates Grid

        Parameters
        -----------
        grid :  Grid
            Grid object containing grid parameters

        Returns
        --------
        geo : mulgrid
            mulgrid parameter with all grid parameters

        """
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

    def specifyGravity(self, gravity=9.81):
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

    def domain_parameters(self, rock_type, perm, porosity, initial_pressure, initial_temp, density,
                          conductivity=None, specific_heat=None):
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
