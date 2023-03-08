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
from plotting.plot_tough_routine import PlotTough
from plotting.plot_multiple_tough_routine import PlotMultiTough
import constants.generalconstants as gc

class FileReadSingle(object):
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
        return 'Results from ' + self.filelocation + ' in ' + self.filetitle + ' for ' + self.simulatortype

    def validateFile(self):
        """ Validate File """
        if type(self.filelocation) != type(self.filetitle):
            print('Values can either be strings or lists')

    def getSimulatorType(self):
        """ Get Simulator Type """
        return self.simulatortype

    def plotTime(self, param, gridblocknumber, format_of_date='year', labels=None, singlePlot=False, style='horizontal',
                 width=12,
                 height=8):
        """ Make Plot of parameter with time """
        if isinstance(param, str):
            plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle, generation=self.generation,
                                 restart_files=self.full_args,
                                 experiment=self.expt)
            if self.full_args is None:
                plottest.plotParamWithTime(param, gridblocknumber, format_of_date)
            else:
                plottest.plotParamWithTimeRestart(param, gridblocknumber, format_of_date)
        elif isinstance(param, list) and isinstance(self.filelocation, str) and singlePlot is False:
            plottest = PlotMultiTough(self.simulatortype, self.filelocation, self.filetitle, generation=self.generation,
                                      restart_files=self.full_args,
                                      experiment=self.expt)
            if self.full_args is None:
                plottest.multi_time_plot(param, gridblocknumber, format_of_date, style)
            else:
                plottest.multi_time_plot_restart(param, gridblocknumber, format_of_date, style)
        elif isinstance(param, list) and isinstance(self.filelocation, str) and singlePlot is True:
            plottest = PlotMultiTough(self.simulatortype, self.filelocation, self.filetitle, generation=self.generation,
                                      restart_files=self.full_args,
                                      experiment=self.expt,
                                      x_slice_value=self.x_slice_value)
            if self.full_args is None:
                plottest.plotMultiParamSinglePlot(param, gridblocknumber, format_of_date, labels)

    def plotParamWithParam(self, param1, param2, gridblocknumber):
        """ Make Plot of parameter with parameter """
        plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle)
        plottest.plotParamWithParam(param1, param2, gridblocknumber)

    def plotParamWithLayer(self, directionXAxis, directionYAxis, param, layer_num, time):
        """ Make Plot of parameter with layer """
        plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle)
        plottest.plotParamWithLayer(directionXAxis, directionYAxis, param, layer_num, time)

    def plot2D(self, direction1, direction2, param, timer, grid_type='plain'):
        """ Make 2D plot either gridded or not gridded """
        plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle)
        if grid_type == 'plain':
            plottest.plot2D_one(direction1, direction2, param, timer)
        elif grid_type == 'grid':
            plottest.plot2D_withgrid(direction1, direction2, param, timer)
        else:
            print('Type can either be plain or grid')
