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


