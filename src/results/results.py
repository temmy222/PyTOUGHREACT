import os
from results.result_multiple import FileReadMultiple
from results.result_single import FileReadSingle
from results.results_factory import ResultServiceProvider

class Results(object):
    def __init__(self, **kwargs):
        config = {
                    'simulator_type': kwargs.get('simulatortype'),
                    'file_locations': kwargs.get('filelocation'),
                    'file_titles': kwargs.get('filetitle'),
                    'props': kwargs.get('props'),
                    'x_slice_value': kwargs.get('x_slice_value'),
                    'per_file' : kwargs.get('per_file'),
                    'title' : kwargs.get('title')
                }
        services = ResultServiceProvider()
        services.register_helper('SingleFile', FileReadSingle(config['simulator_type'], config['file_locations'], config['file_titles']))


        # self.simulator_type = simulator_type
        # self.file_locations = file_locations
        # self.file_titles = file_titles
        # self.props = props
        self.x_slice_value = kwargs.get('x_slice_value')
        self.per_file = kwargs.get('per_file')
        self.title = kwargs.get('title')
        if len(self.file_locations) > 1:
            self.class_to_use = FileReadMultiple(self.simulator_type, self.file_locations, self.file_titles, self.props, **kwargs)
        elif len(self.file_locations) == 1:
            self.class_to_use = FileReadSingle(self.simulator_type, self.file_locations, self.file_titles, **kwargs)
