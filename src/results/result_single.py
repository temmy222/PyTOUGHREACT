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
        if type(self.filelocation) != type(self.filetitle):
            print('Values can either be strings or lists')

    def getSimulatorType(self):
        return self.simulatortype

    def plotTime(self, param, gridblocknumber, format_of_date='year', labels=None, singlePlot=False, style='horizontal',
                 width=12,
                 height=8):
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
        plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle)
        plottest.plotParamWithParam(param1, param2, gridblocknumber)

    def plotParamWithLayer(self, directionXAxis, directionYAxis, param, layer_num, time):
        plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle)
        plottest.plotParamWithLayer(directionXAxis, directionYAxis, param, layer_num, time)

    def plot2D(self, direction1, direction2, param, timer, grid_type='plain'):
        plottest = PlotTough(self.simulatortype, self.filelocation, self.filetitle)
        if grid_type == 'plain':
            plottest.plot2D_one(direction1, direction2, param, timer)
        elif grid_type == 'grid':
            plottest.plot2D_withgrid(direction1, direction2, param, timer)
        else:
            print('Type can either be plain or grid')


config = {
    'spotify_client_key': 'THE_SPOTIFY_CLIENT_KEY',
    'spotify_client_secret': 'THE_SPOTIFY_CLIENT_SECRET',
    'pandora_client_key': 'THE_PANDORA_CLIENT_KEY',
    'pandora_client_secret': 'THE_PANDORA_CLIENT_SECRET',
    'local_music_location': '/usr/data/music'
}

class SingleFileService(object):
    def __init__(self):
        self._instance = None

    def __call__(self, simulatortype, filelocation, filetitle, **_ignored):
        if not self._instance:
            consumer_key, consumer_secret = self.authorize(pandora_client_key, pandora_client_secret)
            self._instance = PandoraService(consumer_key, consumer_secret)
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'