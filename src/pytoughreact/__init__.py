import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pytoughreact.chemical.chemical_composition import WaterComp, Water, PrimarySpecies, ReactGas
from pytoughreact.chemical.kinetic_properties import pHDependenceType2, Dissolution, Precipitation
from pytoughreact.chemical.mineral_composition import MineralComp
from pytoughreact.chemical.mineral_description import Mineral
from pytoughreact.chemical.perm_poro_zone import PermPoro
from pytoughreact.writers.bio_writing import t2bio
from pytoughreact.chemical.biomass_composition import Component, Gas, Water_Bio, Biomass
from pytoughreact.chemical.bio_process_description import Process, BIODG
from pytoughreact.plotting.plot_single import PlotSingle
from .version import __version__
