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


class t2result(object):
    def __init__(self, simulatortype, filetitle, filelocation=None, **kwargs):
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
        if self.simulatortype.lower() == "tmvoc" or self.simulatortype.lower() == "tough3":
            fileReader = ResultTough3(self.simulatortype, self.filelocation, self.filetitle, generation=self.generation)
        else:
            fileReader = ResultReact(self.simulatortype, self.filelocation, self.filetitle)
        return fileReader

    def get_times(self, format_of_date='year'):
        fileReader = self.read_file()
        time = fileReader.convert_times(format_of_date)
        return time

    def get_time_series_data(self, param, gridblocknumber):
        fileReader = self.read_file()
        result_array = fileReader.get_timeseries_data(param, gridblocknumber)
        return result_array

    def get_grid_data(self, timer, param):
        fileReader = self.read_file()
        data = fileReader.get_element_data(timer, param)
        return data
