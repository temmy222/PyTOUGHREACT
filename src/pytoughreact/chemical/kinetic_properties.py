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


class Kinetic(object):
    def __init__(self, rateConstant, ratepH, exponentN, exponentTheta, activationEnergy, coefA=0, coefB=0, coefC=0):
        """Initialization of Parameters

        Parameters
        -----------
        rateConstant :  float
            Rate constant (in mol/m2/sec) at 25°C
        ratepH : int
            Flag for rate constant dependence on pH
        exponentN : float
            exponent eta in rate equation
        exponentTheta : float
            exponent theta in rate equation
        activationEnergy : float
            Activation energy in kJ/mol
        coefA : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desired
        coefB : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire
        coefC : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire


        Returns
        --------

        """
        self.coefC = coefC
        self.coefB = coefB
        self.coefA = coefA
        self.activationEnergy = activationEnergy
        self.exponentTheta = exponentTheta
        self.exponentN = exponentN
        self.ratepH = ratepH
        self.rateConstant = rateConstant


class Dissolution(Kinetic):
    def __init__(self, rateConstant, ratepH, exponentN, exponentTheta, activationEnergy, coefA=0, coefB=0, coefC=0):
        """Initialization of Parameters

        Parameters
        -----------
        rateConstant :  float
            Rate constant (in mol/m2/sec) at 25°C
        ratepH : int
            Flag for rate constant dependence on pH
        exponentN : float
            exponent eta in rate equation
        exponentTheta : float
            exponent theta in rate equation
        activationEnergy : float
            Activation energy in kJ/mol
        coefA : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desired
        coefB : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire
        coefC : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire


        Returns
        --------

        """
        super(Dissolution, self).__init__(rateConstant, ratepH, exponentN, exponentTheta, activationEnergy, coefA,
                                          coefB, coefC)
        self.pHDependence = []


class Precipitation(Kinetic):
    def __init__(self, rateConstant, ratepH, exponentN, exponentTheta, activationEnergy, coefA, coefB, coefC,
                 initVolumeFraction, prepLawIndex, logQKgap, tempGap1, tempGap2):
        """Initialization of Parameters

        Parameters
        -----------
        rateConstant :  float
            Rate constant (in mol/m2/sec) at 25°C
        ratepH : int
            Flag for rate constant dependence on pH
        exponentN : float
            exponent eta in rate equation
        exponentTheta : float
            exponent theta in rate equation
        activationEnergy : float
            Activation energy in kJ/mol
        coefA : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desired
        coefB : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire
        coefC : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire
        initVolumeFraction : float
            The initial volume fraction (Vmineral/Vsolid) to be assumed for calculating initial effective surface
            are a if the mineral is not present at the start of a simulation but precipitates as a new reaction
            product
        prepLawIndex : int
            Precipitation law index (See user guide for more)
        logQKgap : float
            Log (Q/K) gap (supersaturation window). A zero value represents no gap (See user guide for more).
        tempGap1 : float
            Temperature (in °C) at which to begin reducing gap
        tempGap2 : float
            Temperature (in °C) endpoint at which the gap has diminished to nearly zero (1% of original
            value). The gap decreases exponentially from the first (tempGap1) to the second (tempGap2)
            temperature, and tempGap2 must always be greater than tempGap1

        Returns
        --------

        """
        super(Precipitation, self).__init__(rateConstant, ratepH, exponentN, exponentTheta, activationEnergy, coefA,
                                            coefB, coefC)
        self.tempGap2 = tempGap2
        self.tempGap1 = tempGap1
        self.logQKgap = logQKgap
        self.prepLawIndex = prepLawIndex
        self.initVolumeFraction = initVolumeFraction
        self.pHDependence = []


class Equilibrium(object):
    def __init__(self, logQK, tempGap1, tempGap2):
        """Initialization of Parameters

        Parameters
        -----------
        logQK : float
            Log (Q/K) gap (supersaturation window). A zero value represents no gap (See user guide for more).
        tempGap1 : float
            Temperature (in °C) at which to begin reducing gap
        tempGap2 : float
            Temperature (in °C) endpoint at which the gap has diminished to nearly zero (1% of original
            value). The gap decreases exponentially from the first (tempGap1) to the second (tempGap2)
            temperature, and tempGap2 must always be greater than tempGap1

        Returns
        --------

        """
        self.tempGap2 = tempGap2
        self.tempGap1 = tempGap1
        self.logQK = logQK


class pHDependenceType1(object):
    def __init__(self, ph1, slope1, ph2, slope2):
        """Initialization of Parameters (Reaction rate dependence on pH)

        Parameters
        -----------
        ph1 : float
            pH of first mineral in reaction
        slope1 : float
            slope of first mineral in reaction
        ph2 : float
            pH of second mineral in reaction
        slope2 : float
            slope of second mineral in reaction

        Returns
        --------

        """
        self.slope2 = slope2
        self.ph2 = ph2
        self.slope1 = slope1
        self.ph1 = ph1


class pHDependenceType2(object):
    def __init__(self, rateConstant, activationEnergy, numberSpecies, nameSpecies, exponentSpecies):
        """Initialization of Parameters

        Parameters
        -----------
        rateConstant :  float
            Rate constant (in mol/m2/sec) at 25°C
        activationEnergy : float
            Activation energy in kJ/mol
        numberSpecies : int
            Number of species involved in each mechanism (a maximum of five species can be
            considered)
        nameSpecies : list
            Name of species involved in the mechanism that must be in the list of primary or
            secondary specie
        exponentSpecies : float
            Power term in the rate equation (See user guide for more)


        Returns
        --------

        """
        self.exponentSpecies = exponentSpecies
        self.nameSpecies = nameSpecies
        self.numberSpecies = numberSpecies
        self.activationEnergy = activationEnergy
        self.rateConstant = rateConstant
