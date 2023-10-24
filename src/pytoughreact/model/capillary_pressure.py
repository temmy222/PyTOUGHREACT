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

import pytoughreact.constants.cap_pressure_constants as cap_pres_constants
from pytoughreact.exceptions.custom_error import CapillaryPressureTypeError, RestrictionError


class CapillaryPressure(object):
    def __init__(self, type_cap, parameters) -> None:
        self.type_cap = type_cap
        self.parameters = parameters
        self.validate_cap_press()

    def validate_cap_press(self):
        """ Function that validates capillary pressure inputs

        Parameters
        -----------

        Returns
        --------
        parameters : Exception
            Exception depending on what is violated
        """
        cap_pres_aggregates = [cap_pres_constants.CAP_PRESS_LINEAR, cap_pres_constants.CAP_PRESS_LEVERETT, cap_pres_constants.CAP_PRESS_MILLY,
                               cap_pres_constants.CAP_PRESS_NONE, cap_pres_constants.CAP_PRESS_PICKENS, cap_pres_constants.CAP_PRESS_TRUST,
                               cap_pres_constants.CAP_PRESS_VAN_GENUCHTEN]
        if self.type_cap.upper() not in cap_pres_aggregates:
            raise CapillaryPressureTypeError(self.type_cap, cap_pres_aggregates)
        elif self.type_cap.upper() in cap_pres_aggregates:
            if self.type_cap.upper() == cap_pres_constants.CAP_PRESS_LINEAR:
                self.validate_linear()
            elif self.type_cap.upper() == cap_pres_constants.CAP_PRESS_PICKENS:
                self.validate_pickens()
            elif self.type_cap.upper() == cap_pres_constants.CAP_PRESS_TRUST:
                self.validate_trust()
            elif self.type_cap.upper() == cap_pres_constants.CAP_PRESS_MILLY:
                self.validate_milly()
            elif self.type_cap.upper() == cap_pres_constants.CAP_PRESS_LEVERETT:
                self.validate_leverett()

    def validate_linear(self):
        """ Function that validates linear capillary pressure inputs

        Parameters
        -----------

        Returns
        --------
        parameters : RestrictionError
            RestrictionError
        """
        if self.parameters[2] < self.parameters[1]:
            raise RestrictionError([self.parameters[1], self.parameters[2]], 'greater')

    def validate_pickens(self):
        """ Function that validates Pickens capillary pressure inputs

        Parameters
        -----------

        Returns
        --------
        parameters : RestrictionError
            RestrictionError
        """
        if self.parameters[1] < 0:
            raise RestrictionError([0, self.parameters[1]], 'greater')
        if 1 < self.parameters[1]:
            raise RestrictionError([self.parameters[1], 1], 'greater')
        if self.parameters[2] < 1:
            raise RestrictionError([1, self.parameters[2]], 'greater equal')

    def validate_trust(self):
        """ Function that validates Trust capillary pressure inputs

        Parameters
        -----------

        Returns
        --------
        parameters : RestrictionError
            RestrictionError
        """
        if self.parameters[1] < 0:
            raise RestrictionError([0, self.parameters[1]], 'greater equal')
        if self.parameters[2] == 0:
            raise RestrictionError([0, self.parameters[2]], 'not equal')

    def validate_milly(self):
        """ Function that validates Milly capillary pressure inputs

        Parameters
        -----------

        Returns
        --------
        parameters : RestrictionError
            RestrictionError
        """
        if self.parameters[0] < 0:
            raise RestrictionError([0, self.parameters[0]], 'greater equal')

    def validate_leverett(self):
        """ Function that validates Leverett capillary pressure inputs

        Parameters
        -----------

        Returns
        --------
        parameters : RestrictionError
            RestrictionError
        """
        if self.parameters[1] < 0:
            raise RestrictionError([0, self.parameters[1]], 'greater equal')
        if 1 <= self.parameters[1]:
            raise RestrictionError([self.parameters[1], 1], 'greater')

    def cap_pres_converter(self):
        """ Function that converts capillary pressure inputs

        Parameters
        -----------

        Returns
        --------
        cap_pres : dict
            Dictionary of all capillary pressure parameters
        """
        mapping_cap_pres = {}
        cap_pres = {'type': mapping_cap_pres[self.type_cap.upper()], 'parameters': self.parameters}
        return cap_pres
