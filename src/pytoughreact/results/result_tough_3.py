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

import os
import numpy as np
import csv
import collections
import itertools
from pytoughreact.utilities.t2_utilities import t2Utilities


class ResultTough3(object):
    """ Class for processing results from Tough3 """
    def __init__(self, simulatortype, filelocation, filetitle=None, **kwargs):
        """Initialization of Parameters

        Parameters
        -----------
        simulator_type :  string
            Type of simulator being run. Can either be 'tmvoc', 'toughreact' or 'tough3'.
            Should be tough3 for this class
        file_location : string
            Location of results file on system
        file_title : string
            Title or name of the file. Example is 'kddconc.tec' or 'OUTPUT.csv'
        kwargs: dict
            1) generation (string) - if generation data exists in the results.


        Returns
        --------

        """
        if filelocation is None:
            self.filelocation = os.getcwd()
        else:
            self.filelocation = filelocation
            os.chdir(self.filelocation)
        self.filetitle = filetitle
        self.simulatortype = simulatortype
        self.generation = kwargs.get('generation')
        self.file_as_list = []

    def __repr__(self):
        return 'Results from ' + self.filelocation + ' in ' + self.filetitle + ' for ' + self.simulatortype

    def read_file(self):
        """ Read file specified in file_location and file_title

        Parameters
        -----------


        Returns
        --------
        file_as_list : list
            Results from file as list

        """
        os.chdir(self.filelocation)
        with open(self.filetitle) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            self.file_as_list = []
            for row in csv_reader:
                self.file_as_list.append(row)
        return self.file_as_list

    def get_times(self):
        """ Get times stored for duration of the simulation

        Parameters
        -----------
        grid_block_number :  int
            The grid block number for which to retrieve the results
        format_of_date : str
            Provides information to the method on format of the date. For example. year, hour, min or seconds

        Returns
        --------
        unprocessed_time_data : list
            Time data directly from file without processing.
        """
        self.read_file()
        time = []
        unprocessed_time_data = []
        if self.generation is True:
            for i in range(1, len(self.file_as_list)):
                unprocessed_time_data.append(float(self.file_as_list[i][0]))
        else:
            for i in range(len(self.file_as_list)):
                if len(self.file_as_list[i]) == 1:
                    time.append(self.file_as_list[i])
            for i in range(len(time)):
                interim = time[i][0].split()
                unprocessed_time_data.append(float(interim[2]))
        return unprocessed_time_data

    def convert_times(self, format_of_date):
        """ Convert time to desirable format e.g day, month, year

        Parameters
        -----------
        format_of_date : str
            Provides information to the method on format of the date. For example. year, hour, min or seconds

        Returns
        --------
        processed_time_data  : list
            List of converted time

        """
        intermediate = self.get_times()
        utility_function = t2Utilities()
        processed_time_data = utility_function.convert_times(intermediate, format_of_date)
        return processed_time_data

    def get_time_index(self):
        """ Get Index of Time

        Parameters
        -----------


        Returns
        --------
        processed_time_data  : list
            Index the time
        """
        self.read_file()
        indexed_time = []
        for index, value in enumerate(self.file_as_list):
            if len(self.file_as_list[index]) == 1:
                indexed_time.append(index)
        indexed_time.append(len(self.file_as_list))
        return indexed_time

    def get_generation_data(self, param):
        """ Get data from generation.

        Parameters
        -----------
        param: string
            Parameter to be derive data

        Returns
        --------
        result_array : list
            Results from the generation.

        """
        self.read_file()
        result_array = []
        heading = []
        heading_first = self.file_as_list[0]
        heading_first_modify = []
        for i in heading_first:
            heading_first_modify.append(i.upper())
        for i in range(len(heading_first_modify)):
            heading.append(heading_first_modify[i].lstrip())
        index_param = heading.index(param.upper())
        for i in range(1, len(self.file_as_list)):
            result_array.append(float(self.file_as_list[i][index_param]))
        return result_array

    def get_elements(self):
        """ Get elements from the simulation

        Parameters
        -----------


        Returns
        --------
        elements : list
            Elements present in the result file.

        """
        self.read_file()
        indextime = self.get_time_index()
        temp_file = self.file_as_list[indextime[0] + 1:indextime[1]]
        elements = []
        for i in range(len(temp_file)):
            elements.append(temp_file[i][0])
        return elements

    def get_parameters(self):
        """ Remove space from parameters

        Parameters
        -----------


        Returns
        --------
        parameter_list : list
            Parameters with blanks removed.

        """
        self.read_file()
        parameter_list = self.file_as_list[0]
        for i in range(len(parameter_list)):
            parameter_list[i] = parameter_list[i].replace(" ", "")
        return parameter_list

    def get_result_dictionary(self):
        """ Results in dictionary form

        Parameters
        -----------


        Returns
        --------
        result_dict : dict
            Results dictionary

        """
        self.read_file()
        result_dict = {}
        temp_dict = {}
        index_time = self.get_time_index()
        timeraw = self.get_times()
        for i in range(len(index_time) - 1):
            temp_dict[i] = self.file_as_list[index_time[i] + 1:index_time[i + 1]]
        for i in range(len(timeraw)):
            result_dict[timeraw[i]] = temp_dict[i]
        return result_dict

    def get_timeseries_data(self, param, gridblocknumber):
        """ Get Time series data

        Parameters
        -----------
        grid_block_number :  int
            The grid block number for which to retrieve the results
        param: string
            Parameter to be derive data

        Returns
        --------
        final_timeseries_data : list
            Time series data for particular parameter.

        """
        self.read_file()
        results = self.get_result_dictionary()
        resultarray = []
        heading = []
        heading_first = self.file_as_list[0]
        heading_first_modify = []
        for i in heading_first:
            heading_first_modify.append(i.upper())
        for i in range(len(heading_first_modify)):
            heading.append(heading_first_modify[i].lstrip())
        index_param = heading.index(param.upper())
        for k in results.keys():
            resultarray.append(results[k][gridblocknumber][index_param].lstrip())
        final_timeseries_data = [float(x) for x in resultarray]
        return final_timeseries_data

    def get_element_data(self, time, param):
        """ Get Data for elements

        Parameters
        -----------
        time : float
            Time in which the data should be retrieved.
        param: string
            Parameter to be derive data

        Returns
        --------
        final_element_data : list
            Data for each of the elements.
        """
        self.read_file()
        timeraw = self.get_times()
        results = self.get_result_dictionary()
        heading = []
        heading_first = self.file_as_list[0]
        heading_first_modify = []
        for i in heading_first:
            heading_first_modify.append(i.upper())
        for i in range(len(heading_first_modify)):
            heading.append(heading_first_modify[i].lstrip())
        index_param = heading.index(param.upper())
        if time < timeraw[0]:
            time = timeraw[0]
        elif time > timeraw[-1]:
            time = timeraw[-1]
        else:
            absolute_difference_function = lambda list_value: abs(list_value - time)
            time = min(timeraw, key=absolute_difference_function)
        results_specific = results[time]
        data = []
        for i in range(len(results_specific)):
            data.append(results_specific[i][index_param].lstrip())
        final_element_data = [float(x) for x in data]
        return final_element_data

    def get_x_data(self, time):
        """ Get X Axis Data

        Parameters
        -----------
        time : float
            Time in which the data should be retrieved.

        Returns
        --------
        output : list
            Data for the x axis.
        """
        return self.get_element_data(time, 'x')

    def get_y_data(self, time):
        """ Get Y Axis Data

        Parameters
        -----------
        time : float
            Time in which the data should be retrieved.

        Returns
        --------
        output : list
            Data for the y axis.
        """
        return self.get_element_data(time, 'y')

    def get_z_data(self, time):
        """ Get Z Axis Data

        Parameters
        -----------
        time : float
            Time in which the data should be retrieved.

        Returns
        --------
        output : list
            Data for the z axis.
        """
        return self.get_element_data(time, 'z')

    def get_coord_data(self, direction, timer):
        """ Get Coordinate Data

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.
        direction : string
            Direction to get data. Can be 'X', 'Y', 'Z'

        Returns
        --------
        direction_value_output : list
            Data for the specified direction.

        """
        if direction.lower() == 'x':
            direction_value_output = self.get_x_data(timer)
        elif direction.lower() == 'y':
            direction_value_output = self.get_y_data(timer)
        elif direction.lower() == 'z':
            direction_value_output = self.get_z_data(timer)
        else:
            print("coordinates can either be X, Y or Z")
        return direction_value_output

    def get_unique_x_data(self, timer):
        """ Get Unique X Axis Data

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.

        Returns
        --------
        unique_x_output_data : list
            Unique data for the x axis.

        """
        original_array = self.get_coord_data('x', timer)
        indices_array = []
        for i in range(0, len(original_array)):
            try:
                if original_array[i] > original_array[i + 1]:
                    indices_array.append(i)
                else:
                    continue
            except Exception:
                pass
        unique_x_output_data = original_array[0:indices_array[0] + 1]
        return unique_x_output_data

    def get_x_start_points(self, timer):
        """ Get X Axis Start Point Data

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.

        Returns
        --------
        indices_array : list
            X Axis Start Point Data.

        """
        original_array = self.get_coord_data('x', timer)
        indices_array = []
        for i in range(0, len(original_array)):
            try:
                if original_array[i] > original_array[i + 1]:
                    indices_array.append(i)
                else:
                    continue
            except Exception:
                pass
        # output_data = ori_array[0:indices_array[0] + 1]
        return indices_array

    def get_unique_y_data(self, timer):
        """ Get Unique Y Axis Data

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.

        Returns
        --------
        unique_y_output_data : list
            Unique data for the y axis.

        """
        original_array = self.get_coord_data('y', timer)
        unique_y_output_data = list(set(original_array))
        return unique_y_output_data

    def get_unique_z_data(self, timer):
        """ Get Unique Z Axis Data

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.

        Returns
        --------
        unique_z_output_data : list
            Unique data for the z axis.

        """
        original_array = self.get_coord_data('z', timer)
        unique_z_output_data = list(set(original_array))
        return unique_z_output_data

    def get_number_of_layers(self, direction):
        """ Get Number of Layers

        Parameters
        -----------
        direction : string
            Direction to get data. Can be 'X', 'Y', 'Z'

        Returns
        --------
        number_of_layers : int
            Total number of layers.

        """
        if direction.lower() == 'x':
            direction_data_array = self.get_unique_x_data(0)
        elif direction.lower() == 'y':
            direction_data_array = self.get_unique_y_data(0)
        elif direction.lower() == 'z':
            direction_data_array = self.get_unique_z_data(0)
        else:
            print("coordinates can either be X, Y or Z")
        number_of_layers = len(direction_data_array)
        return number_of_layers

    def get_z_layer_data(self, layer_number, param, timer):
        """ Get Z Layer Data

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.
        layer_num: int
            Layer number in which to retrieve data
        param: string
            Parameter to be derive data

        Returns
        --------
        z_layer_data_output : list
            Data for the z direction.

        """
        x_start = self.get_x_start_points(timer)
        z_data = self.get_element_data(timer, param)
        total_grid_in_z = self.get_number_of_layers('z')
        if layer_number > 1:
            begin_index = x_start[layer_number - 2] + 1
        else:
            begin_index = 0
        if layer_number < total_grid_in_z:
            end_index = x_start[layer_number - 1] + 1
        else:
            end_index = 50
        z_layer_data_output = z_data[begin_index:end_index]
        return z_layer_data_output

    def get_x_depth_data(self, line_number, param, timer):
        """ Get X Axis And Depth Data

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.
        line_number: int
            Line number to retrieve x depth data for
        param: string
            Parameter to be derive data

        Returns
        --------
        x_depth_data_array : list
            Data for the x depth.

        """
        element_data = self.get_element_data(timer, param)
        x_layers = self.get_number_of_layers('x')
        z_layers = self.get_number_of_layers('z')
        x_depth_data_array = []
        for i in range(0, z_layers):
            x_depth_data_array.append(element_data[line_number - 1])
            line_number = line_number + x_layers
        return x_depth_data_array

    def get_layer_data(self, direction, layer_number, timer, param):
        """ Get Layer Data

        Parameters
        -----------
        direction : string
            Direction to get data. Can be 'X', 'Y', 'Z'
        timer : float
            Time in which the data should be retrieved.
        layer_num: int
            Layer number in which to retrieve data
        param: string
            Parameter to be derive data

        Returns
        --------
        layer_data_array : list
            Data for the specified direction.

        """
        number_of_layers = self.get_number_of_layers(direction)
        if layer_number > number_of_layers:
            raise ValueError("The specified layer is more than the number of layers in the model")
        else:
            if direction.lower() == 'z':
                layer_data_array = self.get_z_layer_data(layer_number, param, timer)
            elif direction.lower() == 'x':
                layer_data_array = self.get_x_depth_data(layer_number, param, timer)
        return layer_data_array

    def get_unique_coord_data(self, direction, timer):
        """ Get Unique Coordinate Data

        Parameters
        -----------
        direction : string
            Direction to get data. Can be 'X', 'Y', 'Z'
        timer : float
            Time in which the data should be retrieved.

        Returns
        --------
        unique_coordinate_data : list
            Data for the unique coordinate.

        """
        if direction.lower() == 'x':
            unique_coordinate_data = self.get_unique_x_data(timer)
        elif direction.lower() == 'y':
            unique_coordinate_data = self.get_unique_y_data(timer)
        elif direction.lower() == 'z':
            unique_coordinate_data = self.get_unique_z_data(timer)
        else:
            print("coordinates can either be X, Y or Z")
        return unique_coordinate_data

    def remove_non_increasing(self, sequenceA, sequenceB):
        """ Remove Non Increasing Data

        Parameters
        -----------
        sequenceA: list
            list containing first sequence
        sequenceB: list
            list containing second sequence

        Returns
        --------
        sequenceA, sequenceB : list, list
            Data for the unique coordinate.

        """
        monotone = self.check_strictly_increasing(sequenceA)
        if not monotone:
            index = self.duplicate_index(sequenceA)
            if len(index) > 0:
                sequenceA = self.del_index(sequenceA, index)
            indexes1 = self.duplicate_index(sequenceB)
            if len(sequenceA) != len(sequenceB):
                if len(indexes1) > 0:
                    sequenceB = self.del_index(sequenceB, indexes1)
        return sequenceA, sequenceB

    def check_strictly_increasing(self, sequence):
        """ Check for only strictly increasing data

        Parameters
        -----------
        sequence: list
            list containing data

        Returns
        --------
        output : list
            Retuns strictly increasing data

        """
        dx = np.diff(sequence)
        return np.all(dx > 0)

    def del_index(self, input_list, indexes):
        """ Delete index in data

        Parameters
        -----------
        input_list: list
            Input list to remove indexes
        indexes: list
            indexes for which to remove data

        Returns
        --------
        input_list : list
            List after indexes have been removed

        """
        for index in sorted(indexes, reverse=True):
            del input_list[index]
        return input_list

    def duplicate_index(self, sequence):
        """ Duplicate index

        Parameters
        -----------
        sequence: list
            list containing data


        Returns
        --------
        output : list
            Ouput after duplicate indices have been removed

        """
        dicta = {}
        indexes = []
        dups = collections.defaultdict(list)
        for i, e in enumerate(sequence):
            dups[e].append(i)
        for k, v in sorted(dups.items()):
            if len(v) >= 2:
                dicta[k] = v
        for k, v in dicta.items():
            indexes.append(v[1:])
        return list(itertools.chain.from_iterable(indexes))
