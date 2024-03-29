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
    def __init__(self, name, typeOfMineral, typeOfKC, indexSS, dryGridBlock):
        self.dryGridBlock = dryGridBlock
        self.indexSS = indexSS
        self.typeOfKC = typeOfKC
        self.typeOfMineral = typeOfMineral
        startIndex = name.find('\'')
        if startIndex >= 0:
            name = name.replace("'", "")
        self.name = name
        self.dissolution = []
        self.precipitation = []
        self.equilibrium = []
        self.initial_composition = deepcopy(DEFAULT_MINERAL_INCON)

    def getFirstRow(self):
        """ Function that gets the first line of information in Minerals Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (name, Mineral Type, Dry Grid) for mineral reactions
        """
        parameters = [self.name, self.typeOfMineral, self.typeOfKC, self.indexSS, self.dryGridBlock]
        return parameters

    def getDissolutionParams(self):
        """ Function that gets Dissolution parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (rate constant, rate pH, activation energy) for dissolution
        """
        dissolution_data = self.dissolution[0]
        dissolution_data_list = [dissolution_data.rateConstant, dissolution_data.ratepH, dissolution_data.exponentN,
                                 dissolution_data.exponentTheta, dissolution_data.activationEnergy,
                                 dissolution_data.coefA,
                                 dissolution_data.coefB, dissolution_data.coefC]
        return dissolution_data_list

    def getComposition(self):
        return self.initial_composition

    def getPrecipitationParams(self):
        """ Function that gets Precipitation parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (rate constant, rate pH, activation energy etc) for Precipitation
        """
        precipitation_data = self.precipitation[0]
        precipitation_data_list = [precipitation_data.rateConstant, precipitation_data.ratepH,
                                   precipitation_data.exponentN,
                                   precipitation_data.exponentTheta, precipitation_data.activationEnergy,
                                   precipitation_data.coefA,
                                   precipitation_data.coefB, precipitation_data.coefC,
                                   precipitation_data.initVolumeFraction,
                                   precipitation_data.prepLawIndex]
        return precipitation_data_list

    def getPrecipitationParams2(self):
        """ Function that gets Precipitation parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters () for Precipitation
        """
        precipitation_data_2 = self.precipitation[0]
        precipitation_data_list_2 = [precipitation_data_2.logQKgap, precipitation_data_2.tempGap1,
                                     precipitation_data_2.tempGap2]
        return precipitation_data_list_2

    def getNumberOfpHDependence(self):
        """ Function that gets number of pH dependencies

        Parameters
        -----------

        Returns
        --------
        parameter : int
            number of pH dependencies
        """
        return [len(self.dissolution[0].pHDependence)]

    def getpHDependency1(self):
        pass

    def getpHDependency2(self, pHDep):
        """ Function that gets pH Dependency parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (rate constant, activation Energy, number of Species) for pH Dependency
        """
        # pHDep = self.dissolution[0].pHDependence[0]
        pH_dependency_list_2 = [pHDep.rateConstant, pHDep.activationEnergy, pHDep.numberSpecies, pHDep.nameSpecies,
                                pHDep.exponentSpecies]
        return pH_dependency_list_2

    def getEquilibriumData(self):
        """ Function that gets Equilibrium parameters

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters for equilibrium
        """
        equil_data = self.equilibrium[0]
        equil_data_list = [equil_data.logQK, equil_data.tempGap1, equil_data.tempGap2]
        return equil_data_list
