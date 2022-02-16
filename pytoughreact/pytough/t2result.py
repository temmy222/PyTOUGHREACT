import os

from pytoughreact.pytough.t2bioresults import Tough3
from pytoughreact.pytough.t2reactresult import ToughReact


class t2result(object):
    def __init__(self, simulatortype,  filetitle,filelocation=None, **kwargs):
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
            fileReader = Tough3(self.simulatortype,  self.filetitle,self.filelocation,
                                       generation=self.generation)
        else:
            fileReader = ToughReact(self.simulatortype, self.filelocation, self.filetitle)
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

