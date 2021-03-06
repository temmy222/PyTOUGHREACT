from collections import Counter


class BIODG(object):
    """Process specification"""

    def __init__(self, imonod, bfac, sw1, sw2, wea, wsub, processes, biomass, icflag=0):
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

    def getFirstSet(self):
        listo = [self.imonod, self.icflag, self.bfac, self.null, self.sw1, self.sw2, self.wea, self.wsub]
        return listo

    def getNumberOfBiomasses(self):
        biomasses = []
        for process in self.processes:
            biomasses.append(process.biomass)
        return len(set(biomasses))

    def getBaseParameterAndIndex(self, process):
        print(len(process.allProcesses))
        for i in range(len(process.allProcesses)):
            first = process.allProcesses[i]
            keys = list(first.keys())
            values = list(first.values())
            if values[0][1] is not None:
                print(keys[0].index)


class Process(object):
    """Process specification"""

    def __init__(self, biomass, numberOfComponents, mumax, yield_mass, enthalpy, totalComp = 0, NumOfHaldane = 0, NumOfNonCompetiting = 0, NumOfCompetiting = 0, componentParams=None, gasParams=None,
                 waterParams=None):
        self.enthalpy = enthalpy
        self.numberOfComponents = numberOfComponents
        self.yield_mass = yield_mass
        self.mumax = mumax
        self.biomass = biomass
        self.waterParams = waterParams
        self.gasParams = gasParams
        self.componentParams = componentParams
        self.allProcesses = []
        self.NumOfCompetiting = NumOfCompetiting
        self.NumOfNonCompetiting = NumOfNonCompetiting
        self.NumOfHaldane = NumOfHaldane
        self.totalComp = totalComp

    def getNumOfCompetiting(self):
        self.componentParams.values()

    def getUptake(self):
        output = []
        for process in self.allProcesses:
            uptake_values = list(process.values())[0][0]
            output.append(uptake_values)
        return output

    def getKs(self):
        dict_output = {}
        output = []
        for i in reversed(range(len(self.allProcesses))):
            uptake_values = list(self.allProcesses[i].values())[0][1]
            dict_output[i + 1] = uptake_values
            if uptake_values is not None:
                output.append(dict_output)
            dict_output = {}
        output.reverse()
        return output

    def getKc(self):
        dict_output = {}
        output = []
        for i in range(len(self.allProcesses)):
            uptake_values = list(self.allProcesses[i].values())[0][2]
            dict_output[i + 1] = uptake_values
            if uptake_values is not None:
                output.append(dict_output)
            dict_output = {}
        return output

    def getKnc(self):
        dict_output = {}
        output = []
        for i in range(len(self.allProcesses)):
            uptake_values = list(self.allProcesses[i].values())[0][3]
            dict_output[i + 1] = uptake_values
            if uptake_values is not None:
                output.append(dict_output)
            dict_output = {}
        return output

    def getKh(self):
        dict_output = {}
        output = []
        for i in range(len(self.allProcesses)):
            uptake_values = list(self.allProcesses[i].values())[0][4]
            dict_output[i + 1] = uptake_values
            if uptake_values is not None:
                output.append(dict_output)
            dict_output = {}
        return output
