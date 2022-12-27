import os
from results.result_tough_react import ResultReact
from results.result_single import FileReadSingle
from results.results import Results
import constants.generalconstants as gc

filetype_tmvoc = "OUTPUT_ELEME.csv"
read_file2 = FileReadSingle("tmvoc", os.getcwd(), filetype_tmvoc)
read_file2.plot2D('x', 'z', 'X_toluen_L', 2.59e+10, grid_type='grid')
read_file2.plotTime(
    ['X_toluen_L', 'X_O2_L','BIO1'], 0,
    labels=['Toluene', 'Oxygen', 'Biomass'],
    singlePlot=True, format_of_date='day')