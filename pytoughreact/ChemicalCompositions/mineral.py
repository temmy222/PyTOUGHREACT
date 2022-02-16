from copy import deepcopy

default_mineral_incon = {
    'init_volume_fraction': 0.2,
    'reaction_type': 1,
    'radius': 0.0E-00,
    'reactive surface area': 100.0,
    'unit': 0,
    'zone': 1
}


class MineralZone(object):
    def __init__(self, minerals):
        self.minerals = minerals


class PermPoroZone(object):
    def __init__(self, permporo):
        self.permporo = permporo


class MineralComp(object):
    def __init__(self, mineral, init_volume_fraction, reaction_type, radius, reactive_surface_area, unit):
        self.mineral = mineral
        self.init_volume_fraction = init_volume_fraction
        self.reaction_type = reaction_type
        self.radius = radius
        self.reactive_surface_area = reactive_surface_area
        self.unit = unit


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
        self.initial_composition = deepcopy(default_mineral_incon)

    def getFirstRow(self):
        listo = [self.name, self.typeOfMineral, self.typeOfKC, self.indexSS, self.dryGridBlock]
        return listo

    def getDissolutionParams(self):
        diss = self.dissolution[0]
        listo = [diss.rateConstant, diss.ratepH, diss.exponentN, diss.exponentTheta, diss.activationEnergy, diss.coefA,
                 diss.coefB, diss.coefC]
        return listo

    def getComposition(self):
        return self.initial_composition

    def getPrecipitationParams(self):
        diss = self.precipitation[0]
        listo = [diss.rateConstant, diss.ratepH, diss.exponentN, diss.exponentTheta, diss.activationEnergy, diss.coefA,
                 diss.coefB, diss.coefC, diss.initVolumeFraction, diss.prepLawIndex]
        return listo

    def getPrecipitationParams2(self):
        diss = self.precipitation[0]
        listo = [diss.logQKgap, diss.tempGap1, diss.tempGap2]
        return listo

    def getNumberOfpHDependence(self):
        return [len(self.dissolution[0].pHDependence)]

    def getpHDependency1(self):
        pass

    def getpHDependency2(self, pHDep):
        # pHDep = self.dissolution[0].pHDependence[0]
        listo = [pHDep.rateConstant, pHDep.activationEnergy, pHDep.numberSpecies, pHDep.nameSpecies,
                 pHDep.exponentSpecies]
        return listo


class Kinetic(object):
    def __init__(self, rateConstant, ratepH, exponentN, exponentTheta, activationEnergy, coefA=0, coefB=0, coefC=0):
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
        super(Dissolution, self).__init__(rateConstant, ratepH, exponentN, exponentTheta, activationEnergy, coefA,
                                          coefB, coefC)
        self.pHDependence = []


class Precipitation(Kinetic):
    def __init__(self, rateConstant, ratepH, exponentN, exponentTheta, activationEnergy, coefA, coefB, coefC,
                 initVolumeFraction, prepLawIndex, logQKgap, tempGap1, tempGap2):
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
        self.tempGap2 = tempGap2
        self.tempGap1 = tempGap1
        self.logQK = logQK


class pHDependenceType1(object):
    def __init__(self, ph1, slope1, ph2, slope2):
        self.slope2 = slope2
        self.ph2 = ph2
        self.slope1 = slope1
        self.ph1 = ph1


class pHDependenceType2(object):
    def __init__(self, rateConstant, activationEnergy, numberSpecies, nameSpecies, exponentSpecies):
        self.exponentSpecies = exponentSpecies
        self.nameSpecies = nameSpecies
        self.numberSpecies = numberSpecies
        self.activationEnergy = activationEnergy
        self.rateConstant = rateConstant
