---
title: 'PyToughReact – A Python Package for automating reactive transport and biodegradation simulations.'
tags:
  - python
  - reactive transport
  - uncertainty quantification
  - sensitivity analysis
  - TOUGH, PyTOUGH
authors:
  - name: Temitope Ajayi^[Co-first author] # note this makes a footnote saying 'Co-first author'
    orcid: 0000-0002-0782-7460
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Ipsita Gupta^[Corresponding author]
    affiliation: 1
affiliations:
 - name: Louisiana State Univeristy, USA
   index: 1
date: 19 February 2023
bibliography: paper.bib
 
---

# Statement of need

The suite of TOUGH simulators by the Lawrence Berkeley National Laboratory (LBNL) are well known simulators for flow and transport simulations. In order to model chemical reactions coupled to flow for isothermal and non-isothermal systems, the TOUGHREACT simulator exists. In addition, the TMVOC software exists for the modeling of multicomponent mixtures of volatile organic compounds suitable for contamination problems. When biodegradation is required to be modeled, the tool used is known as TMVOC-BIO. These reaction simulators as of now do not provide a mechanism to automate simulations for tasks such as uncertainty quantification or sensitivity analysis which require multiple simulation runs. Users need to create many simulation folders to perform every sensitivity they intend to run with the simulator. This makes it cumbersome to use and users could get lost on the purpose of each folder if not correctly labeled. While PyTOUGH and TOUGHIO exists for fluid flow and transport simulations, no such tool exists for chemical and biodegradation reactions, `PyToughReact` fulfills this need for users familiar with python. Further, `PyTOUGHREACT` enables users familiar with python to incorporate language capabilities into their reaction simulation workflows.

# Introduction

TOUGH suite of simulators requires users to write or modify a text file and parse the file to an executable to perform the simulation. Results from simulations are subsequently also saved to text files for interpretation by third party softwares. These makes it cumbersome for sensitivity analysis and uncertainty studies to be conducted as this would require a user to make multiple manual edits to files to extract required data. As would be imagined, this is also prone to human errors. Further, coupling the simulator with other simulators would be more involving. As a result of this, numerous tools have been created that wrap around the executables and make writing, reading and visualization of model properties easier to implement. Examples of such include PetraSim [@Yamamoto:2008] for which assist in creating the models and visualizing results, TOUGH2VIEWER [@Bondua:2012] and TECPLOT [@tecplot] for postprocessing and visualizations and IGMESH for building and integrating visualization tools suited especially for irregular gridding [@Hu:2016]. For scripting purposes, PyTOUGH [@Croucher:2011] and TOUGHIO [@Luu:2020] are used for pre and post processing of TOUGH2 simulations. So far, no tool exists for scripting of the reaction softwares of TOUGH. Reactive processes as with other processes are subject to lots of uncertainties and need to be adequately accounted for in engineering studies. To enable this with the TOUGHREACT simulator, it is essential to create a scripting tool to accomplish this. This tool extends the work done by PyTOUGH in creating an automatic platform for running TOUGH flow simulations by creating a concurrent tool for automating chemical and biodegradation reactions from any python enabled terminal or IDE.  

# Architecture

## General Architecture

The software uses object-oriented programming principles to structure the code. The software can be thought of as composed of two main segments; the processing segment and the output segment (Figure 1). The processing segment contains three main sections, IO processing, BIO and REACT.  The IO processing is responsible for most of the input and output processing such as reading, writing. The BIO section is responsible for the TMVOC section of the package where it contains classes for storing biomass and degradation information and processing it before passing to IO processing for read/write. Similarly, the react section assists in processing reaction parameters such as mineral, chemical, and solute information before passing to the IO processing segment for read/write. After the files have been written to or read from the appropriate file types, the executable is called from within PyTOUGHREACT and the simulation is performed using the executable. Thereafter, the output segment is called which can read the results of the simulations and contains methods and functions which assist the user in creating 2D or 3D plots through the plotting module.

![Caption for example figure.\label{fig:example}](../images/general_architecture.png)


An example of a full biodegradation run file simulation is shown below

```python
import numpy as np
import pytoughreact as pyt
from pytoughreact import mulgrid, t2grid, Component, Gas, Water_Bio, Biomass, Process, BIODG, rocktype

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
bio.run('tmvoc.exe')

```




# Acknowledgements

Funding for this research is from the National Academy of Sciences, Engineering, and Medicine (NASEM) Gulf Research 
Program (GRP) grant on “Mitigating Risks to Hydrocarbon Release through Integrative Advanced Materials for Wellbore 
Plugging and Remediation” under award number 200008863 and the Early Career Research Fellowship of Ipsita Gupta.

# References