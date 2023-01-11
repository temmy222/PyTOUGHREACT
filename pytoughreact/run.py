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
from writers.react_writing import t2react
from pytough_wrapper.wrapper.reactgrid import t2reactgrid
from pytough_wrapper.wrapper.reactzone import t2zone
from chemical.chemical_composition import PrimarySpecies, WaterComp, Water, ReactGas
from chemical.mineral_composition import MineralComp
from chemical.mineral_zone import MineralZone
from chemical.perm_poro_zone import PermPoroZone, PermPoro
from constants.default_minerals import get_kinetics_minerals, get_specific_mineral
from writers.chemical_writing import t2chemical
from writers.solute_writing import t2solute
from t2grids import rocktype


#________________________FLOW.INP______________________________________________________

length = 1000.
nblks = 10
dx = [length / nblks] * nblks
dy = [1.0]
dz = [1.0] * 5
geo = mulgrid().rectangular(dx, dy, dz)
geo.write('geom.dat')

react = t2react()
react.title = 'Reaction example'

react.multi = {'num_components': 1, 'num_equations': 1, 'num_phases': 2,
               'num_secondary_parameters': 6}

react.grid = t2reactgrid().fromgeo(geo)

react.parameter.update(
    {'print_level': 3,
     'max_timesteps': 9999,
     'tstop': 86400,
     'const_timestep': 100.,
     'print_interval': 1,
     'gravity': 9.81,
     'relative_error': 1e-5,
     'phase_index': 2,
     'default_incons': [101.3e3, 170]})

shale = rocktype('shale', 0, 2600, 0.27, [6.51e-19, 6.51e-19, 6.51e-19], 1.5, 900)
sand = rocktype('sands', 0, 2700, 0.17, [6.51e-19, 6.51e-19, 6.51e-19], 1.5, 800)

react.grid.delete_rocktype('dfalt')
react.grid.add_rocktype(shale)
react.grid.add_rocktype(sand)

for blk in react.grid.blocklist[0:]:
    if 0 < blk.centre[0] < 250 and 0 < blk.centre[1] < 1 and 0 < abs(blk.centre[2]) < 5:
        blk.rocktype = react.grid.rocktype[shale.name]
    else:
        blk.rocktype = react.grid.rocktype[sand.name]


zone1 = t2zone('zone1')
zone2 = t2zone('zone2')
zone3 = t2zone('zone3')
zone4 = t2zone('zone4')
zone5 = t2zone('zone5')

react.grid.add_zone(zone1)
react.grid.add_zone(zone2)
react.grid.add_zone(zone3)
react.grid.add_zone(zone4)
react.grid.add_zone(zone5)

for blk in react.grid.blocklist[0:]:
    if 0 < blk.centre[0] < 150 and 0 < blk.centre[1] < 1 and 0 < abs(blk.centre[2]) < 4:
        blk.zone = react.grid.zone[zone1.name]
    elif 100 < blk.centre[0] < 250 and 0 < blk.centre[1] < 1 and 0 < abs(blk.centre[2]) < 4:
        blk.zone = react.grid.zone[zone2.name]
    elif 200 < blk.centre[0] < 550 and 0 < blk.centre[1] < 1 and 0 < abs(blk.centre[2]) < 4:
        blk.zone = react.grid.zone[zone3.name]
    elif 500 < blk.centre[0] < 1050 and 0 < blk.centre[1] < 1 and 0 < abs(blk.centre[2]) < 4:
        blk.zone = react.grid.zone[zone4.name]
    else:
        blk.zone = react.grid.zone[zone5.name]

react.start = True

react.write('flow.inp')

#____________________________________CHEMICAL.INP________________________________________________________________
h2o = PrimarySpecies('h2o', 0)
h = PrimarySpecies('h+', 0)
hco3 = PrimarySpecies('hco3-', 0)
ca = PrimarySpecies('ca+2', 0)
all_species = [h2o, h, hco3, ca]

h2o_comp1 = WaterComp(h2o, 1, 1.0000E+00, 1.000000E+00)
h_comp1 = WaterComp(h, 1, 1.9033E-11, -3.695684E-02)
hco3_comp1 = WaterComp(hco3, 1, 5.5095E-08, 9.455547E-05)
ca_comp1 = WaterComp(ca, 1, 3.7283E-02, 5.472614E-02)

initial_water_zone1 = Water([h2o_comp1, h_comp1, hco3_comp1, ca_comp1], 50, 1000)
initial_water_zone2 = Water([h2o_comp1, h_comp1, hco3_comp1, ca_comp1], 60, 2000)
initial_water_zone3 = Water([h2o_comp1, h_comp1, hco3_comp1, ca_comp1], 70, 3000)
initial_water_zone4 = Water([h2o_comp1, h_comp1, hco3_comp1, ca_comp1], 80, 4000)
initial_water_zone5 = Water([h2o_comp1, h_comp1, hco3_comp1, ca_comp1], 90, 5000)
boundary_water_zone5 = Water([h2o_comp1, h_comp1, hco3_comp1, ca_comp1], 100, 6000)


mineral_list = ['calcite', 'portlandite']
all_minerals = get_kinetics_minerals(mineral_list)
masa = all_minerals[0]

calcite_zone1 = MineralComp(get_specific_mineral(mineral_list[0]), 0.2, 1, 0.0E-00, 22100.0, 0)
portlandite_zone1 = MineralComp(get_specific_mineral(mineral_list[1]), 0.8, 1, 0.0E-00, 22100.0, 0)
calcite_zone2 = MineralComp(get_specific_mineral(mineral_list[0]), 0.3, 1, 0.0E-00, 22100.0, 0)
portlandite_zone2 = MineralComp(get_specific_mineral(mineral_list[1]), 0.7, 1, 0.0E-00, 22100.0, 0)
calcite_zone3 = MineralComp(get_specific_mineral(mineral_list[0]), 0.4, 1, 0.0E-00, 22100.0, 0)
portlandite_zone3 = MineralComp(get_specific_mineral(mineral_list[1]), 0.6, 1, 0.0E-00, 22100.0, 0)
calcite_zone4 = MineralComp(get_specific_mineral(mineral_list[0]), 0.5, 1, 0.0E-00, 22100.0, 0)
portlandite_zone4 = MineralComp(get_specific_mineral(mineral_list[1]), 0.5, 1, 0.0E-00, 22100.0, 0)
calcite_zone5 = MineralComp(get_specific_mineral(mineral_list[0]), 0.2, 1, 0.0E-00, 22100.0, 0)
portlandite_zone5 = MineralComp(get_specific_mineral(mineral_list[1]), 0.8, 1, 0.0E-00, 22100.0, 0)

initial_co2 = ReactGas('co2(g)', 0, 0)
injection_co2 = ReactGas('co2(g)', 0, 0.01)
ijgas = [[initial_co2], [injection_co2]]

permporo = PermPoro(1, 0, 0)
permporozone = PermPoroZone([permporo])

zone1.water = [[initial_water_zone1], []]
zone1.gas = [[initial_co2], []]
mineral_zone1 = MineralZone([calcite_zone1, portlandite_zone1])
zone1.mineral_zone = mineral_zone1
zone1.permporo = permporozone

zone2.water = [[initial_water_zone2], []]
zone2.gas = [[initial_co2], []]
mineral_zone2 = MineralZone([calcite_zone2, portlandite_zone2])
zone2.mineral_zone = mineral_zone2
zone2.permporo = permporozone

zone3.water = [[initial_water_zone3], []]
zone3.gas = [[initial_co2], []]
mineral_zone3 = MineralZone([calcite_zone3, portlandite_zone3])
zone3.mineral_zone = mineral_zone3
zone3.permporo = permporozone

zone4.water = [[initial_water_zone4], []]
zone4.gas = [[initial_co2], []]
mineral_zone4 = MineralZone([calcite_zone4, portlandite_zone4])
zone4.mineral_zone = mineral_zone4
zone4.permporo = permporozone

zone5.water = [[initial_water_zone5], [boundary_water_zone5]]
zone5.gas = [[initial_co2], [injection_co2]]
mineral_zone5 = MineralZone([calcite_zone5, portlandite_zone5])
zone5.mineral_zone = mineral_zone5
zone5.permporo = permporozone

writeChemical = t2chemical(t2reactgrid=react.grid)
writeChemical.minerals = all_minerals
writeChemical.title = 'Automating Tough react'
writeChemical.primary_aqueous = all_species
writeChemical.gases = initial_co2
writeChemical.write()

#____________________________________SOLUTE.INP________________________________________________________________
writeSolute = t2solute(writeChemical)
writeSolute.nodes_to_write = [0]
masa = writeSolute.getgrid_info()
writeSolute.write()

#___________________________________ RUN SIMULATION ___________________________________________________________
print(os.path.dirname(__file__))
react.run(simulator='treacteos1.exe', runlocation=os.getcwd())

