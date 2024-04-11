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

import numpy as np


class T2Utilities(object):
    def __init__(self):
        pass

    def convert_times(self, arraylist, format_of_date):
        """ Convert times to second/minute/hour/day/year

        Parameters
        -----------
        arraylist :  list
            Array of the time to be converted
        format_of_date : str
            Provides information to the method on format of the date. For example. year, hour, min or seconds

        Returns
        --------
        processed_time_data : list
            Time data after conversion
        """
        processing_data_array = arraylist
        processed_time_data = []
        if format_of_date.lower() == 'year':
            for i in range(len(processing_data_array)):
                processed_time_data.append(processing_data_array[i] / 3.154e+7)
        elif format_of_date.lower() == 'day':
            for i in range(len(processing_data_array)):
                processed_time_data.append(processing_data_array[i] / 86400)
        elif format_of_date.lower() == 'hour':
            for i in range(len(processing_data_array)):
                processed_time_data.append(processing_data_array[i] / 3600)
        elif format_of_date.lower() == 'minute':
            for i in range(len(processing_data_array)):
                processed_time_data.append(processing_data_array[i] / 60)
        elif format_of_date.lower() == 'second':
            for i in range(len(processing_data_array)):
                processed_time_data.append(processing_data_array[i])
        else:
            raise ValueError("format can either be year, day, hour, minute or second")
        return processed_time_data

    def chop_list(self, input_list, step_increase=3):
        """ Reduce the length of the list

        Parameters
        -----------
        input_list :  list[float]
            List for which its size is to be reduced
        step_increase : int
            Step increase to used in the length reduction

        Returns
        --------
        final_processed_list : list
            List data after reduction
        """
        global final_processed_list
        if isinstance(input_list, list):
            if len(input_list) > 100:
                input_list = input_list[0:len(input_list):step_increase]
                self.chop_list(input_list)
            else:
                final_processed_list = input_list[0:len(input_list):step_increase]
        return final_processed_list

    def trim_data_points(self, time_data, result_data, slice_value):
        """ Trim the result output to avoid too many points on a graph

        Parameters
        -----------
        time_data :  list[float]
            Time data list
        result_data :  list[float]
            Result data list
        slice_value : float
            Number at which to trim the data

        Returns
        --------
        time_data, result_data : list , list
            List data after trimming

        """
        for i in range(len(time_data) - 1, 0, -1):
            if time_data[i] > slice_value:
                del time_data[i]
                del result_data[i]
        return time_data, result_data

    def remove_repetiting(self, time_list, value_list):
        """ Remove repetiting values

        Parameters
        -----------
        time_list :  list[float]
            Time data list
        value_list :  list[float]
            Result data list

        Returns
        --------
        final_time_list, final_value_list : list , list
            List data after removing repetiting values

        """
        final_time_list = []
        final_value_list = []
        for i in range(0, len(time_list)):
            if time_list[i] not in final_time_list:
                final_time_list.append(time_list[i])
                final_value_list.append(value_list[i])
        for i in range(len(final_time_list) - 1, 0, -1):
            if final_time_list[i] - final_time_list[i - 1] < 1:
                del final_time_list[i]
                del final_value_list[i]
        return final_time_list, final_value_list

    def param_label_full(self, param):
        """ Get Full Names of TOUGHREACT and TMVIO parameters to be embedded in graphs

        Parameters
        -----------
        param: string
            Parameter to be derived from data

        Returns
        --------
        output : string
            Full name of parameter

        """
        dict_param = {'PRES': 'Pressure (Pa)', 'TEMP': 'Temperature ($^o C$)', 'SAT_G': 'Gas Saturation (-)',
                      'SAT_L': 'Liquid Saturation (-)',
                      'SAT_N': 'NAPL Saturation (-)', 'X_WATER_G': 'Water Mass Fraction in Gas (-)',
                      'X_AIR_G': 'Air Mass Fraction in Gas (-)',
                      'X_WATER_L': 'Water Mass Fraction in Liquid (-)', 'X_AIR_L': 'Air Mass Fraction in Liquid (-)',
                      'X_WATER_N': 'Water Mass Fraction in NAPL (-)',
                      'X_AIR_N': 'Air Mass Fraction in NAPL (-)', 'REL_G"': 'Relative Permeability of Gas (-)',
                      'REL_L': 'Relative Permeability of Liquid (-)',
                      'REL_N': 'Relative Permeability of NAPL (-)',
                      'PCAP_GL': 'Capillary Pressure of Gas in Liquid (Pa)',
                      'PCAP_GN': 'Capillary Pressure of Gas in NAPL (Pa)', 'DEN_G': 'Gas Density ($kg/m^3$)',
                      'DEN_L': 'Liquid Density ($kg/m^3$)',
                      'DEN_N': 'NAPL Density ($kg/m^3$)', 'POR': 'Porosity', 'BIO1': 'Biomass Mass Fraction(-)',
                      'BIO2': 'Biomass Mass Fraction(-)',
                      'X_BENZEN_L': 'Mass Fraction of Benzene in Liquid',
                      'X_TOLUEN_L': 'Mass Fraction of Toluene in Liquid',
                      'X_N-DECA_L': 'Mass Fraction of Decane in Liquid',
                      'X_TOLUEN_N': 'Mass Fraction of Toluene in NAPL',
                      'X_TOLUEN_G': 'Mass Fraction of Toluene in Gas', 'PH': 'pH', 'T_NA+': 'Concentration of Sodium',
                      'T_CL-': 'Concentration of Chlorine',
                      'T_CA+2': 'Concentration of Calcium', 'T_H2O': 'Concentration of Water',
                      'T_H+': 'Concentration of Hydrogen',
                      'T_SO4-2': 'Concentration of Sulphate',
                      'CALCITE': 'Calcite', 'PORTLANDITE': 'Portlandite', 'GYPSUM': 'Gypsum',
                      'POROSITY': 'Porosity', 'ETTRINGITE': 'Ettringite',
                      'X3_L_TOLUENE': 'Mass Fraction of Toluene', 'X2_L_O2': 'Mass Fraction Oxygen',
                      'X_P-XYLE_L': 'Mass Fraction of p-Xylene'
                      }
        return dict_param[param]

    def fmt(self, x, pos):
        """ Format string

        Parameters
        -----------
        x: string
            String to be formatted

        Returns
        --------
        output : string
            String after formatting

        """
        a, b = '{:.2e}'.format(x).split('e')
        b = int(b)
        return r'${} \times 10^{{{}}}$'.format(a, b)

    def get_number_of_grids(self, input_list):
        """ Get number of grids in simulation

        Parameters
        -----------
        input_list: list
            List to determine number of grids

        Returns
        --------
        total_number_of_grids : int
            Total number of grids

        """
        total_number_of_grids = set()
        for x in input_list:
            total_number_of_grids.add(x)
        total_number_of_grids = list(total_number_of_grids)
        return len(total_number_of_grids)

    def get_grid_number(self, data_frame, direction):
        """ Get today number of grids in a particular direction

        Parameters
        -----------
        data_frame: pd.Dataframe
            Dataframe containing coordinate info
        direction: string
            Direction in which the get grid number

        Returns
        --------
        grid_details : list
            Grid information

        """
        x = data_frame[direction]
        d = {}
        for i in x:
            if i not in d:
                d[i] = 1
            else:
                d[i] += 1
        grid_details = list(d.keys())
        return grid_details, len(d)

    def cust_range(self, *args, rtol=1e-05, atol=1e-08, include=[True, False]):
        """
        Combines numpy.arange and numpy.isclose to mimic
        open, half-open and closed intervals.
        Avoids also floating point rounding errors as with
        >>> numpy.arange(1, 1.3, 0.1)
        array([1. , 1.1, 1.2, 1.3])

        args: [start, ]stop, [step, ]
            as in numpy.arange
        rtol, atol: floats
            floating point tolerance as in numpy.isclose
        include: boolean list-like, length 2
            if start and end point are included
        """
        # process arguments
        if len(args) == 1:
            start = 0
            stop = args[0]
            step = 1
        elif len(args) == 2:
            start, stop = args
            step = 1
        else:
            assert len(args) == 3
            start, stop, step = tuple(args)

        # determine number of segments
        n = (stop - start) / step + 1

        # do rounding for n
        if np.isclose(n, np.round(n), rtol=rtol, atol=atol):
            n = np.round(n)

        # correct for start/end is excluded
        if not include[0]:
            n -= 1
            start += step
        if not include[1]:
            n -= 1
            stop -= step

        return np.linspace(start, stop, int(n))

    def crange(self, *args, **kwargs):
        return self.cust_range(*args, **kwargs, include=[True, True])

    def orange(self, *args, **kwargs):
        return self.cust_range(*args, **kwargs, include=[True, False])

    def convert_parameter_name(self, param):
        """ Convert Parameters to conventional names

        Parameters
        -----------
        param: string
            Parameter to be derived from data

        Returns
        --------
        converted_output : string
            parameter after conversion

        """
        if param.lower() == 'porosity':
            converted_output = 'Porosity'
        elif param.startswith("t_"):
            converted_output = "Total Concentration (mol/L)"
        elif param.startswith("pH"):
            converted_output = 'pH'
        return converted_output
