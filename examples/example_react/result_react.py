import os
from pytoughreact.results.result_tough_react import ResultReact
from pytoughreact.results.t2result import T2Result
from pytoughreact.plotting.plot_multiple import PlotMultiple
from pytoughreact.plotting.plot_single import PlotSingle
from pytoughreact.plotting.plot_tough_routine import PlotTough

FILE_PATH = os.path.abspath(os.curdir)

results = T2Result('toughreact', 'kdd_conc.tec', FILE_PATH)
results_tmvoc = T2Result('tmvoc', 'OUTPUT_ELEME.csv', FILE_PATH)
time = results.get_times()
parameter_result = results.get_time_series_data('pH', 0)
time = results_tmvoc.get_times()
parameter_result = results_tmvoc.get_time_series_data('X_WATER_N', 0)

pt = PlotTough('toughreact', FILE_PATH, 'kdd_conc.tec')
# pt.plot2D_withgrid('x', 'z', 'pH', 3000)
# pt.plot2D_one('x', 'z', 'pH', 3000)
# pt.plotParamWithLayer('x', 'z', ['pH'], 1, 300)
# pt.plotParamWithTime('pH', 0, 'day')
# pt.plotParamWithParam('pH', 't_so4-2', 0)


file_toughreact = os.path.join(FILE_PATH, "example_files/folder_1")
file_toughreact2 = os.path.join(FILE_PATH, "example_files/folder_2")
file_toughreact3 = os.path.join(FILE_PATH, "example_files/folder_3")
all_toughreact_files = [file_toughreact, file_toughreact2, file_toughreact3]

filetype_toughreact = 'kdd_conc.tec'
filetype_toughreact_min = 'kdd_min.tec'
all_toughreact_filetypes = [filetype_toughreact, filetype_toughreact, filetype_toughreact, filetype_toughreact]

params2 = ['pH', 't_na+', 't_cl-', 't_ca+2']
params2 = ['pH', 't_h2o', 't_h+', 't_na+']
params3 = ['pH', 't_h2o']
param_min = ['portlandite', 'calcite']
labels = ['first plot', 'second plot', 'third plot', 'fourth plot']

testcodemultitoughreact = PlotMultiple("toughreact", all_toughreact_files, all_toughreact_filetypes, params2)
testcodetoughreact = PlotSingle("toughreact", file_toughreact, filetype_toughreact)
testcodetoughreact_min = PlotSingle("toughreact", file_toughreact, filetype_toughreact_min)

# testcodetoughreact_min.plot2D('x', 'z', 'calcite', 2.592e+15, 'grid')
# testcodetoughreact.plotTime('pH', 85, format_of_date='day')
testcodetoughreact_min.plot_time(param_min, 85, format_of_date='day')

testcodemultitoughreact.plot_time(0, labels)

results = ResultReact('toughreact', FILE_PATH, 'kdd_conc.tec')
time = results.get_times()
parameter_result = results.get_timeseries_data('pH', 0)
