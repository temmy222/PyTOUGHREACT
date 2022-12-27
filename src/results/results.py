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
