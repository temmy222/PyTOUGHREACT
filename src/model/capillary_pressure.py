import constants.cap_pressure_constants as cap_pres_constants
from exceptions.custom_error import CapillaryPressureTypeError, RestrictionError

class CapillaryPressure(object):
    def __init__(self, type_cap, parameters) -> None:
        self.type_cap = type_cap
        self.parameters = parameters
        self.validate_cap_press()


    def validate_cap_press(self):
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
        if self.parameters[2] < self.parameters[1]:
            raise RestrictionError([self.parameters[1], self.parameters[2]], 'greater')


    def validate_pickens(self):
        if self.parameters[1] < 0:
            raise RestrictionError([0, self.parameters[1]], 'greater')
        if 1 < self.parameters[1]:
            raise RestrictionError([self.parameters[1], 1], 'greater')
        if self.parameters[2] < 1:
            raise RestrictionError([1, self.parameters[2]], 'greater equal')


    def validate_trust(self):
        if self.parameters[1] < 0:
            raise RestrictionError([0, self.parameters[1]], 'greater equal')
        if self.parameters[2] == 0:
            raise RestrictionError([0, self.parameters[2]], 'not equal')


    def validate_milly(self):
        if self.parameters[0] < 0:
            raise RestrictionError([0, self.parameters[0]], 'greater equal')

    def validate_leverett(self):
        if self.parameters[1] < 0:
            raise RestrictionError([0, self.parameters[1]], 'greater equal')
        if 1 <= self.parameters[1]:
            raise RestrictionError([self.parameters[1], 1], 'greater')

    def cap_pres_converter(self):
        mapping_cap_pres = {}
        cap_pres = {'type': mapping_cap_pres[self.type_cap.upper()], 'parameters': self.parameters}
        return cap_pres



    

        

        
