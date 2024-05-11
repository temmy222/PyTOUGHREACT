Technical Details of PyTOUGHREACT
===================================

Why PyTOUGHREACT
-----------------
PyTOUGHREACT was borne out of the need to automatically undertake a lot of simulations with the 
TOUGHREACT, TMVOC and TMVOC-BIO softwares developed by the Lawrence Berkeley National Laboratory (LBNL). It was noticed at 
the time that to carry out multiple simulations for uncertainty quantifications involved storing multiple
files on ones local system and attempting to name them descriptively. This was time consuming and importantly
was subject to human errors and mistakes.

A similar tool exists for TOUGH3 with PyTOUGH and PyTOUGHREACT extends its capability to TOUGHREACT with additional
capabilities for plotting. Details of how PyTOUGH works can be found here https://pytough.readthedocs.io/_/downloads/en/latest/pdf/
and is essential to understand how it works before using PyTOUGHREACT.

What is TOUGHREACT / TMVOC and TMVOC-BIO
-----------------------------------------

TOUGHREACT
~~~~~~~~~~
TOUGHREACT is a multiphase, multicomponent non-isothermal simulator that utilizes coupled numerical modeling
methods to the solution of fluid, heat, solute and chemical reaction equations. It has wide applicability in 
many subsurface problems such as waste disposal and acid mine drainage remediation. Full information on how the software
functions can be found here https://www.osti.gov/servlets/purl/834237 

TMVOC
~~~~~~~~~~
TMVOC is another multicomponent nonisothermal simulator by LBNL designed for the simulation of flow of 
volatile organic chemicals in variably saturated media. It involves additional processes such as diffusion,
sorption, advection and phase-partitioning. Details on how the software works can be found in https://tough.lbl.gov/assets/docs/TMVOC_Users_Guide.pdf

TMVOC-BIO
~~~~~~~~~~
TMVOC-BIO possess exact features as the TMVOC with an additional capbility for the modeling of biodegradation
reactions. Details can be found here https://www.osti.gov/servlets/purl/1377850 

What is  PyTOUGHREACT
-----------------------
Simply put, PyTOUGHREACT is a python Library for automating reaction simulations using TOUGHREACT, TMVOC and TMVOC-BIO.
In addition to this capability, it also posesses the ability to make different kinds of 2D line and surface plots for different kinds of 
visualizations.

PyTOUGHREACT Software Architecture
----------------------------------------------

General Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The software uses object-oriented programming principles to structure the code. 
The software can be thought of as composed of two main segments; 
the processing segment and the output segment. 
The processing segment contains three main sections, IO processing, BIO and 
REACT.  The IO processing is responsible for most of the input and output 
processing such as reading, writing. The BIO section is responsible for the 
TMVOC section of the package where it contains classes for storing biomass 
and degradation information and processing it before passing to IO processing 
for read/write. Similarly, the react section assists in processing reaction 
parameters such as mineral, chemical, and solute information before passing 
to the IO processing segment for read/write. After the files have been written 
to or read from the appropriate file types, the executable is called from 
within PyTOUGHREACT and the simulation is performed using the executable. 
Thereafter, the output segment is called which can read the results of the 
simulations and contains methods and functions which assist the user in 
creating 2D or 3D plots through the plotting module.

.. image:: ../docs/images/general_architecture.png
   :alt: general architecture


BIO Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The BIO section is responsible for processing the TMVOC inputs. 
It makes use of two subsections to achieve this. 
The first subsection is responsible for aggregating the unique constituents 
of a biodegradation simulation for TMVOC; these constituents include water, 
gas, biomass, solids, and components. The second subsection is responsible 
for unique biodegradation processes in the simulation. This is done via two
 classes Process class and the BIODG class. The process class defines the 
 constituents for any biodegradation process and BIODG class combines all 
 processes together with numerical parameters for that process. 

 .. image:: ../docs/images/bio_architecture.png
   :alt: bio architecture


REACT Architecture
~~~~~~~~~~~~~~~~~~~~

The react component consists of two main subcomponents: the chemical 
subcomponent and the solute subcomponent. The chemical subcomponent is 
responsible for defining the chemical constituents of the simulation 
such as the primary species, water, mineral, gas while the solute sub 
component is responsible for mapping each of the defined chemical 
constituents to the grid of the simulation and other functions such as 
what grids to write to output etc. This component contains information 
stored in the solute.inp file for TOUGHREACT simulations.


Result and Plotting Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Though separate, the result and plotting architecture have very similar 
structures. The two sections are subdivided into 
single and multiple file processing. As the name suggests, the single file 
enables the processing of a single file. While the results section enables 
to process simulation output further in python, the plotting sections uses 
the output from the results section to make line and 2D plots. Similarly,
the multiple file processing of the results section makes use of multiple 
files to output results which are then used in the plotting section for
line and 2D plots. The multiple file processing provides efficiency when 
multiple files are required to be processed or in the plotting section to 
see variations from one simulation to another in a single plot. 

.. image:: ../docs/images/result_architecture.png
   :alt: bio architecture
