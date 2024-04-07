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


class PermPoroZone(object):
    def __init__(self, permporo):
        """Initialization of Parameters (Permeability Porosity)

        Parameters
        -----------
        permporo :  PermPoro
            List of permeability porosity equations

        Returns
        --------

        """
        self.permporo = permporo


class PermPoro(object):
    def __init__(self, law_type, a_param, b_param):
        """Initialization of Parameters (Permeability Porosity)

        Parameters
        -----------
        law_type :  int
            Index for the permeability law.
            0: no change in permeability. Can be used to turn off permeability changes in specific
            zones
            1: simplified Carman-Kozeny (See user guide for more). The parameter values (a_param and
            b_param) are not used and may be set to 0.0 or any real number.
            2: Modified Hagen-Poiseulle Model. Permeability calculated from pore throat diameter,
            number of throats per pore, and number of pores per area using the Hagen-Poiseulle
            equation. The parameters are: a_param - number of effective throats per pore (typically
            about 2 to 3). b_param -  number of pores per m2 area
            3: cubic law (See user guide for more). The parameter values a_param and b_param are not used and may
            be set to 0.0 or any real number.
            4: modified Cubic Law (See user guide for more). The parameters are: a_param - fracture porosity /
            fracture-matrix area (analogous to fracture aperture) (m3/m2) and b_param - fracture spacing (m).
            5: Verma-Pruess permeability-porosity relation (See user guide for more). The parameters are: a_param - the
            value of “critical” porosity at which permeability goes to zero and b_param - a power law
            exponent.
        a_param : float
            Parameter A based on the permeability law selected
        b_param : float
            Parameter B based on the permeability law selected



        Returns
        --------

        """
        self.law_type = law_type
        self.a_param = a_param
        self.b_param = b_param
