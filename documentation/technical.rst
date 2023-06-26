Technical Details of PyTOUGHREACT
===================================

Why PyTOUGHREACT
-------
PyTOUGHREACT was borne out of the need to automatically undertake a lot of simulations with the 
TOUGHREACT, TMVOC and TMVOC-BIO softwares developed by the Lawrence Berkeley National Laboratory (LBNL). It was noticed at 
the time that to carry out multiple simulations for uncertainty quantifications involved storing multiple
files on ones local system and attempting to name them descriptively. This was time consuming and importantly
was subject to human errors and mistakes

A similar tool exists for TOUGH3 with PyTOUGH and PyTOUGHREACT extends its capability to TOUGHREACT with additional
capabilities for plotting.

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