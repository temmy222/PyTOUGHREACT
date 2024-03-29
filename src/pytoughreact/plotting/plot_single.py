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


class PlotSingle(object):
    def __init__(self, simulatortype, filelocation, filetitle, **kwargs):
        """
        Class for processing single file results
        :type simulatortype: object
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
        return 'Results from ' + self.filelocation + ' in ' + self.filetitle \
            + ' for ' + self.simulatortype

    def _validateFile(self):
        """ Validate File """
        if type(self.filelocation) != type(self.filetitle):
            print('Values can either be strings or lists')

    def _getSimulatorType(self):
        """ Get Simulator Type """
        return self.simulatortype

    def plotTime(self, param, grid_block_number, format_of_date='year',
                 labels=None, singlePlot=False, style='horizontal',
                 width=12, height=8):
        """ General function for making line plot of parameter with time

        Parameters
        -----------
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        param :  str
            parameter to be plotted
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        labels : str
            labels of the plots to be done
        singlePlot : boolean
            Determines if there will be a single plot or multiple plots
        style : str
            orientation for multiple plots; could be horizontal or vertical
        width : int
            width of plot
        height : int
            height of plot


        Returns
        --------

        """
        if isinstance(param, str):
            plottest = PlotTough(self.simulatortype, self.filelocation,
                                 self.filetitle, generation=self.generation,
                                 restart_files=self.full_args,
                                 experiment=self.expt)
            if self.full_args is None:
                plottest.plotParamWithTime(param, grid_block_number,
                                           format_of_date)
            else:
                plottest.plotParamWithTimeRestart(param, grid_block_number,
                                                  format_of_date)
        elif (isinstance(param, list) and isinstance(self.filelocation, str)
              and singlePlot is False):
            plottest = PlotMultiTough(self.simulatortype, self.filelocation,
                                      self.filetitle,
                                      generation=self.generation,
                                      restart_files=self.full_args,
                                      experiment=self.expt)
            if self.full_args is None:
                plottest.multi_time_plot(param, grid_block_number,
                                         format_of_date, style)
            else:
                plottest.multi_time_plot_restart(param, grid_block_number,
                                                 format_of_date, style)
        elif (isinstance(param, list) and isinstance(self.filelocation, str)
              and singlePlot is True):
            plottest = PlotMultiTough(self.simulatortype, self.filelocation,
                                      self.filetitle,
                                      generation=self.generation,
                                      restart_files=self.full_args,
                                      experiment=self.expt,
                                      x_slice_value=self.x_slice_value)
            if self.full_args is None:
                plottest.plotMultiParamSinglePlot(param, grid_block_number,
                                                  format_of_date, labels)

    def plotParamWithParam(self, param1, param2, gridblocknumber):
        """ Line Plot of two parameters in the results file

        Parameters
        -----------
        param1 :  str
            The parameter to be plotted on the x-axis
        param2 :  str
            The parameter to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.

        Returns
        --------

        """
        """ Make Plot of parameter with parameter """
        plottest = PlotTough(self.simulatortype, self.filelocation,
                             self.filetitle)
        plottest.plotParamWithParam(param1, param2, gridblocknumber)

    def plotParamWithLayer(self, direction_x, direction_y, param, layer_num,
                           time):
        """ Make line plot of parameter at a particular time at a particular
        layer

        Parameters
        -----------
        direction_x :  str
            The direction to be plotted on the x axis
        direction_y :  str
            The direction to be plotted on the y axis
        param :  str
            parameter to be plotted
        layer_num :  int
            layer number to be plotted
        time : int
            the time at which the plot is to be made

        Returns
        --------

        """
        plottest = PlotTough(self.simulatortype, self.filelocation,
                             self.filetitle)
        plottest.plotParamWithLayer(direction_x, direction_y, param, layer_num,
                                    time)

    def plot2D(self, direction_x, direction_y, param, timer,
               grid_type='plain'):
        """ Make 2D plot of parameter at a particular time across the whole
        domain

        Parameters
        -----------
        direction_x :  str
            The direction to be plotted on the x axis
        direction_y :  str
            The direction to be plotted on the y axis
        param :  str
            parameter to be plotted
        grid_type :  str
            Specifies if plot should be gridded or not (options are 'plain' or
            'grid')
        timer : int
            the time at which the plot is to be made

        Returns
        --------

        """
        plottest = PlotTough(self.simulatortype, self.filelocation,
                             self.filetitle)
        if grid_type == 'plain':
            plottest.plot2D_one(direction_x, direction_y, param, timer)
        elif grid_type == 'grid':
            plottest.plot2D_withgrid(direction_x, direction_y, param, timer)
        else:
            print('Type can either be plain or grid')
