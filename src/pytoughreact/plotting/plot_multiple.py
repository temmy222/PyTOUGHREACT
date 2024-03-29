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

from pytoughreact.plotting.plot_multiple_files_routine import PlotMultiFiles


class PlotMultiple(object):
    def __init__(self, simulator_type, file_locations, file_titles, props,
                 **kwargs):
        """
        Class for processing multiple file results

        Parameters
        -----------
        file_locations :  list[str]
            specifies the location of the files on the syste
        file_titles : list[str]
            gives the title of the file e.g 'kdd.conc' or 'OUTPUT.csv'.
        simulator_type: str
            can either be toughreact, tmvoc or tough3
        prop : list[str]
            properties to be plotted

        **kwargs

        x_slice value : int
            value at which the plot should be sliced at the  x axis
        per_file : boolean
            if the plot should be made per file and not per property
        tile : str
            title of each of the plots


        Returns
        --------

        """
        assert isinstance(file_locations, list)
        assert isinstance(file_titles, list)
        self.file_locations = file_locations
        self.file_titles = file_titles
        self.simulator_type = simulator_type
        self.props = props
        self.x_slice_value = kwargs.get('x_slice_value')
        self.per_file = kwargs.get('per_file')
        self.title = kwargs.get('title')

    def plotTime(self, grid_block_number, legend, plot_kind='property',
                 format_of_date='day'):
        """ Line Plots of a parameter in the results file as a function of time

        Parameters
        -----------
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        legend: list[str]
            List of all legend values
        plot_kind: str
            if plot should be structured by property or file


        Returns
        --------

        """
        plottest = PlotMultiFiles(self.simulator_type, self.file_locations,
                                  self.file_titles, self.props,
                                  x_slice_value=self.x_slice_value,
                                  per_file=self.per_file, title=self.title)
        if len(self.props) == 1:
            plottest.multiFileSinglePlot(grid_block_number, legend)
        else:
            plottest.plotMultiElementMultiFile(grid_block_number, legend,
                                               format_of_date, plot_kind)

    def plotTimePerPanel(self, grid_block_number, panels,
                         format_of_date='day'):
        """ Plot Multiple plots in a panel

        Parameters
        -----------
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        panels: list[str]
            List of all panels


        Returns
        --------

        """
        plottest = PlotMultiFiles(self.simulator_type, self.file_locations,
                                  self.file_titles, self.props,
                                  x_slice_value=self.x_slice_value,
                                  per_file=self.per_file, title=self.title)
        plottest.plotMultiPerPanel(grid_block_number, panels, format_of_date)

    def plotParamWithLayer(self, direction_x, direction_y, layer_num, time,
                           legend):
        """ Plot of Parameter with Layer

        Parameters
        -----------
        direction_x :  str
            The direction to be plotted on the x axis
        direction_y :  str
            The direction to be plotted on the y axis
        legend :  list[str]
            List of legend values
        layer_num :  int
            The layer in the model to be plotted
        time : int
            the time at which the plot is to be made

        Returns
        --------

        """
        plottest = PlotMultiFiles(self.simulator_type, self.file_locations,
                                  self.file_titles, self.props,
                                  x_slice_value=self.x_slice_value,
                                  per_file=self.per_file, title=self.title)
        if len(self.props) == 1:
            pass
        else:
            plottest.plotMultiFileDistance(direction_x, direction_y, time,
                                           layer_num, legend)
