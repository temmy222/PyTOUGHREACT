import os

from pytoughreact import t2chemical, t2react, t2solute, t2result, t2bio

react = t2react()
react.read('flow.inp')
writeChemical = t2chemical(t2reactgrid=react.grid)
writeSolute = t2solute(t2chemical=writeChemical)



writeChemical.read('chemical.inp')
writeSolute.read('solute.inp')

# react.run(simulator='treacteos.exe')
# results = t2result('toughreact', 'kdd_conc.tec')
# time = results.get_times('second')
# parameter_result = results.get_time_series_data('pH', 0)
# test2 = results.get_grid_data(5000, 'pH')

bio_read = t2bio()
bio_read.read('INFILE')
# bio_read.run(simulator='tmvoc')
results = t2result('tmvoc', 'OUTPUT_ELEME.csv')
time = results.get_times('second')
parameter_result = results.get_time_series_data('X_toluen_L', 0)


# results = t2result('toughreact', path, 'kdd_conc.tec')
# time = results.get_times('second')
# test = results.get_time_series_data('pH', 0)
# test2 = results.get_grid_data(5000,'pH' )
print('correct')