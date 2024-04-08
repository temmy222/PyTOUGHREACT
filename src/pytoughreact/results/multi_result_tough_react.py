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
import pandas as pd
from pytoughreact.results.result_tough_react import ResultReact


class MultiResultReact(object):
    """ Class for retrieving results from multiple files for TOUGHREACT """
    def __init__(self, simulator_type, file_location, file_title, prop, **kwargs):
        """Initialization of Parameters

        Parameters
        -----------
        simulator_type :  list[string]
            List of type of simulator being run. Can either be 'tmvoc', 'toughreact' or 'tough3'.
            Should be toughreact for this class
        file_location : list[string]
            List of location of results file on system
        file_title : list[string]
            List of title or name of the file. Example is 'kddconc.tec'
        prop : string
            Prperty to be plotted. Example could be 'portlandite'
        kwargs: dict
            Extra property for processing. Takes in x_slice_value as a float to know at what
            point to slice the data on the x axis.


        Returns
        --------

        """
        assert isinstance(file_location, list)
        assert isinstance(file_title, list)
        assert isinstance(prop, list)
        self.file_location = file_location
        self.file_title = file_title
        self.simulator_type = simulator_type
        self.prop = prop
        self.x_slice_value = kwargs.get('x_slice_value')

    def __repr__(self):
        return 'Multiple Results from provided file locations and provided files for' + self.simulator_type

    def retrieve_data_multi_timeseries(self, grid_block_number, format_of_date='year'):
        """ Function that retrieves time and timeseries results from file

        Parameters
        -----------
        grid_block_number :  int
            The grid block number for which to retrieve the results
        format_of_date : str
            Provides information to the method on format of the date. For example. year, hour, min or seconds

        Returns
        --------
        data_table : pd.Dataframe
            Dataframe with requested output
        """
        data_table = pd.DataFrame()
        for i in range(0, len(self.file_location)):
            tough_data = ResultReact(self.simulator_type, self.file_location[i], self.file_title[i])
            print(self.file_location[i])
            os.chdir(self.file_location[i])
            result_data = tough_data.get_timeseries_data(self.prop[0], grid_block_number)
            time_data = tough_data.convert_times(format_of_date=format_of_date)
            time_data_label = 'time' + str(i)
            result_data_label = 'result' + str(i)
            data_table[time_data_label] = pd.Series(time_data)
            data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def retrieve_data_multi_file_fixed_time(self, direction, time):
        """ DataFrame to retrieve time and coordinate results from file

        Parameters
        -----------
        direction :  string
            Direction of retrieval. Can be 'X', 'Y' or 'Z'
        time : float
            Time in which the data should be retrieved.

        Returns
        --------
        data_table : pd.Dataframe
            Dataframe with requested output
        """
        data_table = pd.DataFrame()
        for i in range(0, len(self.file_location)):
            tough_data = ResultReact(self.simulator_type, self.file_location[i], self.file_title[i])
            os.chdir(self.file_location[i])
            x_data = tough_data.get_coord_data(direction, time)
            result_data = tough_data.get_element_data(time, self.prop[i])
            x_data_label = 'x' + str(i)
            result_data_label = 'result' + str(i)
            data_table[x_data_label] = pd.Series(x_data)
            data_table[result_data_label] = pd.Series(result_data)
            print(tough_data.get_x_depth_data(1, self.prop[i], time))
        return data_table

    def retrieve_data_multi_file_fixed_time_layer(self, direction, time, layer_num):
        """ DataFrame to retrieve distance and results from file

        Parameters
        -----------
        direction :  string
            Direction of retrieval. Can be 'X', 'Y' or 'Z'
        time : float
            Time in which the data should be retrieved.
        layer_num: int
            Layer number in which to retrieve data

        Returns
        --------
        data_table : pd.Dataframe
            Dataframe with requested output
        """
        data_table = pd.DataFrame()
        for i in range(0, len(self.file_location)):
            tough_data = ResultReact(self.simulator_type, self.file_location[i], self.file_title[i])
            os.chdir(self.file_location[i])
            x_data = tough_data.get_coord_data(direction, time)
            result_data = tough_data.get_layer_data(direction, layer_num, time, self.prop[i])
            x_data_label = 'x' + str(i)
            result_data_label = 'result' + str(i)
            data_table[x_data_label] = pd.Series(x_data)
            data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def getMultiPropDistance(self, directionX, directionY, time, layer_num):
        """ DataFrame to retrieve multi element time and results from file for properties

        Parameters
        -----------
        directionX :  string
            Direction to be plotted on the X axis. Can be 'X', 'Y', 'Z'
        directionY :  string
            Direction to be plotted on the Y axis. Can be 'X', 'Y', 'Z'
        time : float
            Time in which the data should be retrieved.
        layer_num: int
            Layer number in which to retrieve data

        Returns
        --------
        data_table : pd.Dataframe
            Dataframe with requested output
        """
        data_table = pd.DataFrame()
        for i in range(0, len(self.file_location)):
            for j in range(0, len(self.prop)):
                os.chdir(self.file_location[i])
                tough_data = ResultReact(self.simulator_type, self.file_location[i], self.file_title[j])
                x_data = tough_data.get_unique_coord_data(directionX, time)
                result_data = tough_data.get_layer_data(directionY, layer_num, time, self.prop[j])
                if self.x_slice_value is not None:
                    inter = t2Utilities()
                    time_data, result_data = inter.trim_data_points(x_data, result_data, self.x_slice_value)
                time_data_label = self.prop[j] + 'time' + str(i) + str(j)
                result_data_label = self.prop[j] + 'result' + str(i) + str(j)
                data_table[time_data_label] = pd.Series(x_data)
                data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def getMultiFileDistance(self, directionX, directionY, time, layer_num):
        """ DataFrame to retrieve multi element time and results from multiple files

        Parameters
        -----------
        directionX :  string
            Direction to be plotted on the X axis. Can be 'X', 'Y', 'Z'
        directionY :  string
            Direction to be plotted on the Y axis. Can be 'X', 'Y', 'Z'
        time : float
            Time in which the data should be retrieved.
        layer_num: int
            Layer number in which to retrieve data

        Returns
        --------
        data_table : pd.Dataframe
            Dataframe with requested output
        """
        data_table = pd.DataFrame()
        for i in range(0, len(self.prop)):
            for j in range(0, len(self.file_location)):
                os.chdir(self.file_location[j])
                tough_data = ResultReact(self.simulator_type, self.file_location[j], self.file_title[j])
                x_data = tough_data.get_unique_coord_data(directionX, time)
                result_data = tough_data.get_layer_data(directionY, layer_num, time, self.prop[i])
                if self.x_slice_value is not None:
                    utilities_instance = t2Utilities()
                    time_data, result_data = utilities_instance.trim_data_points(x_data, result_data, self.x_slice_value)
                time_data_label = self.prop[i] + 'time' + str(i) + str(j)
                result_data_label = self.prop[i] + 'result' + str(i) + str(j)
                data_table[time_data_label] = pd.Series(x_data)
                data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def getMultiElementData(self, grid_block_number, format_of_date='year'):
        """ DataFrame to retrieve multi element time and results from file

        Parameters
        -----------
        grid_block_number :  int
            The grid block number for which to retrieve the results
        format_of_date : str
            Provides information to the method on format of the date. For example. year, hour, min or seconds

        Returns
        --------
        data_table : pd.Dataframe
            Dataframe with requested output
        """
        data_table = pd.DataFrame()
        for i in range(0, len(self.file_location)):
            for j in range(0, len(self.prop)):
                os.chdir(self.file_location[i])
                tough_data = ResultReact(self.simulator_type, self.file_location[i], self.file_title[j])
                result_data = tough_data.get_timeseries_data(self.prop[j], grid_block_number)
                time_data = tough_data.convert_times(format_of_date)
                if self.x_slice_value is not None:
                    utilities_instance = t2Utilities()
                    time_data, result_data = utilities_instance.trim_data_points(time_data, result_data, self.x_slice_value)
                time_data_label = self.prop[j] + 'time' + str(i) + str(j)
                result_data_label = self.prop[j] + 'result' + str(i) + str(j)
                data_table[time_data_label] = pd.Series(time_data)
                data_table[result_data_label] = pd.Series(result_data)
        return data_table
