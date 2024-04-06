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

    def addToProcess(self, process, Uptake, Ks=None, Kc=None, Knc=None, Kh=None):
        """ Add gas component to the process

        Parameters
        -----------
        process :  Process
            This should be a Process class with all properties of the process
        Uptake : int
            uptake coefficient of gas component in particular process with respect to 1 mole of
            degraded primary substrate (mole component / mole substrate).
        Ks: float
            Substrate degradation rate
        Kc: float
            Competitive inhibition rate
        Knc: float
            Non Competitive inhibition rate
        Kh: float
            Haldane inhibition rate

        Returns
        --------
        output : dict
            Dicitionary of all parameters
        process : Process
            Updated Process with new parameters
        """
        output = {self: [Uptake, Ks, Kc, Knc, Kh]}
        if Kc is not None:
            process.NumOfCompetiting += 1
        if Knc is not None:
            process.NumOfNonCompetiting += 1
        if Kh is not None:
            process.NumOfHaldane += 1
        process.componentParams = output
        process.allProcesses.append(output)
        return output, process


class Water_Bio(object):
    """Rock type"""

    def __init__(self, name='H2O', index=1):
        self.index = index
        self.name = name

    def addToProcess(self, process, Uptake, Ks=None, Kc=None, Knc=None, Kh=None):
        """ Add water component to the process

        Parameters
        -----------
        process :  Process
            This should be a Process class with all properties of the process
        Uptake : int
            uptake coefficient of water component in particular process with respect to 1 mole of
            degraded primary substrate (mole component / mole substrate).
        Ks: float
            Substrate degradation rate
        Kc: float
            Competitive inhibition rate
        Knc: float
            Non Competitive inhibition rate
        Kh: float
            Haldane inhibition rate

        Returns
        --------
        output : dict
            Dictionary of all parameters
        process : Process
            Updated Process with new parameters
        """
        output = {self: [Uptake, Ks, Kc, Knc, Kh]}
        if Kc is not None:
            process.NumOfCompetiting += 1
        if Knc is not None:
            process.NumOfNonCompetiting += 1
        if Kh is not None:
            process.NumOfHaldane += 1
        process.componentParams = output
        process.allProcesses.append(output)
        return output, process


class BaseComponent(object):
    """Rock type"""

    def __init__(self, name=None, critTemp=None, critPres=None, critComp=None, acentricFactor=None, dipoleMoment=None,
                 boilPoint=None, vapPressA=None, vapPressB=None, vapPressC=None, vapPressD=None,
                 molWeight=None, heatCapConstantA=None, heatCapConstantB=None, heatCapConstantC=None,
                 heatCapConstantD=None,
                 liqDensity=None, refTempForDensity=None, refBinaryDif=None, refTempForDif=None, expChemDif=None,
                 liqVisConstA=None, liqVisConstB=None, liqVisConstC=None, liqVisConstD=None, liqCritVol=None,
                 liqChemSolA=None, liqChemSolB=None, liqChemSolC=None, liqChemSolD=None,
                 carbonPartCoefficient=None, fracCarbon=None, decayConstant=None):
        self.diffNAPL = 0
        self.diffGas = 0
        self.diffAqueous = 0
        self.liqCritVol = liqCritVol
        self.liqVisConstD = liqVisConstD
        self.liqVisConstC = liqVisConstC
        self.decayConstant = decayConstant
        self.fracCarbon = fracCarbon
        self.carbonPartCoefficient = carbonPartCoefficient
        self.liqChemSolA = liqChemSolA
        self.liqChemSolD = liqChemSolD
        self.liqChemSolB = liqChemSolB
        self.liqChemSolC = liqChemSolC
        self.liqVisConstB = liqVisConstB
        self.liqVisConstA = liqVisConstA
        self.expChemDif = expChemDif
        self.refTempForDif = refTempForDif
        self.refBinaryDif = refBinaryDif
        self.refTempForDensity = refTempForDensity
        self.liqDensity = liqDensity
        self.heatCapConstantD = heatCapConstantD
        self.heatCapConstantC = heatCapConstantC
        self.heatCapConstantB = heatCapConstantB
        self.heatCapConstantA = heatCapConstantA
        self.molWeight = molWeight
        self.vapPressD = vapPressD
        self.vapPressB = vapPressB
        self.vapPressA = vapPressA
        self.boilPoint = boilPoint
        self.dipoleMoment = dipoleMoment
        self.acentricFactor = acentricFactor
        self.critComp = critComp
        self.vapPressC = vapPressC
        self.critPres = critPres
        self.name = name
        self.critTemp = critTemp

    def getFirstSet(self):
        """ Function that gets the first line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Critical Temperature, Critical Pressure, Acentric Factor,
            Dipole Moment) for biodegradation
        """
        parameters = [self.critTemp, self.critPres, self.critComp, self.acentricFactor, self.dipoleMoment]
        return parameters

    def getSecondSet(self):
        """ Function that gets the second line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Boiling Point, Vapor Pressure) for biodegradation
        """
        parameters = [self.boilPoint, self.vapPressA, self.vapPressB, self.vapPressC, self.vapPressD]
        return parameters

    def getThirdSet(self):
        """ Function that gets the third line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Molecular Weight, heat Capacity Constant) for biodegradation
        """
        parameters = [self.molWeight, self.heatCapConstantA, self.heatCapConstantB, self.heatCapConstantC,
                      self.heatCapConstantD]
        return parameters

    def getFourthSet(self):
        """ Function that gets the fourth line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Liquid density, Reference Temperature for density, Diffusion) for biodegradation
        """
        parameters = [self.liqDensity, self.refTempForDensity, self.refBinaryDif, self.refTempForDif, self.expChemDif]
        return parameters

    def getFifthSet(self):
        """ Function that gets the fifth line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Liquid Viscosity) for biodegradation
        """
        parameters = [self.liqVisConstA, self.liqVisConstB, self.liqVisConstC, self.liqVisConstD, self.liqCritVol]
        return parameters

    def getSixthSet(self):
        """ Function that gets the sixth line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Liquid Chemical Solubility) for biodegradation
        """
        parameters = [self.liqChemSolA, self.liqChemSolB, self.liqChemSolC, self.liqChemSolD]
        return parameters

    def getSeventhSet(self):
        """ Function that gets the seventh line of information in INFILE Component Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (carbon Coefficient, Decay Constant) for biodegradation
        """
        parameters = [self.carbonPartCoefficient, self.fracCarbon, self.decayConstant]
        return parameters

    def addToProcess(self, process, Uptake, Ks=None, Kc=None, Knc=None, Kh=None):
        """ Add bio component to the process

        Parameters
        -----------
        process :  Process
            This should be a Process class with all properties of the process
        Uptake : int
            uptake coefficient of bio component in particular process with respect to 1 mole of
            degraded primary substrate (mole component / mole substrate).
        Ks: float
            Substrate degradation rate
        Kc: float
            Competitive inhibition rate
        Knc: float
            Non Competitive inhibition rate
        Kh: float
            Haldane inhibition rate

        Returns
        --------
        output : dict
            Dicitionary of all parameters
        process : Process
            Updated Process with new parameters
        """
        output = {self: [Uptake, Ks, Kc, Knc, Kh]}
        if Kc is not None:
            process.NumOfCompetiting += 1
        if Knc is not None:
            process.NumOfNonCompetiting += 1
        if Kh is not None:
            process.NumOfHaldane += 1
        process.componentParams = output
        process.allProcesses.append(output)
        return output, process

    def defaultToluene(self):
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

    def defaultBenzene(self):
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

    def defaultNDecane(self):
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

    def defaultPXylene(self):
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

    def defaultNPropylBenzene(self):
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

    def defaultNPentane(self):
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

    def getToluene(self):
        pass


class Solids(object):
    def __init__(self, name, mol_weight, carbonPartCoefficient, decayConstant):
        self.name = name
        self.mol_weight = mol_weight
        self.carbonPartCoefficient = carbonPartCoefficient
        self.decayConstant = decayConstant

    def getFirstSet(self):
        """ Function that gets the first line of information in INFILE Solids Section

        Parameters
        -----------

        Returns
        --------
        parameters : list
            List of parameters (Name, Molecular Weight, Decay Constant, Carbon Coefficient) for biodegradation
        """
        listo = [self.name, self.mol_weight, self.carbonPartCoefficient, self.decayConstant]
        return listo
