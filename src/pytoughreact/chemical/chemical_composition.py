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
