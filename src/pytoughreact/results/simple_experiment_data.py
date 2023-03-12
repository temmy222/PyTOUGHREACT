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
        self.filelocation = filelocation
        os.chdir(self.filelocation)
        self.filetitle = filetitle

    def read_file(self):
        os.chdir(self.filelocation)
        df = pd.read_csv(self.filetitle)
        return df

    def getColumnNames(self):
        df = self.read_file()
        heads = df.columns
        return heads

    def get_times(self):
        df = self.read_file()
        time_raw = df['Time']
        time_raw = list(time_raw)
        time_raw = time_raw[1:]
        time_raw = np.array(time_raw, float)
        return time_raw

    def get_timeseries_data(self, param):
        df = self.read_file()
        resultarray = df[param]
        resultarray = list(resultarray)
        resultarray = resultarray[1:]
        resultarray = np.array(resultarray, float)
        return resultarray
