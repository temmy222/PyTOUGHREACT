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
    def __init__(self, rate_constant, rate_ph, exponent_n, exponent_theta, activation_energy, coef_a=0, coef_b=0,
                 coef_c=0):
        """Initialization of Parameters

        Parameters
        -----------
        rate_constant :  float
            Rate constant (in mol/m2/sec) at 25°C
        rate_ph : int
            Flag for rate constant dependence on pH
        exponent_n : float
            exponent eta in rate equation
        exponent_theta : float
            exponent theta in rate equation
        activation_energy : float
            Activation energy in kJ/mol
        coef_a : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desired
        coef_b : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire
        coef_c : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire


        Returns
        --------

        """
        self.coef_c = coef_c
        self.coef_b = coef_b
        self.coef_a = coef_a
        self.activation_energy = activation_energy
        self.exponent_theta = exponent_theta
        self.exponent_n = exponent_n
        self.rate_ph = rate_ph
        self.rate_constant = rate_constant


class Dissolution(Kinetic):
    def __init__(self, rate_constant, rate_ph, exponent_n, exponent_theta, activation_energy, coef_a=0, coef_b=0,
                 coef_c=0):
        """Initialization of Parameters

        Parameters
        -----------
        rate_constant :  float
            Rate constant (in mol/m2/sec) at 25°C
        rate_ph : int
            Flag for rate constant dependence on pH
        exponent_n : float
            exponent eta in rate equation
        exponent_theta : float
            exponent theta in rate equation
        activation_energy : float
            Activation energy in kJ/mol
        coef_a : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desired
        coef_b : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire
        coef_c : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire


        Returns
        --------

        """
        super(Dissolution, self).__init__(rate_constant, rate_ph, exponent_n, exponent_theta, activation_energy, coef_a,
                                          coef_b, coef_c)
        self.ph_dependence = []


class Precipitation(Kinetic):
    def __init__(self, rate_constant, rate_ph, exponent_n, exponent_theta, activation_energy, coef_a, coef_b, coef_c,
                 initial_volume_fraction, precipitation_law_index, log_qk_gap, temperature_gap_1, temperature_gap_2):
        """Initialization of Parameters

        Parameters
        -----------
        rate_constant :  float
            Rate constant (in mol/m2/sec) at 25°C
        rate_ph : int
            Flag for rate constant dependence on pH
        exponent_n : float
            exponent eta in rate equation
        exponent_theta : float
            exponent theta in rate equation
        activation_energy : float
            Activation energy in kJ/mol
        coef_a : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desired
        coef_b : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire
        coef_c : float
            Coefficient that shows the rate constant dependence on temperature. Defaulted to zero
            unless a different form of rate constant dependence with temperature is desire
        initial_volume_fraction : float
            The initial volume fraction (Vmineral/Vsolid) to be assumed for calculating initial effective surface
            are a if the mineral is not present at the start of a simulation but precipitates as a new reaction
            product
        precipitation_law_index : int
            Precipitation law index (See user guide for more)
        log_qk_gap : float
            Log (Q/K) gap (supersaturation window). A zero value represents no gap (See user guide for more).
        temperature_gap_1 : float
            Temperature (in °C) at which to begin reducing gap
        temperature_gap_2 : float
            Temperature (in °C) endpoint at which the gap has diminished to nearly zero (1% of original
            value). The gap decreases exponentially from the first (temperature_gap_1) to the second (temperature_gap_2)
            temperature, and temperature_gap_2 must always be greater than temperature_gap_1

        Returns
        --------

        """
        super(Precipitation, self).__init__(rate_constant, rate_ph, exponent_n, exponent_theta, activation_energy,
                                            coef_a, coef_b, coef_c)
        self.temperature_gap_2 = temperature_gap_2
        self.temperature_gap_1 = temperature_gap_1
        self.log_qk_gap = log_qk_gap
        self.precipitation_law_index = precipitation_law_index
        self.initial_volume_fraction = initial_volume_fraction
        self.ph_dependence = []


class Equilibrium(object):
    def __init__(self, log_qk, temperature_gap_1, temperature_gap_2):
        """Initialization of Parameters

        Parameters
        -----------
        log_qk : float
            Log (Q/K) gap (supersaturation window). A zero value represents no gap (See user guide for more).
        temperature_gap_1 : float
            Temperature (in °C) at which to begin reducing gap
        temperature_gap_2 : float
            Temperature (in °C) endpoint at which the gap has diminished to nearly zero (1% of original
            value). The gap decreases exponentially from the first (tempGap1) to the second (tempGap2)
            temperature, and tempGap2 must always be greater than tempGap1

        Returns
        --------

        """
        self.tempGap2 = temperature_gap_2
        self.tempGap1 = temperature_gap_1
        self.logQK = log_qk


class PHDependenceType1(object):
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


class PHDependenceType2(object):
    def __init__(self, rate_constant, activation_energy, number_of_species, name_of_species, exponent_of_species):
        """Initialization of Parameters

        Parameters
        -----------
        rate_constant :  float
            Rate constant (in mol/m2/sec) at 25°C
        activation_energy : float
            Activation energy in kJ/mol
        number_of_species : int
            Number of species involved in each mechanism (a maximum of five species can be
            considered)
        name_of_species : list
            Name of species involved in the mechanism that must be in the list of primary or
            secondary specie
        exponent_of_species : float
            Power term in the rate equation (See user guide for more)


        Returns
        --------

        """
        self.exponent_of_species = exponent_of_species
        self.name_of_species = name_of_species
        self.number_of_species = number_of_species
        self.activation_energy = activation_energy
        self.rate_constant = rate_constant
