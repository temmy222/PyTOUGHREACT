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
from mulgrids import mulgrid
from pytoughreact.writers.react_writing import t2react
from pytoughreact.wrapper.reactgrid import t2reactgrid
from pytoughreact.wrapper.reactzone import t2zone
from pytoughreact.chemical.chemical_composition import PrimarySpecies, WaterComp, Water, ReactGas
from pytoughreact.chemical.mineral_composition import MineralComp
from pytoughreact.chemical.mineral_zone import MineralZone
from pytoughreact.constants.default_minerals import get_kinetics_minerals, get_specific_mineral
from pytoughreact.writers.chemical_writing import t2chemical
from pytoughreact.chemical.perm_poro_zone import PermPoro, PermPoroZone
from pytoughreact.writers.solute_writing import t2solute
from t2grids import rocktype

# __________________________________FLOW.INP______________________________________________________
length = 0.1
nblks = 1
dx = [length / nblks] * nblks
dy = [0.5]
dz = [0.5] * 1
geo = mulgrid().rectangular(dx, dy, dz)
geo.write('geom.dat')

react = t2react()
react.title = 'Reaction example'

react.multi = {'num_components': 1, 'num_equations': 1, 'num_phases': 2,
               'num_secondary_parameters': 6}

react.grid = t2reactgrid().fromgeo(geo)

react.parameter.update(
    {'print_level': 4,
     'max_timesteps': 9999,
     'tstop': 8640,
     'const_timestep': 10.,
     'print_interval': 1,
     'gravity': 9.81,
     'relative_error': 1e-5,
     'phase_index': 2,
     'default_incons': [1.013e5, 25]})

sand = rocktype('ROCK1', 0, 2600, 0.1, [6.51e-12, 6.51e-12, 6.51e-12], 0.0, 952.9)

react.grid.delete_rocktype('dfalt')
react.grid.add_rocktype(sand)

for blk in react.grid.blocklist[0:]:
    blk.rocktype = react.grid.rocktype[sand.name]

zone1 = t2zone('zone1')

react.grid.add_zone(zone1)

for blk in react.grid.blocklist[0:]:
    blk.zone = react.grid.zone[zone1.name]

react.start = True

react.write('flow.inp')

# ____________________________________CHEMICAL.INP________________________________________________________________
h2o = PrimarySpecies('h2o', 0)
h = PrimarySpecies('h+', 0)
na = PrimarySpecies('na+', 0)
cl = PrimarySpecies('cl-', 0)
hco3 = PrimarySpecies('hco3-', 0)
ca = PrimarySpecies('ca+2', 0)
so4 = PrimarySpecies('so4-2', 0)
mg = PrimarySpecies('mg+2', 0)
h4sio4 = PrimarySpecies('h4sio4', 0)
al = PrimarySpecies('al+3', 0)
fe = PrimarySpecies('fe+2', 0)
hs = PrimarySpecies('hs-', 0)

all_species = [h2o, h, na, cl, hco3, ca, so4, mg, h4sio4, al, fe, hs]

h2o_comp1 = WaterComp(h2o, 1, 1.0000E+00, 1.000000E+00)
h_comp1 = WaterComp(h, 1, 1E-7, 1E-7)
na_comp1 = WaterComp(na, 1, 1E-10, 2.93E-2)
cl_comp1 = WaterComp(cl, 1, 1E-10, 1.08E-3)
hco3_comp1 = WaterComp(hco3, 1, 1E-10, 2.21E-08)
ca_comp1 = WaterComp(ca, 1, 1E-10, 5.9E-03)
so4_comp1 = WaterComp(so4, 1, 1E-10, 6.94E-3)
mg_comp1 = WaterComp(mg, 1, 1E-10, 2.54E-8)
h4sio4_comp1 = WaterComp(h4sio4, 1, 1E-10, 1E-10)
al_comp1 = WaterComp(al, 1, 1E-10, 9.96E-5)
fe_comp1 = WaterComp(fe, 1, 1E-10, 9.7E-9)
hs_comp1 = WaterComp(hs, 1, 1E-10, 1E-10)

initial_water_zone1 = Water([h2o_comp1, h_comp1, na_comp1, cl_comp1, hco3_comp1, ca_comp1, so4_comp1, mg_comp1, h4sio4_comp1, al_comp1, fe_comp1, hs_comp1],
                            25, 200)

mineral_list = ['c3fh6', 'tobermorite', 'calcite', 'csh', 'portlandite', 'ettringite', 'katoite', 'hydrotalcite']
all_minerals = get_kinetics_minerals(mineral_list)


c3fh6_zone1 = MineralComp(get_specific_mineral(mineral_list[0]), 0.1, 0, 0.0E-00, 20000.0, 0)
tobermorite_zone1 = MineralComp(get_specific_mineral(mineral_list[1]), 0.05, 0, 0.0E-00, 20000.0, 0)
calcite_zone1 = MineralComp(get_specific_mineral(mineral_list[2]), 0.4, 1, 0.0E-00, 260.0, 0)
csh_zone1 = MineralComp(get_specific_mineral(mineral_list[3]), 0.1, 1, 0.0E-00, 20000.0, 0)
portlandite_zone1 = MineralComp(get_specific_mineral(mineral_list[4]), 0.1, 1, 0.0E-00, 1540.0, 0)
ettringite_zone1 = MineralComp(get_specific_mineral(mineral_list[5]), 0.1, 1, 0.0E-00, 20000.0, 0)
katoite_zone1 = MineralComp(get_specific_mineral(mineral_list[6]), 0.1, 1, 0.0E-00, 570.0, 0)
hydrotalcite_zone1 = MineralComp(get_specific_mineral(mineral_list[7]), 0.05, 1, 0.0E-00, 1000.0, 0)

initial_co2 = ReactGas('co2(g)', 0, 1.1)
ijgas = [[initial_co2], []]

permporo = PermPoro(1, 0, 0)
permporozone = PermPoroZone([permporo])

zone1.water = [[initial_water_zone1], []]
zone1.gas = [[initial_co2], []]
mineral_zone1 = MineralZone([c3fh6_zone1, tobermorite_zone1, calcite_zone1, csh_zone1, portlandite_zone1, ettringite_zone1, katoite_zone1, hydrotalcite_zone1])
zone1.mineral_zone = mineral_zone1
zone1.permporo = permporozone

writeChemical = t2chemical(t2reactgrid=react.grid)
writeChemical.minerals = all_minerals
writeChemical.title = 'Automating Tough react'
writeChemical.primary_aqueous = all_species
writeChemical.gases = initial_co2
writeChemical.write()

# ____________________________________SOLUTE.INP________________________________________________________________
writeSolute = t2solute(t2chemical=writeChemical)
writeSolute.nodes_to_write = [0]
writeSolute.write()

# ___________________________________ RUN SIMULATION ___________________________________________________________
print(os.path.dirname(__file__))
react.run(writeSolute, simulator='treacteos1.exe')
# react.run(simulator='treacteos1.exe', runlocation=os.getcwd())
