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
from pytoughreact.utilities.t2_utilities import t2Utilities
from pytoughreact.utilities.t2_tough_react_utilities import t2UtilitiesToughReact
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
        find_connection = t2UtilitiesToughReact(self.filelocation, 'CONNE')
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
        value = t2Utilities()
        if len(time_data2) > 15:
            time_data = value.choplist(time_data2, 15)
            return time_data
        return time_data2

    def convert_times(self, format_of_date):
        """ Convert time to required format """
        get_times = self.get_times()
        utility_class = t2Utilities()
        timeyear = utility_class.convert_times(get_times, format_of_date)
        return timeyear

    def get_timeseries_data(self, param, gridblocknumber):
        """ Get timeseries data """
        os.chdir(self.filelocation)
        grid = self.get_elements()[gridblocknumber]
        mf = self.data.history([(grid, param)])
        timeseries = mf[1]
        timeseries = list(timeseries)
        value = t2Utilities()
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
        if len(indices_array) > 0:
            output_data = ori_array[0:indices_array[0] + 1]
        else:
            output_data = ori_array
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
from pytoughreact.utilities.t2_utilities import t2Utilities
from pytoughreact.utilities.t2_tough_react_utilities import t2UtilitiesToughReact
import t2listing


class ResultReact(object):
    def __init__(self, simulatortype, filelocation, filetitle):
        """
        Class for processing results from TOUGHREACT

        Parameters
        -----------
        file_location :  str
            specifies the location of the files on the syste
        file_title : str
            gives the title of the file e.g 'kdd.conc'.
        simulator_type: str
            can either be toughreact
        
        
        Returns
        --------

        """
        self.filelocation = filelocation
        os.chdir(self.filelocation)
        self.filetitle = filetitle
        self.simulatortype = simulatortype
        self.data = t2listing.toughreact_tecplot(self.filetitle, self._get_elements())

    def __repr__(self):
        return 'Results from ' + self.filelocation + ' in ' + self.filetitle + ' for ' + self.simulatortype

    def _getParameters(self):
        """
        Class for processing results from TOUGHREACT

        Parameters
        -----------
        
        
        Returns
        --------

        """
        return self.data.element.column_name

    def _get_elements(self):
        """
        Get elements from the output file

        Parameters
        -----------
        
        
        Returns
        --------
        grid_blocks: list[str]
            list of all grid blocks

        """
        find_connection = t2UtilitiesToughReact(self.filelocation, 'CONNE')
        find_connection.findword()
        find_connection.sliceoffline()
        find_connection.writetofile()
        with open('test.txt') as f:
            grid_blocks = f.read().splitlines()
        return grid_blocks

    def get_times(self):
        """
        Get times from data file 

        Parameters
        -----------
        
        
        Returns
        --------
        time_data: list[int]
            list of all time

        """
        time_data = self.data.times
        time_data2 = list(time_data)
        value = t2Utilities()
        if len(time_data2) > 15:
            time_data = value.choplist(time_data2, 15)
            return time_data
        return time_data2

    def convert_times(self, format_of_date):
        """
        Convert time to required 

        Parameters
        -----------
        
        
        Returns
        --------
        timeyear: list[int]
            list of all converted time

        """
        get_times = self.get_times()
        utility_class = t2Utilities()
        timeyear = utility_class.convert_times(get_times, format_of_date)
        return timeyear

    def get_timeseries_data(self, param, grid_block_number):
        """
        Get timeseries data

        Parameters
        -----------
        grid_block_number : int
            the grid block in which its data is to be gotten.
        param :  str
            The parameter in which the data is to be gotten
        
        
        Returns
        --------
        timeseries: list[int]
            list of all time

        """
        os.chdir(self.filelocation)
        grid = self._get_elements()[grid_block_number]
        data_history = self.data.history([(grid, param)])
        timeseries = data_history[1]
        timeseries = list(timeseries)
        value = t2Utilities()
        if len(timeseries) > 15:
            timeseries = value.choplist(timeseries, 15)
            return timeseries
        return timeseries

    def get_element_data(self, time, param):
        """
        Get data for elements

        Parameters
        -----------
        time : int
            time for which element data is to be gotten.
        param :  str
            The parameter in which the data is to be gotten
        
        
        Returns
        --------
        final_data: array[float]
            array of all value of parameter at that time

        """
        self.data.set_time(time)
        final_data = self.data.element[param]
        return final_data

    def _get_X_data(self, time):
        """
        Get data for X axis 

        Parameters
        -----------
        time : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        output: list[str]
            list of all elements in X direction

        """
        return self.get_element_data(time, 'X(m)')

    def _get_Y_data(self, time):
        """
        Get data for Y axis

        Parameters
        -----------
        time : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        output: list[str]
            list of all elements in Y direction

        """
        return self.get_element_data(time, 'Y(m)')

    def _get_Z_data(self, time):
        """
        Get data for Z axis

        Parameters
        -----------
        time : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        output: list[str]
            list of all elements in Z direction

        """
        return self.get_element_data(time, 'Z(m)')

    def getUniqueXData(self, timer):
        """
        Get Unique X axis data

        Parameters
        -----------
        timer : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        output_data: list[str]
            list of all unique elements in X direction

        """
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
        if len(indices_array) > 0:
            output_data = ori_array[0:indices_array[0] + 1]
        else:
            output_data = ori_array
        return output_data

    def getXStartPoints(self, timer):
        """
        Get X axis Start Points

        Parameters
        -----------
        timer : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        indices_array: list[int]
            list of all start points in X axis

        """
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
        """
        Get Unique Y axis data

        Parameters
        -----------
        timer : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        output: list[int]
            list of all unique Y data

        """
        ori_array = self.get_coord_data('y', timer)
        output = list(set(ori_array))
        return output

    def getUniqueZData(self, timer):
        """
        Get Unique Z axis data

        Parameters
        -----------
        timer : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        output: list[int]
            list of all unique Z data

        """
        ori_array = self.get_coord_data('z', timer)
        output = list(set(ori_array))
        return output

    def getNumberOfLayers(self, direction):
        """
        Get Number of Layers

        Parameters
        -----------
        direction : str
            direction to which to retrieve the number of layers.
        
        
        Returns
        --------
        number: int
            number of layers

        """
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
        """
        Get Data for Z (depth) layer

        Parameters
        -----------
        layer_number : int
            the layer to retrieve Z layer data.
        param : str
            the parameter for which the parameter is to be retrieved.
        timer : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        output: list[int]
            list of Z Layer data

        """
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
        """
        Get Data for X (depth) layer

        Parameters
        -----------
        line_number : int
            the line to retrieve X Depth data.
        param : str
            the parameter for which the data is to be retrieved.
        timer : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        data_array: list[int]
            list of X Depth data

        """
        element_data = self.get_element_data(timer, param)
        x_layers = self.getNumberOfLayers('x')
        z_layers = self.getNumberOfLayers('z')
        data_array = []
        for i in range(0, z_layers):
            data_array.append(element_data[line_number - 1])
            line_number = line_number + x_layers
        return data_array

    def getLayerData(self, direction, layer_number, timer, param):
        """
        Get Data for Layers

        Parameters
        -----------
        direction : str
            the direction to retrieve layer data.
        layer_number : int
            layer number to retrieve layer data.
        timer : int
            time for which element data is to be gotten.
        param : str
            the parameter for which the data is to be retrieved.
        
        
        Returns
        --------
        data_array: list[int]
            list of Layer data

        """
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
        """
        Get Coordinate data

        Parameters
        -----------
        direction : str
            the direction to retrieve layer data.
        timer : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        value: list[int]
            list of coordinate data

        """
        if direction.lower() == 'x':
            value = self._get_X_data(timer)
        elif direction.lower() == 'y':
            value = self._get_Y_data(timer)
        elif direction.lower() == 'z':
            value = self._get_Z_data(timer)
        else:
            print("coordinates can either be X, Y or Z")
        return value

    def get_unique_coord_data(self, direction, timer):
        """
        Get Unique Coordinate data

        Parameters
        -----------
        direction : str
            the direction to retrieve layer data.
        timer : int
            time for which element data is to be gotten.
        
        
        Returns
        --------
        value: list[int]
            list of unique coordinate data

        """
        if direction.lower() == 'x':
            value = self.getUniqueXData(timer)
        elif direction.lower() == 'y':
            value = self.getUniqueYData(timer)
        elif direction.lower() == 'z':
            value = self.getUniqueZData(timer)
        else:
            raise ValueError("coordinates can either be X, Y or Z")
        return value
