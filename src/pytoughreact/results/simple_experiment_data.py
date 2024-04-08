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
import os
import pandas as pd


class Experiment(object):
    def __init__(self, filelocation, filetitle):
        """Initialization of Parameters

        Parameters
        -----------
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

    def read_file(self):
        """ Read file specified in file_location and file_title

        Parameters
        -----------


        Returns
        --------
        data_table : pd.Dataframe
            Dataframe with requested output

        """
        os.chdir(self.filelocation)
        data_table = pd.read_csv(self.filetitle)
        return data_table

    def getColumnNames(self):
        """ Get coulmn names from data table

        Parameters
        -----------


        Returns
        --------
        column_names : list
            column names in file

        """
        df = self.read_file()
        column_names = df.columns
        return column_names

    def get_times(self):
        """ Get times stored for duration of the simulation

        Parameters
        -----------


        Returns
        --------
        unprocessed_time_data : list
            Time data directly from file without processing.
        """
        df = self.read_file()
        unprocessed_time_data = df['Time']
        unprocessed_time_data = list(unprocessed_time_data)
        unprocessed_time_data = unprocessed_time_data[1:]
        unprocessed_time_data = np.array(unprocessed_time_data, float)
        return unprocessed_time_data

    def get_timeseries_data(self, param):
        """ Get Time series data

        Parameters
        -----------
        param: string
            Parameter to be derived from data

        Returns
        --------
        final_timeseries_data : list
            Time series data for particular parameter.

        """
        df = self.read_file()
        final_timeseries_data = df[param]
        final_timeseries_data = list(final_timeseries_data)
        final_timeseries_data = final_timeseries_data[1:]
        final_timeseries_data = np.array(final_timeseries_data, float)
        return final_timeseries_data
