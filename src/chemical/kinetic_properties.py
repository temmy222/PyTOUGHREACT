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