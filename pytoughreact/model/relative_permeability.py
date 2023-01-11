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

import constants.rel_perm_constants as rel_perm_constants
from exceptions.custom_error import RelativePermeabilityTypeError, RestrictionError

class RelativePermeability(object):
    def __init__(self, type_rel, parameters) -> None:
        self.type_rel = type_rel
        self.parameters = parameters
        if type_rel == rel_perm_constants.REL_PERM_VERMA:
            self.parameters = [0.2, 0.895, 1.259, 1.7615, 0.5089]
        self.validate_rel_perm()


    def validate_rel_perm(self):
        rel_perm_aggregates = [rel_perm_constants.REL_PERM_COREY, rel_perm_constants.REL_PERM_EXPONENTIAL, rel_perm_constants.REL_PERM_FAT_KLIKOFF,
                               rel_perm_constants.REL_PERM_GRANT, rel_perm_constants.REL_PERM_LINEAR, rel_perm_constants.REL_PERM_MOBILE_PHASES,
                               rel_perm_constants.REL_PERM_VAN_GENUCHTEN, rel_perm_constants.REL_PERM_VERMA]
        if self.type_rel.upper() not in rel_perm_aggregates:
            raise RelativePermeabilityTypeError(self.type_rel, rel_perm_aggregates)
        elif self.type_rel.upper() in rel_perm_aggregates:
            if self.type_rel.upper() == rel_perm_constants.REL_PERM_LINEAR:
                self.validate_linear()
            elif self.type_rel.upper() == rel_perm_constants.REL_PERM_COREY:
                self.validate_corey()
            elif self.type_rel.upper() == rel_perm_constants.REL_PERM_GRANT:
                self.validate_grant()

    def validate_linear(self):
        if self.parameters[2] < self.parameters[0]:
            raise RestrictionError([self.parameters[0], self.parameters[2]], 'greater')
        elif self.parameters[3] < self.parameters[1]:
            raise RestrictionError([self.parameters[1], self.parameters[3]], 'greater')

    def validate_corey(self):
        if self.parameters[0] + self.parameters[1] < 1:
            raise RestrictionError([self.parameters[0], self.parameters[1]], 'addition less one')

    def validate_grant(self):
        if self.parameters[0] + self.parameters[1] < 1:
            raise RestrictionError([self.parameters[0], self.parameters[1]], 'addition less one')

    def validate_fat_klikoff(self):
        if self.parameters[0] < 1:
            raise RestrictionError([self.parameters[0], 1], 'greater')

    def rel_perm_converter(self):
        mapping_rel_perm = {rel_perm_constants.REL_PERM_LINEAR:1 , rel_perm_constants.REL_PERM_EXPONENTIAL:2, rel_perm_constants.REL_PERM_COREY:3,
                            rel_perm_constants.REL_PERM_GRANT:4, rel_perm_constants.REL_PERM_MOBILE_PHASES:5, rel_perm_constants.REL_PERM_FAT_KLIKOFF:6,
                            rel_perm_constants.REL_PERM_VAN_GENUCHTEN:7, rel_perm_constants.REL_PERM_VERMA:8}
        rel_perm = {'type': mapping_rel_perm[self.type_rel.upper()], 'parameters': self.parameters}
        return rel_perm
        


    

        

        
