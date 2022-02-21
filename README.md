# PyTOUGHREACT

PyTOUGHREACT is a Python library for automating reactive transport simulations including biodegradation reactions.
It makes use of TOUGHREACT, TMVOC and TMVOCBIO for running the simulations. These softwares are interfaced
with python to automate the runs. It will be particularly useful for uncertainty quantifications, sensitivity 
analysis without the need to have a lot of files stored on your local computer.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyTOUGHREACT.

```bash
pip install pytoughreact
```

## Usage

```python
import numpy as np
import pytoughreact as pyt
from pytoughreact import mulgrid, t2grid, Component, Gas, Water_Bio, Biomass, Process, BIODG
from pytoughreact.pytough.t2grids import rocktype

second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour
year = 365. * day
year = float(year)
simtime = 1 * year

length = 9
xblock = 3
yblock = 1
zblock = 4
dx = [length / xblock] * xblock
dy = [0.1]
dz = [2] * zblock
geo = mulgrid().rectangular(dx, dy, dz, origin=[0, 0, -100])
geo.write('geom.dat')

bio = pyt.t2bio()
bio.title = 'Biodegradation Runs'

bio.grid = t2grid().fromgeo(geo)
bio.grid.delete_rocktype('dfalt')
shale = rocktype('shale', 0, 2600, 0.67, [6.51e-14, 6.51e-14, 6.51e-14], 1.5, 900)
bio.grid.add_rocktype(shale)

for blk in bio.grid.blocklist[0:]:
    blk.rocktype = bio.grid.rocktype[shale.name]

bio.multi = {'num_components': 3, 'num_equations': 3, 'num_phases': 3,
             'num_secondary_parameters': 8}

bio.parameter.update(
    {'print_level': 3,
     'max_timesteps': 9999,
     'tstop': simtime,
     'const_timestep': 1.,
     'print_interval': 1,
     'gravity': 9.81,
     'option': np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
     'relative_error': 1e-5,
     'phase_index': 2,
     'default_incons': [9.57e+05, 0, 0, 0, 0, 0, 0, 1e-3, 10.]})

# ,

bio.start = True
toluene = Component(1).defaultToluene()
bio.components = [toluene]

O2_gas = Gas('O2', 2)
bio.gas = [O2_gas]

water = Water_Bio('H2O')

biomass = Biomass(1, 'biom', 0.153, 1.00e-6, 30, 0, 0.e-6)
oxygen_ks = 0.5e-6
oxygen_uptake = 1
water_uptake = -3

process1 = Process(biomass, 2, 1.6944e-04, 0.58, 0)
water.addToProcess(process1, water_uptake)
O2_gas.addToProcess(process1, oxygen_uptake, oxygen_ks)
toluene.addToProcess(process1, 1, 7.4625e-06)

biodegradation = BIODG(0, 1e-5, 0, 0.2, 0.9, 0.9,
                       [process1],
                       [biomass])
bio.biodg = [biodegradation]

bio.diffusion = [
    [2.e-5, 6.e-10, 6.e-10],
    [2.e-5, 6.e-10, 6.e-10],
    [2.e-5, 6.e-10, 6.e-10]
]

bio.write('INFILE')
bio.run('executable_name.exe')


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)