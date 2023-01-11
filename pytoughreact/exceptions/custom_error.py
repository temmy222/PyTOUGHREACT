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

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class RequiredInputException(Exception):
    """Exception raised for missing inputs"""
    def __init__(self, input_value):
        self.input_value = input_value
        self.message =  '{0} is missing from input!'.format(self.input_value)
        super().__init__(self.message)

class RelativePermeabilityTypeError(Exception):
    def __init__(self, input_value, all_rel_perm_types):
        self.input_value = input_value
        self.all_rel_perm_types = all_rel_perm_types
        self.message =  '{0} is not one of the in-built relative permeability types. Please choose one of {1}'.format(self.input_value, self.all_rel_perm_types)
        super().__init__(self.message)

class CapillaryPressureTypeError(Exception):
    def __init__(self, input_value, all_cap_pres_types):
        self.input_value = input_value
        self.all_cap_pres_types = all_cap_pres_types
        self.message =  '{0} is not one of the in-built capillary pressure types. Please choose one of {1}'.format(self.input_value, self.all_cap_pres_types)
        super().__init__(self.message)

class RestrictionError(Exception):
    def __init__(self, *args, condition_type):
        if condition_type == 'greater':
            self.message =  '{1} must be greater than {0}'.format(args[0], args[1])
        if condition_type == 'less':
            self.message =  '{1} must be less than {0}'.format(args[0], args[1])
        if condition_type == 'addition less one':
            self.message =  '{0} + {1} must be less than 1'.format(args[0], args[1])
        if condition_type == 'greater equal':
            self.message =  '{1} must be greater than or equal to {0}'.format(args[0], args[1])
        if condition_type == 'not equal':
            self.message =  '{1} must not be equal to {0}'.format(args[0], args[1])
        
        super().__init__(self.message)

class ParameterLessThanThreeError(Exception):
    def __init__(self):
        self.message =  'Parameters must be a list of parameter values with parameters less than 3'
        super().__init__(self.message)


class ReactiveOptionsError(Error):
    """Please add options for reaction calculations"""
    pass


class ReactiveConstraintsError(Error):
    """Please add options for reaction calculations"""
    pass
