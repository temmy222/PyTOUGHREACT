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
import numpy as np
import csv
import collections
import itertools
import pandas as pd
from utilities.synergy_general_utilities import SynergyUtilities


class ResultTough3(object):
    """ Class for processing results from Tough3 """
    def __init__(self, simulatortype, filelocation, filetitle=None, **kwargs):
        if filelocation is None:
            self.filelocation = os.getcwd()
        else:
            self.filelocation = filelocation
            os.chdir(self.filelocation)
        self.filetitle = filetitle
        self.simulatortype = simulatortype
        self.generation = kwargs.get('generation')
        self.file_as_list = []

    def __repr__(self):
        return 'Results from ' + self.filelocation + ' in ' + self.filetitle + ' for ' + self.simulatortype

    def read_file(self):
        """ Read file """
        os.chdir(self.filelocation)
        with open(self.filetitle) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            self.file_as_list = []
            for row in csv_reader:
                self.file_as_list.append(row)
        return self.file_as_list

    def get_times(self):
        """
        get times stored for duration of the simulation
        :return: a list of all times
        """
        self.read_file()
        time = []
        timeraw = []
        if self.generation is True:
            for i in range(1, len(self.file_as_list)):
                timeraw.append(float(self.file_as_list[i][0]))
        else:
            for i in range(len(self.file_as_list)):
                if len(self.file_as_list[i]) == 1:
                    time.append(self.file_as_list[i])
            for i in range(len(time)):
                interim = time[i][0].split()
                timeraw.append(float(interim[2]))
        return timeraw

    def convert_times(self, format_of_date):
        """
        convert time to desirable time e.g day, month, year
        :param format_of_date: string of type 'day', 'month', 'year'
        :return: a list of the time
        """
        intermediate = self.get_times()
        utility_function = SynergyUtilities()
        timeyear = utility_function.convert_times(intermediate, format_of_date)
        return timeyear

    def get_time_index(self):
        """ Get Index of Time """
        self.read_file()
        indextime = []
        for index, value in enumerate(self.file_as_list):
            if len(self.file_as_list[index]) == 1:
                indextime.append(index)
        indextime.append(len(self.file_as_list))
        return indextime

    def getGenerationData(self, param):
        """ Get Data from GENER file """
        self.read_file()
        resultarray = []
        heading = []
        heading_first = self.file_as_list[0]
        heading_first_modify = []
        for i in heading_first:
            heading_first_modify.append(i.upper())
        for i in range(len(heading_first_modify)):
            heading.append(heading_first_modify[i].lstrip())
        index_param = heading.index(param.upper())
        for i in range(1, len(self.file_as_list)):
            resultarray.append(float(self.file_as_list[i][index_param]))
        return resultarray

    def get_elements(self):
        """ Get elements from the simulation """
        self.read_file()
        indextime = self.get_time_index()
        temp_file = self.file_as_list[indextime[0] + 1:indextime[1]]
        elements = []
        for i in range(len(temp_file)):
            elements.append(temp_file[i][0])
        return elements

    def getParameters(self):
        """ Remove space from parameters """
        self.read_file()
        full_list = self.file_as_list[0]
        for i in range(len(full_list)):
            full_list[i] = full_list[i].replace(" ", "")
        return full_list

    def resultdict(self):
        self.read_file()
        resultdict = {}
        tempdict = {}
        indextime = self.get_time_index()
        timeraw = self.get_times()
        for i in range(len(indextime) - 1):
            tempdict[i] = self.file_as_list[indextime[i] + 1:indextime[i + 1]]
        for i in range(len(timeraw)):
            resultdict[timeraw[i]] = tempdict[i]
        return resultdict

    def get_timeseries_data(self, param, gridblocknumber):
        """ Get Time series data"""
        self.read_file()
        results = self.resultdict()
        resultarray = []
        heading = []
        heading_first = self.file_as_list[0]
        heading_first_modify = []
        for i in heading_first:
            heading_first_modify.append(i.upper())
        for i in range(len(heading_first_modify)):
            heading.append(heading_first_modify[i].lstrip())
        index_param = heading.index(param.upper())
        for k in results.keys():
            resultarray.append(results[k][gridblocknumber][index_param].lstrip())
        final_data = [float(x) for x in resultarray]
        return final_data

    def get_element_data(self, time, param):
        """ Get Data for elements """
        self.read_file()
        timeraw = self.get_times()
        results = self.resultdict()
        heading = []
        heading_first = self.file_as_list[0]
        heading_first_modify = []
        for i in heading_first:
            heading_first_modify.append(i.upper())
        for i in range(len(heading_first_modify)):
            heading.append(heading_first_modify[i].lstrip())
        index_param = heading.index(param.upper())
        if time < timeraw[0]:
            time = timeraw[0]
        elif time > timeraw[-1]:
            time = timeraw[-1]
        else:
            absolute_difference_function = lambda list_value: abs(list_value - time)
            time = min(timeraw, key=absolute_difference_function)
        results_specific = results[time]
        data = []
        for i in range(len(results_specific)):
            data.append(results_specific[i][index_param].lstrip())
        final_data = [float(x) for x in data]
        return final_data

    def get_X_data(self, time):
        """ Get X Axis Data """
        return self.get_element_data(time, 'x')

    def get_Y_data(self, time):
        """ Get Y Axis Data """
        return self.get_element_data(time, 'y')

    def get_Z_data(self, time):
        """ Get Z Axis Data """
        return self.get_element_data(time, 'z')

    def get_coord_data(self, direction, timer):
        """ Get Coordinate Data """
        if direction.lower() == 'x':
            value = self.get_X_data(timer)
        elif direction.lower() == 'y':
            value = self.get_Y_data(timer)
        elif direction.lower() == 'z':
            value = self.get_Z_data(timer)
        else:
            print("coordinates can either be X, Y or Z")
        return value

    def getUniqueXData(self, timer):
        """ Get Unique X Axis Data """
        ori_array = self.get_coord_data('x', timer)
        indices_array = []
        for i in range(0, len(ori_array)):
            try:
                if ori_array[i] > ori_array[i + 1]:
                    indices_array.append(i)
                else:
                    continue
            except:
                pass
        output_data = ori_array[0:indices_array[0] + 1]
        return output_data

    def getXStartPoints(self, timer):
        """ Get X Axis Start Point Data """
        original_array = self.get_coord_data('x', timer)
        indices_array = []
        for i in range(0, len(original_array)):
            try:
                if original_array[i] > original_array[i + 1]:
                    indices_array.append(i)
                else:
                    continue
            except:
                pass
        # output_data = ori_array[0:indices_array[0] + 1]
        return indices_array

    def getUniqueYData(self, timer):
        """ Get Unique Y Axis Data """
        ori_array = self.get_coord_data('y', timer)
        output = list(set(ori_array))
        return output

    def getUniqueZData(self, timer):
        """ Get Unique Z Axis Data """
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
        """ Get Z Layer Data """
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
        output = z_data[begin_index:end_index]
        return output

    def getXDepthData(self, line_number, param, timer):
        """ Get X Axis And Depth Data """
        element_data = self.get_element_data(timer, param)
        x_layers = self.getNumberOfLayers('x')
        z_layers = self.getNumberOfLayers('z')
        data_array = []
        for i in range(0, z_layers):
            data_array.append(element_data[line_number - 1])
            line_number = line_number + x_layers
        return data_array

    def getLayerData(self, direction, layer_number, timer, param):
        """ Get Layer Data """
        number_of_layers = self.getNumberOfLayers(direction)
        if layer_number > number_of_layers:
            raise ValueError("The specified layer is more than the number of layers in the model")
        else:
            if direction.lower() == 'z':
                data_array = self.getZLayerData(layer_number, param, timer)
            elif direction.lower() == 'x':
                data_array = self.getXDepthData(layer_number, param, timer)
        return data_array

    def get_unique_coord_data(self, direction, timer):
        """ Get Unique Coordinate Data """
        if direction.lower() == 'x':
            value = self.getUniqueXData(timer)
        elif direction.lower() == 'y':
            value = self.getUniqueYData(timer)
        elif direction.lower() == 'z':
            value = self.getUniqueZData(timer)
        else:
            print("coordinates can either be X, Y or Z")
        return value

    def remove_non_increasing(self, seqA, seqB):
        """ Remove Non Increasing Data """
        monotone = self.check_strictly_increasing(seqA)
        if not monotone:
            index = self.duplicate_index(seqA)
            if len(index) > 0:
                seqA = self.del_index(seqA, index)
            indexes1 = self.duplicate_index(seqB)
            if len(seqA) != len(seqB):
                if len(indexes1) > 0:
                    seqB = self.del_index(seqB, indexes1)
        return seqA, seqB

    def check_strictly_increasing(self, sequence):
        """ Check for only strictly increasing data """
        dx = np.diff(sequence)
        return np.all(dx > 0)

    def del_index(self, my_list, indexes):
        """ Delete index """
        for index in sorted(indexes, reverse=True):
            del my_list[index]
        return my_list

    def duplicate_index(self, sequence):
        """ Duplicate index """
        dicta = {}
        indexes = []
        dups = collections.defaultdict(list)
        for i, e in enumerate(sequence):
            dups[e].append(i)
        for k, v in sorted(dups.items()):
            if len(v) >= 2:
                dicta[k] = v
        for k, v in dicta.items():
            indexes.append(v[1:])
        return list(itertools.chain.from_iterable(indexes))


