Tutorial
===================================

This section details how to use PyTOUGHREACT to conduct a simulation for both TOUGHREACT and 
TMVOC_BIO

TOUGHREACT Example Simulation
------------------------------

Flow Model
~~~~~~~~~~~~~~~~~~~~

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


The simulation grid is then created. A simple 2D grid is created here consisting of one block in the X and Z directions. The mulgrid class is used to create the
rectangular dimensions of the grid and stroed in the `geom.dat` file

.. code-block:: python

    length = 0.1
    nblks = 1
    dx = [length / nblks] * nblks
    dy = [0.5]
    dz = [0.5] * 1
    geo = mulgrid().rectangular(dx, dy, dz)
    geo.write('geom.dat')


After the 2D grid has been created, the reaction model is then created. This is done with a t2react
class which provides the functionality to assign different reaction model to different segments of the
grid. The number of phases and components are also specified in this section

.. code-block:: python

    react = t2react()
    react.title = 'Reaction example'

    react.multi = {'num_components': 1, 'num_equations': 1, 'num_phases': 2,
                'num_secondary_parameters': 6}

    react.grid = t2reactgrid().fromgeo(geo)


The numerical parameters and default initial conditions for the model are then specified using the update method of the react.parameter
dictionary as shown below

.. code-block:: python

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


The physical rock type of the model is then specified using the rocktype class. This is the section where
parameters such as the rock density, porosity, permeability are specified as shown below. The default rocktype
is deleted before the assignment of new rock types to the grid. The `for` loop assigns each grid to a particular rock type

.. code-block:: python

    sand = rocktype('ROCK1', 0, 2600, 0.1, [6.51e-12, 6.51e-12, 6.51e-12], 0.0, 952.9)

    react.grid.delete_rocktype('dfalt')
    react.grid.add_rocktype(sand)

    for blk in react.grid.blocklist[0:]:
        blk.rocktype = react.grid.rocktype[sand.name]


The final part of creating the flow model involves initializing the chemical reaction model. This is 
done using the `t2zone` class with a name assigned to the name of the zone. A `for` loop can also be
used to assign reaction zones to different parts of the model.

.. code-block:: python

    zone1 = t2zone('zone1')

    react.grid.add_zone(zone1)

    for blk in react.grid.blocklist[0:]:
        blk.zone = react.grid.zone[zone1.name]


Chemical Reaction Model
~~~~~~~~~~~~~~~~~~~~

After the flow model is created, the chemical reaction model follows. This begins with  