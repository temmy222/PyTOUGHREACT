class Water(object):
    def __init__(self, primary_species, temperature, pressure):
        self.pressure = pressure
        self.temperature = temperature
        self.primary_species = primary_species


class ReactGas(object):
    def __init__(self, name, fugacity_flag, partial_pressure):
        startIndex = name.find('\'')
        if startIndex >= 0:
            name = name.replace("'", "")
        self.partial_pressure = partial_pressure
        self.name = name
        self.fugacity_flag = fugacity_flag


class WaterComp(object):
    def __init__(self, primary_species, icon, nrguess, ctot, nameq='*', qksat=0.0, naads_min=None, sdens=None, imod=None, capac=None):
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
        self.NOTRANS = notrans
        startIndex = name.find('\'')
        if startIndex >= 0:
            name = name.replace("'", "")
        self.NAME = name

    def getNameTrans(self):
        listo = [self.NAME, self.NOTRANS]
        return listo
