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

import numpy as np

DEFAULT_OPTIONS = {
    'iteration_scheme': 2,
    'rsa_newton_raphson': 0,
    'linear_equation_solver': 5,
    'activity_coefficient_calculation': 0,
    'gaseous_species_in_transport': 0,
    'result_printout': 2,
    'poro_perm': 1,
    'co2_h2o_effects': 0,
    'itds_react': 0}

DEFAULT_CONSTRAINTS = {
    'skip_saturation': 1e-4,
    'courant_number': 0.5,
    'maximum_ionic_strength': 14,
    'weighting_factor': 1}

DEFAULT_READIO = {
    'database': 'thddem.dat',
    'iteration_info': 'iter.out',
    'aqueous_concentration': 'kdd_conc.tec',
    'minerals': 'kdd_min.tec',
    'gas': 'kdd_gas.tec',
    'time': 'kdd_tim.tec'}

DEFAULT_WEIGHT_DIFFUSION = {
    'time_weighting': 1,
    'upstream_weighting': 1,
    'aqueous_diffusion_coefficient': 1.65e-10,
    'gas_diffusion_coefficient': 0}

DEFAULT_TOLERANCE = {
    'maximum_iterations_transport': 1,
    'transport_tolerance': 0.0001,
    'maximum_iterations_chemistry': 300,
    'chemistry_tolerance': 0.0001,
    'not_used1': 0.000,
    'not_used2': 0.000,
    'relative_concentration_change': 0.000,
    'relative_kinetics_change': 0.000
}

DEFAULT_PRINTOUT = {
    'printout_frequency': 1000,
    'number_of_gridblocks': 1,
    'number_of_chemical_components': -1,
    'number_of_minerals': -1,
    'number_of_aqueous': 0,
    'number_of_surface_complexes': 0,
    'number_of_exchange_species': 0,
    'aqueous_unit': 1,
    'mineral_unit': 1,
    'gas_unit': 1,
}

DEFAULT_ZONE = {
    'IZIWDF': 1,
    'IZBWDF': 1,
    'IZMIDF': 1,
    'IZGSDF': 1,
    'IZADDF': 0,
    'IZEXDF': 0,
    'IZPPDF': 1,
    'IZKDDF': 0,
    'IZBGDF': 1
}


DEFAULT_MINERAL_INCON = {
    'init_volume_fraction': 0.2,
    'reaction_type': 1,
    'radius': 0.0E-00,
    'reactive surface area': 100.0,
    'unit': 0,
    'zone': 1
}

DEFAULT_PARAMETERS = {
    'max_iterations': None,
    'print_level': None,
    'max_timesteps': None,
    'max_duration': None,
    'print_interval': None,
    '_option_str': '0' * 24,
    'option': np.zeros(25, int),
    'diff0': None,
    'texp': None,
    'tstart': 0.0,
    'tstop': None,
    'const_timestep': 0.0,
    'timestep': [],
    'max_timestep': None,
    'print_block': None,
    'gravity': 0.0,
    'timestep_reduction': None,
    'scale': None,
    'relative_error': None,
    'absolute_error': None,
    'pivot': None,
    'upstream_weight': None,
    'newton_weight': None,
    'derivative_increment': None,
    'phase_index': None,
    'default_incons': []}


DEFAULT_REACT = [0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


