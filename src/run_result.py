import os
from results.result_tough_react import ResultReact
from results.result_single import FileReadSingle
from results.results import Results
import constants.generalconstants as gc


gridblocknumber = 0
result_2 = Results(simulatortype=gc.TOUGHREACT, filelocation=os.getcwd(), filetitle=gc.TOUGHREACT_CONC_FILE)
result = FileReadSingle(gc.TOUGHREACT, os.getcwd(), gc.TOUGHREACT_CONC_FILE)
result.plotTime('pH', 0)
print('correct')