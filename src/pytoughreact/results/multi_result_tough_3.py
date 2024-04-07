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
import pandas as pd
from pytoughreact.results.result_tough_3 import ResultTough3


class MultiResultTough3(object):
    """ Class for retrieving results from multiple files for Tough3 and TMVOC """
    def __init__(self, simulator_type, file_location, file_title, prop):
        """Initialization of Parameters

        Parameters
        -----------
        simulator_type :  list[string]
            List of type of simulator being run. Can either be 'tmvoc', 'toughreact' or 'tough3'.
            Should be tough3 for this class
        file_location : list[string]
            List of location of results file on system
        file_title : list[string]
            List of title or name of the file. Example is 'kddconc.tec'
        prop : string
            Prperty to be plotted. Example could be 'portlandite'


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
            tough_data = ResultTough3(self.simulator_type, self.file_location[i], self.file_title[i])
            os.chdir(self.file_location[i])
            result_data = tough_data.get_timeseries_data(self.prop[0], grid_block_number)
            time_data = tough_data.convert_times(format_of_date='year')
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
            tough_data = ResultTough3(self.simulator_type, self.file_location[i], self.file_title[i])
            os.chdir(self.file_location[i])
            x_data = tough_data.get_coord_data(direction, time)
            result_data = tough_data.get_element_data(time, self.prop[i])
            x_data_label = 'x' + str(i)
            result_data_label = 'result' + str(i)
            data_table[x_data_label] = pd.Series(x_data)
            data_table[result_data_label] = pd.Series(result_data)
            print(tough_data.getXDepthData(1, self.prop[i], time))
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
            tough_data = ResultTough3(self.simulator_type, self.file_location[i], self.file_title[i])
            os.chdir(self.file_location[i])
            x_data = tough_data.get_coord_data(direction, time)
            result_data = tough_data.getLayerData(direction, layer_num, time, self.prop[i])
            x_data_label = 'x' + str(i)
            result_data_label = 'result' + str(i)
            data_table[x_data_label] = pd.Series(x_data)
            data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def getMultiElementData(self, grid_block_number, format_of_date):
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
        pd.set_option('float_format', lambda x: '%.9f' % x)
        for i in range(0, len(self.file_location)):
            for j in range(0, len(self.prop)):
                os.chdir(self.file_location[i])
                tough_data = ResultTough3(self.simulator_type, self.file_location[i], self.file_title[i])
                result_data = tough_data.get_timeseries_data(self.prop[j], grid_block_number)
                time_data = tough_data.convert_times(format_of_date)
                time_data_label = self.prop[j] + 'time' + str(i) + str(j)
                result_data_label = self.prop[j] + 'result' + str(i) + str(j)
                data_table[time_data_label] = pd.Series(time_data)
                data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def getMultiElementDataPerPanel(self, grid_block_number, panels, format_of_date):
        """ DataFrame to retrieve multi element time and results from file per panel

        Parameters
        -----------
        grid_block_number :  int
            The grid block number for which to retrieve the results
        panels: list[string]
            Date to be retrieved for each of the panel in the canvas
        format_of_date : str
            Provides information to the method on format of the date. For example. year, hour, min or seconds

        Returns
        --------
        data_table : pd.Dataframe
            Dataframe with requested output
        """
        data_table = pd.DataFrame()
        pd.set_option('float_format', lambda x: '%.9f' % x)
        for i in range(0, len(panels)):
            properties = list(panels[i].values())[0][0]
            os.chdir(self.file_location[i])
            tough_data = ResultTough3(self.simulator_type, self.file_location[i], self.file_title[i])
            time_data = tough_data.convert_times(format_of_date)
            time_data_label = properties[0] + 'time' + str(i) + str(0)
            data_table[time_data_label] = pd.Series(time_data)
            for j in range(0, len(properties)):
                result_data = tough_data.get_timeseries_data(properties[j], grid_block_number)
                result_data_label = properties[j] + 'result' + str(i) + str(j)
                data_table[result_data_label] = pd.Series(result_data)
        return data_table
