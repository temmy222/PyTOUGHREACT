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
from pytoughreact.utilities.t2_utilities import t2Utilities
from pytoughreact.utilities.t2_tough_react_utilities import t2UtilitiesToughReact
import t2listing


class ResultReact(object):
    """ Class for processing results from TOUGHREACT """
    def __init__(self, simulatortype, filelocation, filetitle):
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


        Returns
        --------

        """
        self.filelocation = filelocation
        os.chdir(self.filelocation)
        self.filetitle = filetitle
        self.simulatortype = simulatortype
        self.data = t2listing.toughreact_tecplot(self.filetitle, self.get_elements())

    def __repr__(self):
        return 'Results from ' + self.filelocation + ' in ' + self.filetitle + ' for ' + self.simulatortype

    def get_parameters(self):
        """ Get Parameters from file

        Parameters
        -----------


        Returns
        --------
        output : list
            Parameters returned as list

        """
        return self.data.element.column_name

    def get_elements(self):
        """ Get elements from the simulation

        Parameters
        -----------


        Returns
        --------
        grid_blocks : list
            Elements present in the result file.

        """
        find_connection = t2UtilitiesToughReact(self.filelocation, 'CONNE')
        find_connection.find_word()
        find_connection.slice_off_line()
        find_connection.write_to_file()
        with open('test.txt') as f:
            grid_blocks = f.read().splitlines()
        return grid_blocks

    def get_times(self):
        """ Get times stored for duration of the simulation

        Parameters
        -----------


        Returns
        --------
        unprocessed_time_data : list
            Time data directly from file without processing.
        """
        time_data = self.data.times
        unprocessed_time_data = list(time_data)
        value = t2Utilities()
        if len(unprocessed_time_data) > 15:
            time_data = value.chop_list(unprocessed_time_data, 15)
            return time_data
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
        get_times = self.get_times()
        utility_class = t2Utilities()
        processed_time_data = utility_class.convert_times(get_times, format_of_date)
        return processed_time_data

    def get_timeseries_data(self, param, grid_block_number):
        """ Get Time series data

        Parameters
        -----------
        grid_block_number :  int
            The grid block number for which to retrieve the results
        param: string
            Parameter to be derived from data

        Returns
        --------
        final_timeseries_data : list
            Time series data for particular parameter.

        """
        os.chdir(self.filelocation)
        grid = self.get_elements()[grid_block_number]
        mf = self.data.history([(grid, param)])
        final_timeseries_data = mf[1]
        final_timeseries_data = list(final_timeseries_data)
        value = t2Utilities()
        if len(final_timeseries_data) > 15:
            final_timeseries_data = value.chop_list(final_timeseries_data, 15)
            return final_timeseries_data
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
        self.data.set_time(time)
        final_element_data = self.data.element[param]
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
        return self.get_element_data(time, 'X(m)')

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
        return self.get_element_data(time, 'Y(m)')

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
        return self.get_element_data(time, 'Z(m)')

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
        if len(indices_array) > 0:
            unique_x_output_data = original_array[0:indices_array[0] + 1]
        else:
            unique_x_output_data = original_array
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
        return indices_array

    def get_unique_y_data(self, timer):
        """ Get Unique Y Axis Data

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.

        Returns
        --------
        unique_x_output_data : list
            Unique data for the y axis.

        """
        original_array = self.get_coord_data('y', timer)
        output = list(set(original_array))
        return output

    def get_unique_z_data(self, timer):
        """ Get Unique Z Axis Data

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.

        Returns
        --------
        unique_x_output_data : list
            Unique data for the z axis.

        """
        ori_array = self.get_coord_data('z', timer)
        output = list(set(ori_array))
        return output

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
            array = self.get_unique_x_data(0)
        elif direction.lower() == 'y':
            array = self.get_unique_y_data(0)
        elif direction.lower() == 'z':
            array = self.get_unique_z_data(0)
        else:
            print("coordinates can either be X, Y or Z")
        number_of_layers = len(array)
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

    def get_coord_data(self, direction, timer):
        """ Get Coordinate Data

        Parameters
        -----------
        direction : string
            Direction to get data. Can be 'X', 'Y', 'Z'
        timer : float
            Time in which the data should be retrieved.

        Returns
        --------
        coordinate_data : list
            Data for the unique coordinate.

        """
        if direction.lower() == 'x':
            coordinate_data = self.get_x_data(timer)
        elif direction.lower() == 'y':
            coordinate_data = self.get_y_data(timer)
        elif direction.lower() == 'z':
            coordinate_data = self.get_z_data(timer)
        else:
            print("coordinates can either be X, Y or Z")
        return coordinate_data

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
