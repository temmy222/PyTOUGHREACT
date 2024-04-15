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

from copy import deepcopy
from pytoughreact.constants.defaults_constants import DEFAULT_MINERAL_INCON


class Mineral(object):
    def __init__(self, name, type_of_mineral, type_of_kinetic_constraint, index_solid_solution, dry_grid_block):
        """Initialization of Parameters

        Parameters
        -----------
        name :  string
            Name of the mineral phase,
        type_of_mineral : int
            Flag for the type of mineral: 0 for minerals at equilibrium, and 1 for those under kinetic
            constraints
        type_of_kinetic_constraint : int
            Flag for the type of kinetic constraint: 1 for dissolution only, 2 for precipitation only, and 3
            for both (mineral can either precipitate or dissolve
        index_solid_solution : int
            Index for a solid solution mineral end member. All end members for a specified phase are given the
            same ISS value: ISS = 1 for each end member of the first solid solution, ISS = 2 for each
            end member of the second solid solution
        dry_grid_block : int
            Flag to indicate that the mineral may precipitate in a dry grid block as a result of complete
            evaporation (See user guide for more)


        Returns
        --------

        """
        self.dry_grid_block = dry_grid_block
        self.index_solid_solution = index_solid_solution
        self.type_of_kinetic_constraint = type_of_kinetic_constraint
        self.type_of_mineral = type_of_mineral
        start_index = name.find('\'')
        if start_index >= 0:
            name = name.replace("'", "")
        self.name = name
        self.dissolution = []
        self.precipitation = []
        self.equilibrium = []
        self.initial_composition = deepcopy(DEFAULT_MINERAL_INCON)

    def get_first_row(self):
        """ Function that gets the first line of information in Minerals Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (name, Mineral Type, Dry Grid) for mineral reactions
        """
        parameters = [self.name, self.type_of_mineral, self.type_of_kinetic_constraint, self.index_solid_solution,
                      self.dry_grid_block]
        return parameters

    def get_dissolution_parameters(self):
        """ Function that gets Dissolution parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (rate constant, rate pH, activation energy) for dissolution
        """
        dissolution_data = self.dissolution[0]
        dissolution_data_list = [dissolution_data.rate_constant, dissolution_data.rate_ph, dissolution_data.exponent_n,
                                 dissolution_data.exponent_theta, dissolution_data.activation_energy,
                                 dissolution_data.coef_a,
                                 dissolution_data.coef_b, dissolution_data.coef_c]
        return dissolution_data_list

    def get_composition(self):
        return self.initial_composition

    def get_precipitation_parameters(self):
        """ Function that gets Precipitation parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (rate constant, rate pH, activation energy etc) for Precipitation
        """
        precipitation_data = self.precipitation[0]
        precipitation_data_list = [precipitation_data.rate_constant, precipitation_data.rate_ph,
                                   precipitation_data.exponent_n,
                                   precipitation_data.exponent_theta, precipitation_data.activation_energy,
                                   precipitation_data.coef_a,
                                   precipitation_data.coef_b, precipitation_data.coef_c,
                                   precipitation_data.initial_volume_fraction,
                                   precipitation_data.precipitation_law_index]
        return precipitation_data_list

    def get_precipitation_parameters_2(self):
        """ Function that gets Precipitation parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters () for Precipitation
        """
        precipitation_data_2 = self.precipitation[0]
        precipitation_data_list_2 = [precipitation_data_2.log_qk_gap, precipitation_data_2.temperature_gap_1,
                                     precipitation_data_2.temperature_gap_2]
        return precipitation_data_list_2

    def get_number_of_ph_dependence(self):
        """ Function that gets number of pH dependencies

        Parameters
        -----------

        Returns
        --------
        parameter : int
            number of pH dependencies
        """
        return [len(self.dissolution[0].ph_dependence)]

    def get_ph_dependency_1(self):
        pass

    def get_ph_dependency_2(self, ph_dependency):
        """ Function that gets pH Dependency parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (rate constant, activation Energy, number of Species) for pH Dependency
        """
        # pHDep = self.dissolution[0].pHDependence[0]
        ph_dependency_list_2 = [ph_dependency.rate_constant, ph_dependency.activation_energy,
                                ph_dependency.number_of_species,
                                ph_dependency.name_of_species,
                                ph_dependency.exponent_of_species]
        return ph_dependency_list_2

    def get_equilibrium_data(self):
        """ Function that gets Equilibrium parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters for equilibrium
        """
        equil_data = self.equilibrium[0]
        equil_data_list = [equil_data.log_qk_gap, equil_data.temperature_gap_1, equil_data.temperature_gap_2]
        return equil_data_list
