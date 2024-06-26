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


class BIODG(object):
    """Process specification"""
    def __init__(self, imonod, bfac, sw1, sw2, wea, wsub, processes, biomass, icflag=0):
        """Initialization of Parameters

        Parameters
        -----------
        imonod :  int
            Selects between multiplicative and minimum Monod model for the substrate
            degradation rate equation
        bfac : float
            Reduction factor criterion for local Newton-Raphson iteration in BIOREACT
            subroutine to reduce substrate residual
        sw1 : float
            Lower limit of aqueous phase saturation considered in the saturation inhibition
            function (if =0, the default value is 0.02)
        sw2 : float
            Upper limit of aqueous phase saturation considered in the saturation inhibition
            function (SW1 < SW2 ≤ 1)
        wea : float
            Weighting factor for the linear interpolation of electron acceptor and nutrients
            concentrations to be used in the substrate degradation rate equation (0 < WEA ≤
            1). Default value is WEA = 0.5. WEA = 1 corresponds to using the concentration
            evaluated at the end of the time step
        wsub : float
            weighting factor for the linear interpolation of substrate concentration to be used
            in the substrate degradation rate equation (0 < WSUB ≤ 1). Default value is
            WSUB = 0.5. WSUB=1 corresponds to using the concentration evaluated at the
            end of the time step
        processes: Process
            List of Processes making use of this biodegradation configuration
        biomass: Biomass
            Biomass class list with all properties of the biomass
        icflag: int
            Selects how to consider the competitive and Haldane inhibition terms in the
            Monod model

        Returns
        --------

        """
        self.biomass = biomass
        self.icflag = icflag
        self.imonod = imonod
        self.processes = processes
        self.wsub = wsub
        self.wea = wea
        self.sw2 = sw2
        self.sw1 = sw1
        self.bfac = bfac
        self.null = " "

    def get_first_set(self):
        """ Function that gets the first line of information

        Parameters
        -----------

        Returns
        --------
        bio_numerical_parameters : list
            List of numerical parameters for biodegradation
        """
        bio_numerical_parameters = [self.imonod, self.icflag, self.bfac, self.null, self.sw1, self.sw2,
                                    self.wea, self.wsub]
        return bio_numerical_parameters

    def get_number_of_biomasses(self):
        """ Function that gets the number of biomasses

        Parameters
        -----------

        Returns
        --------
        biomass_number : int
            Number of biomasses
        """
        biomasses = []
        for process in self.processes:
            biomasses.append(process.biomass)
        return len(set(biomasses))

    def get_base_parameter_and_index(self, process):
        """ Function that retrieves base parameter and index

        Parameters
        -----------
        process :  bio.Process
            the particular process of investigation

        Returns
        --------
        index : int
            Index and Base Parameter
        """
        print(len(process.all_processes))
        for i in range(len(process.all_processes)):
            first = process.all_processes[i]
            keys = list(first.keys())
            values = list(first.values())
            if values[0][1] is not None:
                print(keys[0].index)


class Process(object):
    """Process specification"""

    def __init__(self, biomass, number_of_components, mumax, yield_mass, enthalpy, total_component=0,
                 number_of_haldane=0, number_of_non_competiting=0,
                 number_competiting=0, component_params=None, gas_params=None, water_params=None):
        """Initialization of Parameters

        Parameters
        -----------
        biomass :  Biomass
            Biomass class with all properties of the biomass
        number_of_components : int
            Number of mass components responsible for competitive inhibition in process
        mumax: float
            Maximum specific substrate degradation rate
        yield_max: float
            Yield coefficient for the growth of biomass due to the degradation of unit mass of
            substrate in process IP (kg biomass / kg substrate)
        enthalpy: float
            Heat of reaction for the degradation of substrate in process (J/kg substrate)
        total_component: int
            Number of mass components controlling the substrate degradation rate in process
        number_of_haldane: int
            Number of mass components responsible for Haldane inhibition in process
        number_of_non_competiting: int
            Number of mass components responsible for non-competitive inhibition in process
        component_params : list
            List of chemical components involved in the process
        water_params : list
            List of water components involved in the process
        gas_params : list
            List of gas components involved in the process

        Returns
        --------

        """
        self.enthalpy = enthalpy
        self.numberOfComponents = number_of_components
        self.yield_mass = yield_mass
        self.mumax = mumax
        self.biomass = biomass
        self.water_params = water_params
        self.gas_params = gas_params
        self.component_params = component_params
        self.all_processes = []
        self.number_competiting = number_competiting
        self.number_of_non_competiting = number_of_non_competiting
        self.number_of_haldane = number_of_haldane
        self.totalComp = total_component

    def get_number_of_competiting(self):
        """ Function that retrieves number of competiting specie

        Parameters
        -----------

        Returns
        --------
        num_of_competiting : int
            Number of Competiting species
        """
        self.component_params.values()

    def get_uptake(self):
        """ Function that retrieves uptake information

        Parameters
        -----------

        Returns
        --------
        output : list
            list of uptake parameters
        """
        output = []
        for process in self.all_processes:
            uptake_values = list(process.values())[0][0]
            output.append(uptake_values)
        return output

    def get_ks(self):
        """ Function that retrieves Ks information

        Parameters
        -----------

        Returns
        --------
        output : list
            list of Ks parameters
        """
        dict_output = {}
        output = []
        for i in reversed(range(len(self.all_processes))):
            uptake_values = list(self.all_processes[i].values())[0][1]
            dict_output[i + 1] = uptake_values
            if uptake_values is not None:
                output.append(dict_output)
            dict_output = {}
        output.reverse()
        return output

    def get_kc(self):
        """ Function that retrieves competitive inhibition information

        Parameters
        -----------

        Returns
        --------
        output : list
            list of competitive inhibition parameters
        """
        dict_output = {}
        output = []
        for i in range(len(self.all_processes)):
            uptake_values = list(self.all_processes[i].values())[0][2]
            dict_output[i + 1] = uptake_values
            if uptake_values is not None:
                output.append(dict_output)
            dict_output = {}
        return output

    def get_knc(self):
        """ Function that retrieves non competitive inhibition information

        Parameters
        -----------

        Returns
        --------
        output : list
            list of non competitive inhibition parameters
        """
        dict_output = {}
        output = []
        for i in range(len(self.all_processes)):
            uptake_values = list(self.all_processes[i].values())[0][3]
            dict_output[i + 1] = uptake_values
            if uptake_values is not None:
                output.append(dict_output)
            dict_output = {}
        return output

    def get_kh(self):
        """ Function that retrieves haldane inhibition information

        Parameters
        -----------

        Returns
        --------
        output : list
            list of haldane inhibition parameters
        """
        dict_output = {}
        output = []
        for i in range(len(self.all_processes)):
            uptake_values = list(self.all_processes[i].values())[0][4]
            dict_output[i + 1] = uptake_values
            if uptake_values is not None:
                output.append(dict_output)
            dict_output = {}
        return output
