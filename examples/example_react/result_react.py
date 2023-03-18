import os
from pytoughreact.results.result_tough_react import ResultReact
from pytoughreact.results.t2result import t2result

FILE_PATH = os.path.abspath(os.curdir)

results = t2result('toughreact', 'kdd_conc.tec', FILE_PATH)
time = results.get_times()
parameter_result = results.get_time_series_data('pH', 0)
print('yes')


# results = ResultReact('toughreact', FILE_PATH, 'kdd_conc.tec')
# time = results.get_times()
# parameter_result = results.get_timeseries_data('pH', 0)
# time_length = len(time)
# parameter_result_length = len(parameter_result)
# assert time_length == parameter_result_length
