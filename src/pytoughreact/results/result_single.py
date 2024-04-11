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
from pytoughreact.plotting.plot_tough_routine import PlotTough
from pytoughreact.plotting.plot_multiple_tough_routine import PlotMultiTough
import pytoughreact.constants.generalconstants as gc


class FileReadSingle(object):
    """Class for processing single file results"""
    def __init__(self, simulatortype, filelocation, filetitle, **kwargs):
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
            2) restart_files  (list[string]) - if restart files exist in the results
            3) experiment (list[strings]) - location of experiment results if available
            4) x_slice_value (integer) - if the plot should be sliced on the  x axis


        Returns
        --------

        """
        self.filelocation = filelocation
        if isinstance(self.filelocation, str):
            os.chdir(self.filelocation)
        self.filetitle = filetitle
        self.simulatortype = simulatortype
        self.generation = kwargs.get(gc.GENERATION)
        self.full_args = kwargs.get(gc.RESTART_FILES)
        self.expt = kwargs.get(gc.EXPERIMENT)
        self.x_slice_value = kwargs.get(gc.X_SLICE_VALUE)

    def __repr__(self):
        return 'Results from ' + self.filelocation + ' in ' + self.filetitle + ' for ' + self.simulatortype

    def validate_file(self):
        """ Validate File

        Parameters
        -----------


        Returns
        --------

        """
        if type(self.filelocation) != type(self.filetitle):
            print('Values can either be strings or lists')

    def get_simulator_type(self):
        """ Get Simulator Type

        Parameters
        -----------


        Returns
        --------

        """
        return self.simulatortype

    def plot_time(self, param, gridblocknumber, format_of_date='year', labels=None, single_plot=False,
                  style='horizontal', width=12, height=8):
        """ Make Plot of parameter with time

        Parameters
        -----------
        grid_block_number : int
            The grid block number in mesh for which to retrieve the results
        param: string
            Parameter to be plotted
        format_of_date : string
            Provides information to the method on format of the date. For example. year, hour, min or seconds
        labels : string
            Labels for the plot (Title)
        singlePlot : boolean
            If single plot should be made or multiple plots
        style : string
            Orientation of plot (should be 'vertical' or 'horizontal)
        width : int
            width of plot
        height : int
            height of plot

        Returns
        --------

        """
        if isinstance(param, str):
            plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle, generation=self.generation,
                                 restart_files=self.full_args,
                                 experiment=self.expt)
            if self.full_args is None:
                plottest.plot_param_with_time(param, gridblocknumber, format_of_date)
            else:
                plottest.plot_param_with_time_restart(param, gridblocknumber, format_of_date)
        elif isinstance(param, list) and isinstance(self.filelocation, str) and single_plot is False:
            plottest = PlotMultiTough(self.simulatortype, self.filelocation, self.filetitle, generation=self.generation,
                                      restart_files=self.full_args,
                                      experiment=self.expt)
            if self.full_args is None:
                plottest.multi_time_plot(param, gridblocknumber, format_of_date, style)
            else:
                plottest.multi_time_plot_restart(param, gridblocknumber, format_of_date, style)
        elif isinstance(param, list) and isinstance(self.filelocation, str) and single_plot is True:
            plottest = PlotMultiTough(self.simulatortype, self.filelocation, self.filetitle, generation=self.generation,
                                      restart_files=self.full_args,
                                      experiment=self.expt,
                                      x_slice_value=self.x_slice_value)
            if self.full_args is None:
                plottest.plot_multi_param_single_plot(param, gridblocknumber, format_of_date, labels)

    def plot_param_with_param(self, param1, param2, gridblocknumber):
        """ Make Plot of parameter with parameter

        Parameters
        -----------
        grid_block_number : int
            The grid block number in mesh for which to retrieve the results
        param1: string
            First Parameter to be plotted on x axis
        param2: string
            Second Parameter to be plotted on x axis


        Returns
        --------

        """
        plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle)
        plottest.plot_param_with_param(param1, param2, gridblocknumber)

    def plot_param_with_layer(self, direction_x_axis, direction_y_axis, param, layer_num, time):
        """ Make Plot of parameter with layer

        Parameters
        -----------
        direction_x_axis : string
            Direction to be plotted on the X axis. Can be 'X', 'Y', 'Z'
        direction_y_axis : string
            Direction to be plotted on the Y axis. Can be 'X', 'Y', 'Z'
        param: string
            Parameter to be plotted
        layer_num: int
            Layer number in which to retrieve data
        time : float
            Time in which the data should be retrieved.

        Returns
        --------

        """
        plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle)
        plottest.plot_param_with_layer(direction_x_axis, direction_y_axis, param, layer_num, time)

    def plot_2d(self, direction1, direction2, param, timer, grid_type='plain'):
        """ Make 2D plot either gridded or not gridded

        Parameters
        -----------
        direction1 : string
            Direction to be plotted on the X axis. Can be 'X', 'Y', 'Z'
        direction2 : string
            Direction to be plotted on the Y axis. Can be 'X', 'Y', 'Z'
        param : string
            Parameter to be plotted
        grid_type : string
            Shows if plot should contain grids or not. Options are 'grid' and 'plain'
        timer : float
            Time in which the data should be retrieved.

        Returns
        --------

        """
        plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle)
        if grid_type == 'plain':
            plottest.plot_2d_one(direction1, direction2, param, timer)
        elif grid_type == 'grid':
            plottest.plot_2d_with_grid(direction1, direction2, param, timer)
        else:
            print('Type can either be plain or grid')
