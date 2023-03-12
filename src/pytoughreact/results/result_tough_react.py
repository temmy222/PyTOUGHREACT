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
from pytoughreact.utilities.synergy_general_utilities import SynergyUtilities
from pytoughreact.utilities.synergy_tough_react_utilities import SynergyUtilitiesToughReact
import t2listing


class ResultReact(object):
    """ Class for processing results from TOUGHREACT """
    def __init__(self, simulatortype, filelocation, filetitle):
        self.filelocation = filelocation
        os.chdir(self.filelocation)
        self.filetitle = filetitle
        self.simulatortype = simulatortype
        self.data = t2listing.toughreact_tecplot(self.filetitle, self.get_elements())

    def __repr__(self):
        return 'Results from ' + self.filelocation + ' in ' + self.filetitle + ' for ' + self.simulatortype

    def getParameters(self):
        """ Get Parameters """
        return self.data.element.column_name

    def get_elements(self):
        """ Get elements """
        find_connection = SynergyUtilitiesToughReact(self.filelocation, 'CONNE')
        find_connection.findword()
        find_connection.sliceoffline()
        find_connection.writetofile()
        with open('test.txt') as f:
            grid_blocks = f.read().splitlines()
        return grid_blocks

    def get_times(self):
        """ Get times from data file """
        time_data = self.data.times
        time_data2 = list(time_data)
        value = SynergyUtilities()
        if len(time_data2) > 15:
            time_data = value.choplist(time_data2, 15)
            return time_data
        return time_data2

    def convert_times(self, format_of_date):
        """ Convert time to required format """
        get_times = self.get_times()
        utility_class = SynergyUtilities()
        timeyear = utility_class.convert_times(get_times, format_of_date)
        return timeyear

    def get_timeseries_data(self, param, gridblocknumber):
        """ Get timeseries data """
        os.chdir(self.filelocation)
        grid = self.get_elements()[gridblocknumber]
        mf = self.data.history([(grid, param)])
        timeseries = mf[1]
        timeseries = list(timeseries)
        value = SynergyUtilities()
        if len(timeseries) > 15:
            timeseries = value.choplist(timeseries, 15)
            return timeseries
        return timeseries

    def get_element_data(self, time, param):
        """ Get data for elements """
        self.data.set_time(time)
        final_data = self.data.element[param]
        return final_data

    def get_X_data(self, time):
        """ Get data for X axis """
        return self.get_element_data(time, 'X(m)')

    def get_Y_data(self, time):
        """ Get data for Y axis """
        return self.get_element_data(time, 'Y(m)')

    def get_Z_data(self, time):
        """ Get data for Z axis """
        return self.get_element_data(time, 'Z(m)')

    def getUniqueXData(self, timer):
        """ Get Unique X axis data """
        ori_array = self.get_coord_data('x', timer)
        indices_array = []
        for i in range(0, len(ori_array)):
            try:
                if ori_array[i] > ori_array[i + 1]:
                    indices_array.append(i)
                else:
                    continue
            except Exception:
                pass
        output_data = ori_array[0:indices_array[0] + 1]
        return output_data

    def getXStartPoints(self, timer):
        """ Get X axis Start Points"""
        ori_array = self.get_coord_data('x', timer)
        indices_array = []
        for i in range(0, len(ori_array)):
            try:
                if ori_array[i] > ori_array[i + 1]:
                    indices_array.append(i)
                else:
                    continue
            except Exception:
                pass
        return indices_array

    def getUniqueYData(self, timer):
        """ Get Unique Y axis data """
        ori_array = self.get_coord_data('y', timer)
        output = list(set(ori_array))
        return output

    def getUniqueZData(self, timer):
        """ Get Unique Z axis data """
        ori_array = self.get_coord_data('z', timer)
        output = list(set(ori_array))
        return output

    def getNumberOfLayers(self, direction):
        """ Get Number of Layers """
        if direction.lower() == 'x':
            array = self.getUniqueXData(0)
        elif direction.lower() == 'y':
            array = self.getUniqueYData(0)
        elif direction.lower() == 'z':
            array = self.getUniqueZData(0)
        else:
            print("coordinates can either be X, Y or Z")
        number = len(array)
        return number

    def getZLayerData(self, layer_number, param, timer):
        """ Get Data for Z (depth) layer """
        x_start = self.getXStartPoints(timer)
        z_data = self.get_element_data(timer, param)
        total_grid_in_z = self.getNumberOfLayers('z')
        if layer_number > 1:
            begin_index = x_start[layer_number - 2] + 1
        else:
            begin_index = 0
        if layer_number < total_grid_in_z:
            end_index = x_start[layer_number - 1] + 1
        else:
            end_index = 50
        z_data = self.get_element_data(timer, param)
        output = z_data[begin_index:end_index]
        return output

    def getXDepthData(self, line_number, param, timer):
        """ Get Data for X (depth) layer """
        element_data = self.get_element_data(timer, param)
        x_layers = self.getNumberOfLayers('x')
        z_layers = self.getNumberOfLayers('z')
        data_array = []
        for i in range(0, z_layers):
            data_array.append(element_data[line_number - 1])
            line_number = line_number + x_layers
        return data_array

    def getLayerData(self, direction, layer_number, timer, param):
        """ Get Data for Layers """
        number_of_layers = self.getNumberOfLayers(direction)
        if layer_number > number_of_layers:
            raise ValueError("The specified layer is more than the number of layers in the model")
        else:
            if direction.lower() == 'z':
                data_array = self.getZLayerData(layer_number, param, timer)
            elif direction.lower() == 'x':
                data_array = self.getXDepthData(layer_number, param, timer)
        return data_array

    def get_coord_data(self, direction, timer):
        """ Get Coordinate data """
        if direction.lower() == 'x':
            value = self.get_X_data(timer)
        elif direction.lower() == 'y':
            value = self.get_Y_data(timer)
        elif direction.lower() == 'z':
            value = self.get_Z_data(timer)
        else:
            print("coordinates can either be X, Y or Z")
        return value

    def get_unique_coord_data(self, direction, timer):
        """ Get Unique coordinate data """
        if direction.lower() == 'x':
            value = self.getUniqueXData(timer)
        elif direction.lower() == 'y':
            value = self.getUniqueYData(timer)
        elif direction.lower() == 'z':
            value = self.getUniqueZData(timer)
        else:
            print("coordinates can either be X, Y or Z")
        return value
