Tutorial
===================================

This section details how to use PyTOUGHREACT to conduct a simulation for both TOUGHREACT and 
TMVOC_BIO

TOUGHREACT Example Simulation
------------------------------

The first step in using the package is to import all the necessary libraries into the main file.
This can be done as shown below

.. code-block:: python

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


The simulation grid is then created. This is done in the same manner as in PyTOUGH. A simple 2D grid is 
created here consisting of one block in the X and Z directions. The mulgrid class is used to create the
rectangular dimensions of the grid and stroed in the `geom.dat` file

.. code-block:: python
    length = 0.1
    nblks = 1
    dx = [length / nblks] * nblks
    dy = [0.5]
    dz = [0.5] * 1
    geo = mulgrid().rectangular(dx, dy, dz)
    geo.write('geom.dat')