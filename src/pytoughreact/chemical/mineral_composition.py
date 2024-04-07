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


class MineralComp(object):
    def __init__(self, mineral, init_volume_fraction, reaction_type, radius=None,
                 reactive_surface_area=None, unit=None):
        """Initialization of Parameters

        Parameters
        -----------
        mineral :  Mineral
            Mineral phase with all its properties,
        init_volume_fraction : float
            initial volume fraction of the mineral, excluding liquid (mineral volume divided by total volume
            of solids). The sum of VOL's need not add up to 1. If the sum is less than 1, the remaining solid
            volume fraction is considered nonreactive.
        reaction_type : int
            Flag for the mineral type ; 0 for minerals at equilibrium,  for minerals under kinetic constraints
            and 2 to suppress reaction for either kinetic and/or equilibrium minerals
        radius : float
            Radius of mineral grain (in m) used to calculate surface area
        reactive_surface_area : float
            Specific reactive surface area (See user guide for more)
        unit : int
            Flag to specify the units of input reactive_surface_area values. 0 for cm2mineral/gmineral,
            1 for m2mineral/m3mineral, 2 for m2rock/m3medium (total), 3 for m2rock/m3medium (solids),
            3 and radius=0, the input surface area will remain constant,
            4 (constant rate is input in mol/sec; surface area is not used)


        Returns
        --------

        """
        self.mineral = mineral
        self.init_volume_fraction = init_volume_fraction
        self.reaction_type = reaction_type
        self.radius = radius
        self.reactive_surface_area = reactive_surface_area
        self.unit = unit
