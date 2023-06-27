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

The model is instructed to start and the file is saved to the `flow.inp` simulation file

.. code-block:: python

    react.start = True

    react.write('flow.inp')

Chemical Reaction Model
~~~~~~~~~~~~~~~~~~~~

After the flow model is created, the chemical reaction model follows. This begins with the creation of 
the primary species in the simulation. This is done using the `PrimarySpecies` class in PyTOUGHREACT.
This class takes in two arguments for the name of the primary species and a NOTRANS argument. All species
are then combined into a list

.. code-block:: python

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


The composition of the water present in the simulation are initialized. This is done using the `WaterComp` class
in PyTOUGHREACT. The class takes in arguments for the primary species, type of constraint controlling 
the solute content, initial concentration guess and total dissolved component concentration.

.. code-block:: python

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

The water in a zone is then summarized using the `Water` class consisting of a list of the earlier 
defined `WaterComp` classes and the temperature and pressure in that water zone.

.. code-block:: python

    initial_water_zone1 = Water([h2o_comp1, h_comp1, na_comp1, cl_comp1, hco3_comp1, ca_comp1, so4_comp1, mg_comp1, h4sio4_comp1, al_comp1, fe_comp1, hs_comp1],
                            25, 200)


The next step is to generate a mineral property. This process involves multiple steps. The first of which
is to define the `Mineral` class. The mineral class is defined as follows. It takes in five arguments; the
name of the mineral, a flag for the type of mineral, a flag for the kind of constraints provided, 
an index for a solid solution mineral endmember and an index for a mineral that may be precipitated in a dry grid block. 

.. code-block:: python

    albite = Mineral('Albite(low)', 1, 3, 0, 0)


To provide the dissolution and precipitation properties for the mineral, the `Dissolution` and `Precipitation`
classes are used. These classes contain information for rate constants (in mol/m2/sec), flag for
rate dependence on pH, rate equation exponents, activation energy. If Precipitation is defined, parameters
are also made for the initial volume fraction and precipitation law index. If ph dependence is specified,
two pH dependence parameters law classes are made viz `pHDependenceType1` and `pHDependenceType2`. The pH
dependence type 1 takes in parameters for pH1 and pH2 and slope 1 and slope 2 as in the TOUGHREACT manual.
The second pH dependence type takes in parameters for activation energy, number of species involved in each
mechanism, name of the species involved in the mechanism and the power term exponential. The dissolution, 
precipitation and ph dependence types are added to the base mineral class as shown below

.. code-block:: python

    dissolution_albite = Dissolution(1.4454e-13, 2, 1, 1, 69.8, 0, 0, 0)
    precipitation_albite = Precipitation(1.4454e-13, 0, 1, 1, 69.8, 0, 0, 0, 1.0E-6, 0, 0, 0, 0)
    albite_ph = pHDependenceType2(2.1380e-11, 65, 1, 'h+', 0.457)
    dissolution_albite.pHDependence = [albite_ph]
    albite.dissolution = [dissolution_albite]
    albite.precipitation = [precipitation_albite]


All minerals used in the simulation are then saved in a list. Default mineral properties are 
saved in the `default_minerals.py` script and can be accessed in a list using
the `get_kinetics_minerals` function as below.

.. code-block:: python

    mineral_list = ['c3fh6', 'tobermorite', 'calcite', 'csh', 'portlandite', 'ettringite', 'katoite', 'hydrotalcite']
    all_minerals = get_kinetics_minerals(mineral_list)

The minerals are then aggregated in a zone using the `MineralComp` class. This class takes in the 
`Mineral` class, initial volume fraction for that zone, flag for if the mineral is at equilibrium 
or under kinetic constraints. If the mineral is kinetic, additional parameters are added for radius 
of mineral grain, specific reactive surface area, flag for surface area conversion


.. code-block:: python

    c3fh6_zone1 = MineralComp(get_specific_mineral(mineral_list[0]), 0.1, 0, 0.0E-00, 20000.0, 0)
    tobermorite_zone1 = MineralComp(get_specific_mineral(mineral_list[1]), 0.05, 0, 0.0E-00, 20000.0, 0)
    calcite_zone1 = MineralComp(get_specific_mineral(mineral_list[2]), 0.4, 1, 0.0E-00, 260.0, 0)
    csh_zone1 = MineralComp(get_specific_mineral(mineral_list[3]), 0.1, 1, 0.0E-00, 20000.0, 0)
    portlandite_zone1 = MineralComp(get_specific_mineral(mineral_list[4]), 0.1, 1, 0.0E-00, 1540.0, 0)
    ettringite_zone1 = MineralComp(get_specific_mineral(mineral_list[5]), 0.1, 1, 0.0E-00, 20000.0, 0)
    katoite_zone1 = MineralComp(get_specific_mineral(mineral_list[6]), 0.1, 1, 0.0E-00, 570.0, 0)
    hydrotalcite_zone1 = MineralComp(get_specific_mineral(mineral_list[7]), 0.05, 1, 0.0E-00, 1000.0, 0)


The information for gases to be added to the domain is done using the `ReactGas` class. It takes in
three parameters, the name of the gaseous species, the fugacity flag and the partial pressure (in bar)
as shown below

.. code-block:: python

    co2_gas = ReactGas('co2(g)', 0, 1.1)


The initial and injection gas are then saved in a list as shown below

.. code-block:: python

    ijgas = [[initial_co2], []]

The permeability porosity relation is modeled with the `PermPoro` class with the index for the permeability
law, and parameters for the chosen law chosen as inputs to the simulation.

.. code-block:: python

    permporo = PermPoro(1, 0, 0)


To be able to assign the permeability porosity to different zones in the domain, the `PermPoroZone`
is created

.. code-block:: python

    permporozone = PermPoroZone([permporo])

After the declaration of all parameters is completed, they are then assigned to different parts of the
domain using the earlier defined zones as shown


.. code-block:: python

    zone1.water = [[initial_water_zone1], []]
    zone1.gas = [[initial_co2], []]
    mineral_zone1 = MineralZone([c3fh6_zone1, tobermorite_zone1, calcite_zone1, csh_zone1, portlandite_zone1, ettringite_zone1, katoite_zone1, hydrotalcite_zone1])
    zone1.mineral_zone = mineral_zone1
    zone1.permporo = permporozone


The properties to be written in the `chemical.inp` file are then saved in a `t2chemical` class

.. code-block:: python

    writeChemical = t2chemical(t2reactgrid=react.grid)
    writeChemical.minerals = all_minerals
    writeChemical.title = 'Automating Tough react'
    writeChemical.primary_aqueous = all_species
    writeChemical.gases = initial_co2
    writeChemical.write()

The `t2solute` class takes care of writing to `solute.inp` file as shown below

.. code-block:: python

    writeSolute = t2solute(t2chemical=writeChemical)
    writeSolute.nodes_to_write = [0]
    writeSolute.write()

The simulation can be run using the code below

.. code-block:: python

    react.run(writeSolute, simulator='treacteos1.exe')