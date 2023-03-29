'''
MIT License

Copyright (c) [2022] [Temitope Ajayi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

t2solute_sections = [
    'TITLE', 'OPTIONS', 'CONSTRAINTS', 'READIO', 'WEIGHT_DIFFU', 'TOLERANCE', 'PRINTOUT', 'NODES',
    'PRIMARY_SPECIES', 'MINERALS', 'AQUEOUS_SPECIES', 'ADSORPTION_SPECIES',
    'EXCHANGE_SPECIES', 'CHEMICAL_ZONES', 'CHEMICAL_ZONES_TO_NODES']

t2chemical_sections = [
    'TITLE', 'PRIMARY_AQUEOUS', 'AQUEOUS_KINETICS', 'AQUEOUS_COMPLEXES', 'MINERALS', 'GASES', 'SURFACE_COMPLEXES',
    'DECAY_SPECIES', 'EXCHANGEABLE_CATIONS', 'IB_WATERS', 'MINERAL_ZONES',
    'IJ_GAS', 'PERM_PORO', 'SURFACE_ADSORPTION', 'LINEAR_EQUILIBRIUM', 'CATION_EXCHANGE']

t2chemical_read_sections = [
    'TITLE', 'PRIMARY AQUEOUS', 'AQUEOUS KINETICS', 'AQUEOUS COMPLEXES', 'MINERALS', 'GASES', 'SURFACE COMPLEXES',
    'DECAY_SPECIES', 'EXCHANGEABLE_CATIONS', 'Initial Boundary WATERS', 'MINERAL ZONES',
    'Initial Injection GAS', 'PERMeability Porosity', 'Surface Adsorption', 'LINEAR EQUILIBRIUM', 'CATION EXCHANGE']

t2bio_sections = [
    'SIMUL', 'ROCKS', 'MULTI', 'CHEMP', 'NCGAS', 'BIODG', 'SOLIDS', 'PARAM', 'MOMOP', 'START', 'NOVER', 'RPCAP',
    'LINEQ', 'SOLVR', 'TIMES', 'SELEC', 'DIFFU',
    'ELEME', 'CONNE', 'MESHM', 'GENER', 'SHORT', 'FOFT',
    'COFT', 'GOFT', 'INCON', 'INDOM']

t2react_sections = [
    'SIMUL', 'ROCKS', 'PARAM', 'REACT', 'MOMOP', 'START', 'NOVER', 'RPCAP',
    'LINEQ', 'SOLVR', 'MULTI', 'TIMES', 'SELEC', 'DIFFU',
    'ELEME', 'CONNE', 'MESHM', 'GENER', 'SHORT', 'FOFT',
    'COFT', 'GOFT', 'INCON', 'INDOM']
