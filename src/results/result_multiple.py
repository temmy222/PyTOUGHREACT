from plotting.plot_multiple_files_routine import PlotMultiFiles

class FileReadMultiple(object):
    """
    Class for processing multiple file results
    file_locations (list of strings) - specifies the location of the files on the system
    file_titles (list of strings) - gives the title of the file e.g 'kdd.conc' or 'OUTPUT.csv
    simulator_type (string) can either be toughreact, tmvoc or tough3
    props (list of strings) -  are the properties to be plotted

    **kwargs
    x_slice value (integer) - if the plot should be sliced a the  x axis
    per_file -  (boolean) - if the plot should be made per file and not per property
    title (list of strings) - title of each of the plots
    """

    def __init__(self, simulator_type, file_locations, file_titles, props, **kwargs):
        assert isinstance(file_locations, list)
        assert isinstance(file_titles, list)
        self.file_locations = file_locations
        self.file_titles = file_titles
        self.simulator_type = simulator_type
        self.props = props
        self.x_slice_value = kwargs.get('x_slice_value')
        self.per_file = kwargs.get('per_file')
        self.title = kwargs.get('title')

    def plotTime(self, grid_block_number, legend, plot_kind='property', format_of_date='day'):
        # TODO write code to slice x axis
        # TODO write code to slice through domain

        """

        :param format_of_date:
        :param grid_block_number: grid block number in mesh
        :type grid_block_number: int
        :param legend:
        :type legend: list
        :param plot_kind:
        :type plot_kind: string
        """
        plottest = PlotMultiFiles(self.simulator_type, self.file_locations, self.file_titles, self.props,
                                  x_slice_value=self.x_slice_value, per_file=self.per_file, title=self.title)
        if len(self.props) == 1:
            plottest.multiFileSinglePlot(grid_block_number, legend)
        else:
            plottest.plotMultiElementMultiFile(grid_block_number, legend, format_of_date, plot_kind)

    def plotTimePerPanel(self, grid_block_number, panels, format_of_date='day'):
        plottest = PlotMultiFiles(self.simulator_type, self.file_locations, self.file_titles, self.props,
                                  x_slice_value=self.x_slice_value, per_file=self.per_file, title=self.title)
        plottest.plotMultiPerPanel(grid_block_number, panels, format_of_date)

    def plotParamWithLayer(self, directionX, directionY, layer_num, time, legend):
        plottest = PlotMultiFiles(self.simulator_type, self.file_locations, self.file_titles, self.props,
                                  x_slice_value=self.x_slice_value, per_file=self.per_file, title=self.title)
        if len(self.props) == 1:
            pass
        else:
            plottest.plotMultiFileDistance(directionX, directionY, time, layer_num, legend)
