from pytoughreact.writers.chemical_writing import t2chemical
from pytoughreact.writers.react_writing import t2react
from pytoughreact.writers.solute_writing import t2solute

react = t2react()

react.read('flow.inp')
writeChemical = t2chemical(t2reactgrid=react.grid)
writeSolute = t2solute(t2chemical=writeChemical)


writeChemical.read('chemical.inp')
writeSolute.read('solute.inp')
print('yes')
