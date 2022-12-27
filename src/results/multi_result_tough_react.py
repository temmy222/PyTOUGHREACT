import os
from utilities.synergy_general_utilities import SynergyUtilities
import pandas as pd
from results.result_tough_react import ResultReact

class MultiResultReact(object):
    def __init__(self, simulator_type, file_location, file_title, prop, **kwargs):
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
        data_table = pd.DataFrame()
        for i in range(0, len(self.file_location)):
            tough_data = ResultReact(self.simulator_type, self.file_location[i], self.file_title[i])
            print(self.file_location[i])
            os.chdir(self.file_location[i])
            result_data = tough_data.get_timeseries_data(self.prop[0], grid_block_number)
            time_data = tough_data.convert_times(format_of_date='year')
            time_data_label = 'time' + str(i)
            result_data_label = 'result' + str(i)
            data_table[time_data_label] = pd.Series(time_data)
            data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def retrieve_data_multi_file_fixed_time(self, direction, time):
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
            print(tough_data.getXDepthData(1, self.prop[i], time))
        return data_table

    def retrieve_data_multi_file_fixed_time_layer(self, direction, time, layer_num):
        data_table = pd.DataFrame()
        for i in range(0, len(self.file_location)):
            tough_data = ResultReact(self.simulator_type, self.file_location[i], self.file_title[i])
            os.chdir(self.file_location[i])
            x_data = tough_data.get_coord_data(direction, time)
            result_data = tough_data.getLayerData(direction, layer_num, time, self.prop[i])
            x_data_label = 'x' + str(i)
            result_data_label = 'result' + str(i)
            data_table[x_data_label] = pd.Series(x_data)
            data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def getMultiPropDistance(self, directionX, directionY, time, layer_num):
        data_table = pd.DataFrame()
        for i in range(0, len(self.file_location)):
            for j in range(0, len(self.prop)):
                os.chdir(self.file_location[i])
                tough_data = ResultReact(self.simulator_type, self.file_location[i], self.file_title[j])
                x_data = tough_data.get_unique_coord_data(directionX, time)
                result_data = tough_data.getLayerData(directionY, layer_num, time, self.prop[j])
                if self.x_slice_value is not None:
                    inter = SynergyUtilities()
                    time_data, result_data = inter.cutdata(x_data, result_data, self.x_slice_value)
                time_data_label = self.prop[j] + 'time' + str(i) + str(j)
                result_data_label = self.prop[j] + 'result' + str(i) + str(j)
                data_table[time_data_label] = pd.Series(x_data)
                data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def getMultiFileDistance(self, directionX, directionY, time, layer_num):
        data_table = pd.DataFrame()
        for i in range(0, len(self.prop)):
            for j in range(0, len(self.file_location)):
                os.chdir(self.file_location[j])
                tough_data = ResultReact(self.simulator_type, self.file_location[j], self.file_title[j])
                x_data = tough_data.get_unique_coord_data(directionX, time)
                result_data = tough_data.getLayerData(directionY, layer_num, time, self.prop[i])
                if self.x_slice_value is not None:
                    utilities_instance = SynergyUtilities()
                    time_data, result_data = utilities_instance.cutdata(x_data, result_data, self.x_slice_value)
                time_data_label = self.prop[i] + 'time' + str(i) + str(j)
                result_data_label = self.prop[i] + 'result' + str(i) + str(j)
                data_table[time_data_label] = pd.Series(x_data)
                data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def getMultiElementData(self, grid_block_number, format_of_date='year'):
        data_table = pd.DataFrame()
        for i in range(0, len(self.file_location)):
            for j in range(0, len(self.prop)):
                os.chdir(self.file_location[i])
                tough_data = ResultReact(self.simulator_type, self.file_location[i], self.file_title[j])
                result_data = tough_data.get_timeseries_data(self.prop[j], grid_block_number)
                time_data = tough_data.convert_times(format_of_date='year')
                if self.x_slice_value is not None:
                    utilities_instance = SynergyUtilities()
                    time_data, result_data = utilities_instance.cutdata(time_data, result_data, self.x_slice_value)
                time_data_label = self.prop[j] + 'time' + str(i) + str(j)
                result_data_label = self.prop[j] + 'result' + str(i) + str(j)
                data_table[time_data_label] = pd.Series(time_data)
                data_table[result_data_label] = pd.Series(result_data)
        return data_table

