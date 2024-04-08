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


class t2zone(object):
    def __init__(self, name='default', water=None, mineral=None, gas=None, permporo=None, adsorption=None,
                 decay=None, cation=None):
        """ Initialization of parameters

        Parameters
        -----------
        name : string
            Name of the zone
        water : list[list[Water], list[Water]]
            List of initial and boundary waters
        mineral : MineralZone
            Mineral composition present in the zone
        gas : list[list[ReactGas], list[ReactGas]]
            List of all initial and injected gases
        permporo : PermPoroZone
            Porosity Permeability relationship to be used in the zone
        adsorption : list[list[Adsorb], list[Adsorb]]
            List of all initial and injected adsorption zones (Not Implemented yet)
        decay : list[list[Decay], list[Decay]]
            List of all initial and injected decay zones (Not Implemented yet)
        cation : list[list[Cation], list[Cation]]
            List of all initial and injected cation zones (Not Implemented yet)


        Returns
        --------

        """
        self.name = name
        self.cation = cation
        self.decay = decay
        self.adsorption = adsorption
        self.permporo = permporo
        self.water = water
        self.mineral_zone = mineral
        self.gas = gas

    def __repr__(self):
        return self.name
