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

import numpy as np
import os

from mulgrids import mulgrid
from pytoughreact.writers.bio_writing import T2Bio
from pytoughreact.chemical.biomass_composition import Component, Biomass, Gas, WaterBio
from pytoughreact.chemical.bio_process_description import BIODG, Process
from t2grids import t2grid
from t2data import rocktype, t2generator

# __________________________________FLOW.INP______________________________________________________
second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour
year = 365. * day
year = float(year)
simulation_time = 100 * year

length = 1000.
x_block = 10
y_block = 1
z_block = 5
dx = [length / x_block] * x_block
dy = [1.0]
dz = [5] * z_block
geo = mulgrid().rectangular(dx, dy, dz, origin=[0, 0, -95])
geo.write('geom.dat')

bio = T2Bio()
bio.title = 'Biodegradation Runs'

bio.grid = t2grid().fromgeo(geo)
bio.grid.delete_rocktype('dfalt')
shale = rocktype('shale', 0, 2600, 0.27, [6.51e-19, 6.51e-19, 6.51e-19], 1.5, 900)
bio.grid.add_rocktype(shale)

for blk in bio.grid.blocklist[0:]:
    blk.rocktype = bio.grid.rocktype[shale.name]

bio.multi = {'num_components': 3, 'num_equations': 3, 'num_phases': 3,
             'num_secondary_parameters': 8}

bio.parameter.update(
    {'print_level': 3,
     'max_timesteps': 9999,
     'tstop': simulation_time,
     'const_timestep': 100.,
     'print_interval': 1,
     'gravity': 9.81,
     'option': np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
     'relative_error': 1e-5,
     'phase_index': 2,
     'default_incons': [9.57e+06, 0, 1e-6, 30.]})

# ______________________________________BIODEGRADATION______________________________
bio.start = True
toluene = Component(1).default_toluene()
bio.components = [toluene]
O2_gas = Gas('O2', 2)
bio.gas = [O2_gas]

water = WaterBio('H2O')

biomass = Biomass(1, 'biom', 0.0153, 1.00e-6, 30, 2.3148e-07, 0.e-6)
oxygen_ks = 0.5e-6
oxygen_uptake = 1
water_uptake = -3

process1 = Process(biomass, 2, 1.6944e-04, 0.58, 0)
water.add_to_process(process1, water_uptake)
O2_gas.add_to_process(process1, oxygen_uptake, oxygen_ks)
toluene.add_to_process(process1, 1, 7.4625e-06)

biodegradation = BIODG(0, 1.e-10, 0, 0.2, 0.9, 0.9,
                       [process1],
                       [biomass])
bio.biodg = [biodegradation]

bio.diffusion = [
    [2.e-5, 6.e-10, 6.e-10],
    [2.e-5, 6.e-10, 6.e-10],
    [2.e-5, 6.e-10, 6.e-10],
    [2.e-5, 6.e-10, 6.e-10],
    [2.e-5, 6.e-10, 6.e-10],
    [2.e-5, 6.e-10, 6.e-10],
    [2.e-5, 6.e-10, 6.e-10],
    [2.e-5, 6.e-10, 6.e-10]
]

well = 'wl '
compo = ['COM3']
direction = 'x'
duration = [0, 1 * year, 101 * year]
# duration = np.linspace(0, simulation_time * 2, 7)
rate = np.array([1.00e-2, 0, 0])
rate_o2 = [1.00e-03, 0, 0]
energy = [5, 5, 5]

if direction == 'x':
    j = 0
    for i in range(0, x_block):
        # for i in range(x_block * (z_block - 1), x_block * (z_block)):
        for component in compo:
            if component == 'COM2':
                gen = t2generator(name=well + str(i), block=bio.grid.blocklist[i].name, type=component,
                                  ltab=len(duration),
                                  itab=str(3),
                                  time=duration, rate=rate_o2, enthalpy=energy)
                bio.add_generator(gen)
            else:
                gen = t2generator(name=well + str(i), block=bio.grid.blocklist[i].name, type=component,
                                  ltab=len(duration),
                                  itab=str(3),
                                  time=duration, rate=rate, enthalpy=energy)
                bio.add_generator(gen)
            j = j + 1

# ____________________________________RUN SIMULATION_______________________________________________________________

run_location = os.getcwd()
bio.write('INFILE', run_location=os.getcwd())
bio.run(simulator='tmvoc', run_location='')
