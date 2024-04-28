# PyTOUGHREACT


- [PyTOUGHREACT](#pytoughreact)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [Documentation](#documentation)
  - [License](#license)
  - [Tests](#tests)


PyTOUGHREACT is a Python package for automating reactive transport simulations including biodegradation reactions.
It makes use of TOUGHREACT, TMVOC and TMVOCBIO executables for running the simulations. These executables are interfaced
with python to automate the runs. It will be particularly useful for uncertainty quantifications, sensitivity 
analysis without the need to have a lot of files stored on your local computer. It builds on the PyTOUGH software which processes for the TOUGH2 executables.

## Installation

PyTOUGHREACT is available on PyPI which is a repository of softwares built with the Python Programming Language. Before installing PyTOUGHREACT, it is required to have Python >=3.7 installed on your local computer. Python can be downloaded from the [python.org](python.org) website and installing it by following the instructions. Windows users should ensure that the path to the python is set in the environment variable to ensure availability everywhere.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyTOUGHREACT.

```bash
pip install pytoughreact
```

The package can also be forked from this GitHub page and installation performed using

```bash
python setup.py install  or py setup.py install
```

<!-- Because pytoughreact requires PyTOUGH and PyTOUGH is not uploaded to PyPI, it is required to download the zip folder of PyTOUGH from the GitHub repository https://github.com/acroucher/PyTOUGH. Unzip the folder and place in your current working directory. Change directory into the PyTOUGH folder and run python setup.py install or pip install on the command line. With PyTOUGH installed, PyTOUGHREACT is ready to be used as a package. -->

Because pytoughreact requires PyTOUGH, this library also needs to be installed.
PyTOUGH can be installed by running the command below

```bash
pip install PyTOUGH
```

## Usage

```python
import os
from mulgrids import mulgrid
from pytoughreact.writers.react_writing import T2React
from pytoughreact.chemical.chemical_composition import PrimarySpecies, WaterComp, Water, ReactGas
from pytoughreact.wrapper.reactgrid import T2ReactGrid
from pytoughreact.wrapper.reactzone import T2Zone
from pytoughreact.chemical.mineral_composition import MineralComp
from pytoughreact.chemical.mineral_zone import MineralZone
from pytoughreact.constants.default_minerals import get_kinetics_minerals, get_specific_mineral
from pytoughreact.chemical.mineral_description import Mineral
from pytoughreact.writers.chemical_writing import T2Chemical
from pytoughreact.chemical.perm_poro_zone import PermPoro, PermPoroZone
from pytoughreact.writers.solute_writing import T2Solute
from t2grids import rocktype

#__________________________________FLOW.INP____________________________________________
length = 0.1
nblks = 1
dx = [length / nblks] * nblks
dy = [0.5]
dz = [0.5] * 1
geo = mulgrid().rectangular(dx, dy, dz)
geo.write('geom.dat')

react = T2React()
react.title = 'Reaction example'

react.multi = {'num_components': 1, 'num_equations': 1, 'num_phases': 2,
               'num_secondary_parameters': 6}

react.grid = T2ReactGrid().fromgeo(geo)

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


zone1 = T2Zone('zone1')

react.grid.add_zone(zone1)

for blk in react.grid.blocklist[0:]:
    blk.zone = react.grid.zone[zone1.name]

react.start = True

react.write('flow.inp')

#____________________________________CHEMICAL.INP________________________________________
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

all_species = [h2o, h,na, cl, hco3, ca, so4, mg, h4sio4, al, fe, hs]

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

initial_water_zone1 = Water([h2o_comp1, h_comp1, na_comp1, cl_comp1, hco3_comp1, ca_comp1, so4_comp1, mg_comp1, h4sio4_comp1, al_comp1, fe_comp1, hs_comp1], 25, 200)

mineral_list = ['c3fh6', 'tobermorite', 'calcite', 'csh' , 'portlandite', 'ettringite', 'katoite', 'hydrotalcite']
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

write_chemical = T2Chemical(t2reactgrid=react.grid)
write_chemical.minerals = all_minerals
write_chemical.title = 'Automating Tough react'
write_chemical.primary_aqueous = all_species
write_chemical.gases = initial_co2
write_chemical.write()

#____________________________________SOLUTE.INP__________________________________________
write_solute = T2Solute(t2chemical=write_chemical)
write_solute.readio['database'] = 'tk-ddem25aug09.dat' # update a property in solute file
write_solute.nodes_to_write = [0]
write_solute.write()

#___________________________________ RUN SIMULATION ______________________________________
react.run(simulator='treacteos1.exe', runlocation=os.getcwd())


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Contributing to the code would involve you following the below procedures to quickly get started

1. Clone the repo using preferred cloning method
2. Install the library to enable you able to use the test example using

```python
pip install -e .
```
3. Modify the code 
4. Tests are conducted with pytest and coverage reports are performed using pytest-cov. Install pytest and pytest-cov using the commands below
   
```python
pip install pytest
```

```python
pip install pytest-cov
```
5. Run tests:  Run the below command from the root folder to run the tests
   
```python
pytest
```

6. Flake8 is also used to ensure code readability. Install flake8 using 
   
```python
pip install flake8
```
and run flake8 using

```python
flake8 src
```

7. PEP8 Naming package is also used to ensure adherence to PEP8. Install pep8-naming using 
   
```python
pip install pep8-naming
```

8. Make a pull request after passing all tests
9. More information can be found in developer notes in the documentation - https://pytoughreact.readthedocs.io/en/master/developer.html 

## Documentation
Documentation can be found here https://pytoughreact.readthedocs.io/en/latest/ 


## License
[MIT](https://github.com/temmy222/PyTOUGHREACT/blob/master/LICENSE)

## Tests

![Tests](https://github.com/temmy222/PyTOUGHREACT/actions/workflows/tests.yml/badge.svg)
![JOSS Article](https://github.com/temmy222/PyTOUGHREACT/actions/workflows/draft-pdf.yml/badge.svg)
![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=for-the-badge&logo=dependabot&logoColor=white)
![GitHub contributors](https://img.shields.io/github/contributors/temmy222/PyTOUGHREACT)
![PyPI - Version](https://img.shields.io/pypi/v/PyTOUGHREACT)
![PyPI - License](https://img.shields.io/pypi/l/pytoughreact)
