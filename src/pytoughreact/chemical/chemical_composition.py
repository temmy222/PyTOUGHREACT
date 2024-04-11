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


class Water(object):
    def __init__(self, primary_species, temperature, pressure):
        """Initialization of Parameters (Water composition)

        Parameters
        -----------
        primary_species :  PrimarySpecies
            Primary specie present in the water composition
        temperature : float
            Temperature of the solution (°C). Note that this temperature is used only for initial speciation
            calculations for this water, before the water composition is assigned to different grid block
        pressure : float
            Pressure of the solution (bar). This value can be omitted, in which case PT is assumed 1 bar

        Returns
        --------

        """
        self.pressure = pressure
        self.temperature = temperature
        self.primary_species = primary_species


class ReactGas(object):
    def __init__(self, name, fugacity_flag, partial_pressure):
        """Initialization of Parameters (React Gas)

        Parameters
        -----------
        name :  string
            Name of the gaseous species present in the system
        partial_pressure : float
            Initial partial pressure of the gaseous species (in bars)
        fugacity_flag : int
            Flag depicting if fugacity is enabled or not



        Returns
        --------

        """
        start_index = name.find('\'')
        if start_index >= 0:
            name = name.replace("'", "")
        self.partial_pressure = partial_pressure
        self.name = name
        self.fugacity_flag = fugacity_flag


class WaterComp(object):
    def __init__(self, primary_species, icon, nrguess, ctot, nameq='*', qksat=0.0, naads_min=None,
                 sdens=None, imod=None, capac=None):
        """Initialization of Parameters (Water composition)

        Parameters
        -----------
        primary_species :  PrimarySpecies
            Primary specie present in the water composition
        icon : int
            Flag indicating the type of constraint controlling the input concentration of the aqueous species
            1: input values of CTOT represent total amounts (in moles) for aqueous species, and total
            kilogram    s for liquid H2O
            2: the total concentration of the species will be computed such that the saturation index
            of mineral or gas  equals qksat at temperature and pressure TC2
            and PT, respectively.
            3: input values of ctot represent the known activity of the specific species (i.e., not
            total concentration) at temperature and pressure TC2 and PT, respectively.
            4: the total concentration of the species is adjusted to yield charge balance. Use only
            with a charged species
        nrguess : float
            initial guess (trial) value for the concentration of the individual primary species (not total
            concentration), in moles/kg H2O (molal) for species other than H2O and in kg for H2O.
        ctot : float
            If icon=1, CTOT is total moles of aqueous species, and total amount (in kg) of liquid water for
            H2O
        nameq : string
            Name of mineral or gas (in quotes) to use with option ICON=2. Names must match exactly
            those previously listed as minerals or gases in the definition of the chemical system
        qksat : float
            desired value of mineral log(Q/K) or gas log(fugacity) when option icon=2 is used
        sdens : float
            Sorption site density in molsites/m2mineral for this surface species
        imod : int
            Adsorption model type
            0 surface complexation without electrostatic terms
            1 constant capacitance model
            2 double diffuse layer model, linear
            3 double diffuse layer model, Gouy-Chapman (most common)
        capac : float
            Capacitance in F m–2. Must be entered only if imod=1

        Returns
        --------

        """
        self.primary_species = primary_species
        self.icon = icon
        self.nrguess = nrguess
        self.ctot = ctot
        self.nameq = nameq
        self.qksat = qksat
        self.naads_min = naads_min
        self.sdens = sdens
        self.imod = imod
        self.capac = capac


class PrimarySpecies(object):
    def __init__(self, name, notrans):
        """Initialization of Parameters

        Parameters
        -----------
        name :  string
            Name of the primary species,
        notrans : int
            Flag for transport and surface complexation options; 0 species (component) will be transported,
            1 no transport for this species (component)


        Returns
        --------

        """
        self.NOTRANS = notrans
        start_index = name.find('\'')
        if start_index >= 0:
            name = name.replace("'", "")
        self.NAME = name

    def get_name_trans(self):
        """ Function that retrieves the name of primary species and flag for transport and surface complexation options
        Parameters
        -----------

        Returns
        --------
        parameter : list
            List containing name of primary species and flag for transport and surface complexation options
        """
        parameter = [self.NAME, self.NOTRANS]
        return parameter
