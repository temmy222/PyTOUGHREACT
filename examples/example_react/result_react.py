import os
from pytoughreact.results.result_tough_react import ResultReact

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

results = ResultReact('toughreact', FILE_PATH, 'kdd_conc.tec')
time = results.get_times()
parameter_result = results.get_timeseries_data('pH', 0)
time_length = len(time)
parameter_result_length = len(parameter_result)
assert time_length == parameter_result_length
