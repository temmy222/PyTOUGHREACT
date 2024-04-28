import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pytoughreact.chemical.chemical_composition import WaterComp, Water, PrimarySpecies, ReactGas
from pytoughreact.chemical.kinetic_properties import PHDependenceType2, Dissolution, Precipitation, Kinetic
from pytoughreact.chemical.kinetic_properties import Equilibrium, PHDependenceType1
from pytoughreact.chemical.mineral_composition import MineralComp
from pytoughreact.chemical.mineral_description import Mineral
from pytoughreact.chemical.perm_poro_zone import PermPoro, PermPoroZone
from pytoughreact.chemical.mineral_zone import MineralZone
from pytoughreact.writers.bio_writing import T2Bio, T2BioParser
from pytoughreact.chemical.biomass_composition import Component, Gas, WaterBio, Biomass, BaseComponent, Solids
from pytoughreact.chemical.bio_process_description import Process, BIODG
from pytoughreact.plotting.plot_single import PlotSingle
from pytoughreact.wrapper.react_data import ReactData
from pytoughreact.wrapper.reactblock import T2Block
from pytoughreact.wrapper.reactgrid import T2ReactGrid
from pytoughreact.wrapper.reactzone import T2Zone
from pytoughreact.writers.chemical_writing import T2Chemical, T2ChemicalData
from pytoughreact.writers.react_writing import T2React, T2ReactParser, T2ExtraPrecisionDataParser
from pytoughreact.writers.solute_writing import T2Solute, T2SoluteParser


from .version import __version__
