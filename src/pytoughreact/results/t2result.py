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

from pytoughreact.results.result_tough_3 import ResultTough3
from pytoughreact.results.result_tough_react import ResultReact


class T2Result(object):
    def __init__(self, simulatortype, filetitle, filelocation=None, **kwargs):
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
            # self.filelocation = os.path.dirname(os.path.realpath(__file__))
            self.filelocation = os.getcwd()
        else:
            self.filelocation = filelocation
        os.chdir(self.filelocation)
        self.filetitle = filetitle
        self.simulatortype = simulatortype
        self.generation = kwargs.get('generation')
        self.file_as_list = []

    def read_file(self):
        """ Read file specified in file_location and file_title

        Parameters
        -----------


        Returns
        --------
        resulting_class : ResultTough3 , ResultReact
            Resulting class for further processing

        """
        if self.simulatortype.lower() == "tmvoc" or self.simulatortype.lower() == "tough3":
            resulting_class = ResultTough3(self.simulatortype, self.filelocation, self.filetitle,
                                           generation=self.generation)
        else:
            resulting_class = ResultReact(self.simulatortype, self.filelocation, self.filetitle)
        return resulting_class

    def get_times(self, format_of_date='year'):
        """ Get times stored for duration of the simulation

        Parameters
        -----------
        format_of_date : str
            Provides information to the method on format of the date. For example. year, hour, min or seconds

        Returns
        --------
        processed_time_data : list
            Time data directly from file without processing.
        """
        file_reader = self.read_file()
        processed_time_data = file_reader.convert_times(format_of_date)
        return processed_time_data

    def get_time_series_data(self, param, gridblocknumber):
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
        file_reader = self.read_file()
        final_timeseries_data = file_reader.get_timeseries_data(param, gridblocknumber)
        return final_timeseries_data

    def get_grid_data(self, timer, param):
        """ Get Data for grids

        Parameters
        -----------
        timer : float
            Time in which the data should be retrieved.
        param: string
            Parameter to be derive data

        Returns
        --------
        final_element_data : list
            Data for each of the elements.
        """
        file_reader = self.read_file()
        final_element_data = file_reader.get_element_data(timer, param)
        return final_element_data
