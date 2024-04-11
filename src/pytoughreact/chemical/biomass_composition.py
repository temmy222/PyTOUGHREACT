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


class Biomass(object):
    """Rock type"""

    def __init__(self, index, name, init_conc, min_conc, max_temp, death_rate, inhibition_constant):
        self.index = index
        self.death_rate = death_rate
        self.max_temp = max_temp
        self.min_conc = min_conc
        self.init_conc = init_conc
        self.name = name
        self.inhibition_constant = inhibition_constant


class Gas(object):
    """Rock type"""

    def __init__(self, name, index):
        self.index = index
        self.name = name

    def add_to_process(self, process, uptake, ks=None, kc=None, knc=None, kh=None):
        """ Add gas component to the process

        Parameters
        -----------
        process :  Process
            This should be a Process class with all properties of the process
        uptake : int
            uptake coefficient of gas component in particular process with respect to 1 mole of
            degraded primary substrate (mole component / mole substrate).
        ks: float
            Substrate degradation rate
        kc: float
            Competitive inhibition rate
        knc: float
            Non Competitive inhibition rate
        kh: float
            Haldane inhibition rate

        Returns
        --------
        output : dict
            Dicitionary of all parameters
        process : Process
            Updated Process with new parameters
        """
        output = {self: [uptake, ks, kc, knc, kh]}
        if kc is not None:
            process.number_competiting += 1
        if knc is not None:
            process.number_of_non_competiting += 1
        if kh is not None:
            process.number_of_haldane += 1
        process.component_params = output
        process.all_processes.append(output)
        return output, process


class WaterBio(object):
    """Rock type"""

    def __init__(self, name='H2O', index=1):
        self.index = index
        self.name = name

    def add_to_process(self, process, uptake, ks=None, kc=None, knc=None, kh=None):
        """ Add water component to the process

        Parameters
        -----------
        process :  Process
            This should be a Process class with all properties of the process
        uptake : int
            uptake coefficient of water component in particular process with respect to 1 mole of
            degraded primary substrate (mole component / mole substrate).
        ks: float
            Substrate degradation rate
        kc: float
            Competitive inhibition rate
        knc: float
            Non Competitive inhibition rate
        kh: float
            Haldane inhibition rate

        Returns
        --------
        output : dict
            Dictionary of all parameters
        process : Process
            Updated Process with new parameters
        """
        output = {self: [uptake, ks, kc, knc, kh]}
        if kc is not None:
            process.number_competiting += 1
        if knc is not None:
            process.number_of_non_competiting += 1
        if kh is not None:
            process.number_of_haldane += 1
        process.component_params = output
        process.all_processes.append(output)
        return output, process


class BaseComponent(object):
    """Rock type"""

    def __init__(self, name=None, critical_temperature=None, critical_pressure=None, critical_composition=None,
                 acentric_factor=None, dipole_moment=None,
                 boiling_point=None, vapor_pressure_a=None, vapor_pressure_b=None,
                 vapor_pressure_c=None, vapor_pressure_d=None,
                 molecular_weight=None, heat_capacity_constant_a=None, heat_capacity_constant_b=None,
                 heat_capacity_constant_c=None, heat_capacity_constant_d=None,
                 liquid_density=None, reference_temp_for_density=None, reference_binary_difference=None,
                 reference_temperature_for_difference=None, exponent_chemical_difference=None,
                 liquid_viscosity_constant_a=None, liquid_viscosity_constant_b=None, liquid_viscosity_constant_c=None,
                 liquid_viscosity_constant_d=None, liquid_critical_volume=None,
                 liquid_chemical_solubility_a=None, liquid_chemical_solubility_b=None,
                 liquid_chemical_solubility_c=None, liquid_chemical_solubility_d=None,
                 carbon_part_coefficient=None, fractional_carbon=None, decay_constant=None):
        self.differential_napl = 0
        self.differential_gas = 0
        self.differential_aqueous = 0
        self.liquid_critical_volume = liquid_critical_volume
        self.liquid_viscosity_cosntant_d = liquid_viscosity_constant_d
        self.liquid_viscosity_cosntant_c = liquid_viscosity_constant_c
        self.decay_constant = decay_constant
        self.fractional_carbon = fractional_carbon
        self.carbon_part_coefficient = carbon_part_coefficient
        self.liquid_chemical_solubility_a = liquid_chemical_solubility_a
        self.liquid_chemical_solubility_d = liquid_chemical_solubility_d
        self.liquid_chemical_solubility_b = liquid_chemical_solubility_b
        self.liquid_chemical_solubility_c = liquid_chemical_solubility_c
        self.liquid_viscosity_constant_b = liquid_viscosity_constant_b
        self.liquid_viscosity_constant_a = liquid_viscosity_constant_a
        self.exponent_chemical_difference = exponent_chemical_difference
        self.reference_temperature_for_difference = reference_temperature_for_difference
        self.reference_binary_difference = reference_binary_difference
        self.reference_temp_for_density = reference_temp_for_density
        self.liquid_density = liquid_density
        self.heat_capacity_constant_d = heat_capacity_constant_d
        self.heat_capacity_constant_c = heat_capacity_constant_c
        self.heat_capacity_constant_b = heat_capacity_constant_b
        self.heat_capacity_constant_a = heat_capacity_constant_a
        self.molecular_weight = molecular_weight
        self.vapor_pressure_d = vapor_pressure_d
        self.vapor_pressure_b = vapor_pressure_b
        self.vapor_pressure_a = vapor_pressure_a
        self.boiling_point = boiling_point
        self.dipole_moment = dipole_moment
        self.acentric_factor = acentric_factor
        self.critical_composition = critical_composition
        self.vapor_pressure_c = vapor_pressure_c
        self.critical_pressure = critical_pressure
        self.name = name
        self.critical_temperature = critical_temperature

    def get_first_set(self):
        """ Function that gets the first line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Critical Temperature, Critical Pressure, Acentric Factor,
            Dipole Moment) for biodegradation
        """
        parameters = [self.critical_temperature, self.critical_pressure, self.critical_composition,
                      self.acentric_factor, self.dipole_moment]
        return parameters

    def get_second_set(self):
        """ Function that gets the second line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Boiling Point, Vapor Pressure) for biodegradation
        """
        parameters = [self.boiling_point, self.vapor_pressure_a, self.vapor_pressure_b, self.vapor_pressure_c,
                      self.vapor_pressure_d]
        return parameters

    def get_third_set(self):
        """ Function that gets the third line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Molecular Weight, heat Capacity Constant) for biodegradation
        """
        parameters = [self.molecular_weight, self.heat_capacity_constant_a, self.heat_capacity_constant_b,
                      self.heat_capacity_constant_c, self.heat_capacity_constant_d]
        return parameters

    def get_fourth_set(self):
        """ Function that gets the fourth line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Liquid density, Reference Temperature for density, Diffusion) for biodegradation
        """
        parameters = [self.liquid_density, self.reference_temp_for_density, self.reference_binary_difference,
                      self.reference_temperature_for_difference, self.exponent_chemical_difference]
        return parameters

    def get_fifth_set(self):
        """ Function that gets the fifth line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Liquid Viscosity) for biodegradation
        """
        parameters = [self.liquid_viscosity_constant_a, self.liquid_viscosity_constant_b,
                      self.liquid_viscosity_cosntant_c, self.liquid_viscosity_cosntant_d, self.liquid_critical_volume]
        return parameters

    def get_sixth_set(self):
        """ Function that gets the sixth line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Liquid Chemical Solubility) for biodegradation
        """
        parameters = [self.liquid_chemical_solubility_a, self.liquid_chemical_solubility_b,
                      self.liquid_chemical_solubility_c, self.liquid_chemical_solubility_d]
        return parameters

    def get_seventh_set(self):
        """ Function that gets the seventh line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (carbon Coefficient, Decay Constant) for biodegradation
        """
        parameters = [self.carbon_part_coefficient, self.fractional_carbon, self.decay_constant]
        return parameters

    def add_to_process(self, process, uptake, ks=None, kc=None, knc=None, kh=None):
        """ Add bio component to the process

        Parameters
        -----------
        process :  Process
            This should be a Process class with all properties of the process
        uptake : int
            uptake coefficient of bio component in particular process with respect to 1 mole of
            degraded primary substrate (mole component / mole substrate).
        ks: float
            Substrate degradation rate
        kc: float
            Competitive inhibition rate
        knc: float
            Non Competitive inhibition rate
        kh: float
            Haldane inhibition rate

        Returns
        --------
        output : dict
            Dicitionary of all parameters
        process : Process
            Updated Process with new parameters
        """
        output = {self: [uptake, ks, kc, knc, kh]}
        if kc is not None:
            process.number_competiting += 1
        if knc is not None:
            process.number_of_non_competiting += 1
        if kh is not None:
            process.number_of_haldane += 1
        process.component_params = output
        process.all_processes.append(output)
        return output, process

    def default_toluene(self):
        """ Function that provides default parameters for Toluene component (can be modified)

        Parameters
        -----------

        Returns
        --------
        toluene : BaseComponent
            List of default parameters for Toluene for biodegradation
        """
        toluene = BaseComponent("Toluene", 591.8, 41.0, 0.263, 0.263, 0.4,
                                383.8, -7.28607, 1.38091, -2.83433, -2.79168,
                                92.141, -.2435E+02, 0.5125E+00, -.2765E-03, 0.4911E-07,
                                867, 293.0, 0.0000088, 303.10, 1.41,
                                -5.878, 1287, 0.004575, -0.000004499, 316.0,
                                0.000101, 0, 0, 0,
                                0.0088649, 0, 0)
        return toluene

    def default_benzene(self):
        """ Function that provides default parameters for Benzene component (can be modified)

        Parameters
        -----------

        Returns
        --------
        benzene : BaseComponent
            List of default parameters for benzene for biodegradation
        """
        benzene = BaseComponent("Benzene", 562.2, 48.2, 0.271, 0.212, 0.0,
                                353.2, -6.98273, 1.33213, -2.62863, -3.33399,
                                78.114, -.3392E+02, 0.4739E+00, -.3017E-03, 0.7130E-07,
                                885, 289.00, 0.770E-05, 273.10, 1.52,
                                0.4612E+01, 0.1489E+03, -.2544E-01, 0.2222E-04, 259.0,
                                0.411E-03, 0, 0, 0,
                                0.891E-01, 0, 0)
        return benzene

    def default_n_decane(self):
        """ Function that provides default parameters for Decane component (can be modified)

        Parameters
        -----------

        Returns
        --------
        decane : BaseComponent
            List of default parameters for decane for biodegradation
        """
        component = BaseComponent("n-Decane", 617.7, 21.2, 0.249, 0.489, 0.0,
                                  447.3, -8.56523, 1.97756, -5.81971, -0.29982,
                                  142.286, -7.913E+0, 9.609E-1, -5.288E-4, 1.131E-7,
                                  730.000, 293.000, 1.000E-5, 293.000, 1.600,
                                  0, 0, 0.5900, 293.000, 603.000,
                                  3.799e-7, 0, 0, 0,
                                  7.000, 0.001, 0)
        return component

    def default_p_xylene(self):
        """ Function that provides default parameters for P-Xylene component (can be modified)

        Parameters
        -----------

        Returns
        --------
        component : BaseComponent
            List of default parameters for pxylene for biodegradation
        """
        component = BaseComponent("p-Xylene", 616.2, 35.1, 0.260, 0.320, 0.1,
                                  411.5, -7.63495, 1.50724, -3.19678, -2.78710,
                                  106.168, -.2509E+02, 0.6042E+00, -.3374E-03, 0.6820E-07,
                                  861, 293.00, 0.704E-05, 293.00, 1.93,
                                  -.7790E+01, 0.1580E+04, 0.8730E-02, -.6735E-05, 379.0,
                                  0.297E-04, 0, 0, 0,
                                  0.550E+00, 0.001, 0)
        return component

    def default_n_propyl_benzene(self):
        """ Function that provides default parameters for N Propyl Benzene component (can be modified)

        Parameters
        -----------

        Returns
        --------
        component : BaseComponent
            List of default parameters for N Propyl Benzene for biodegradation
        """
        component = BaseComponent("n-PropylBenzene", 638.200, 32.000, 0.265, 0.344, 0.00,
                                  432.400, -7.92198, 1.97403, -4.27504, -1.28568,
                                  120.195, -3.129E+1, 7.486E-1, -4.601E-4, 1.081E-7,
                                  862.000, 293.000, 1.000E-5, 293.000, 1.600,
                                  -4.297E+00, 1.215E+03, 0, 0, 440.0,
                                  8.985e-6, 0, 0, 0,
                                  1.050, 0.001, 0)
        return component

    def default_n_pentane(self):
        """ Function that provides default parameters for N Pentane component (can be modified)

        Parameters
        -----------

        Returns
        --------
        component : BaseComponent
            List of default parameters for N Pentane for biodegradation
        """
        component = BaseComponent("n-Pentane", 469.7, 33.7, 0.263, 0.251, 0.0,
                                  309.2, -7.28936, 1.53679, -3.08367, -1.02456,
                                  72.151, -3.626E+00, .4873E+00, -2.580E-04, 5.305E-08,
                                  626, 293.00, 0.770E-05, 273.10, 1.52,
                                  -3.958E+00, 7.222E+02, 0., 0.0, 304.0,
                                  0.997E-07, 0, 0, 0,
                                  0.635E-00, 0.001, 0)
        return component


class Component(BaseComponent):
    def __init__(self, index):
        self.index = index

    def get_toluene(self):
        pass


class Solids(object):
    def __init__(self, name, molecular_weight, carbon_part_coefficient, decay_constant):
        self.name = name
        self.molecular_weight = molecular_weight
        self.carbon_part_coefficient = carbon_part_coefficient
        self.decay_constant = decay_constant

    def get_first_set(self):
        """ Function that gets the first line of information in INFILE Solids Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Name, Molecular Weight, Decay Constant, Carbon Coefficient) for biodegradation
        """
        listo = [self.name, self.molecular_weight, self.carbon_part_coefficient, self.decay_constant]
        return listo
