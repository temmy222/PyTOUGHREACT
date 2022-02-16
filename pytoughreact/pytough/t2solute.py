from __future__ import print_function

import os
from copy import deepcopy

from pytoughreact.pytough.customError import ReactiveOptionsError, ReactiveConstraintsError, RequiredInput
from pytoughreact.pytough.t2incons import *
import struct

default_options = {
    'iteration_scheme': 2,
    'rsa_newton_raphson': 0,
    'linear_equation_solver': 5,
    'activity_coefficient_calculation': 0,
    'gaseous_species_in_transport': 0,
    'result_printout': 2,
    'poro_perm': 1,
    'co2_h2o_effects': 0,
    'itds_react': 0}

default_constraints = {
    'skip_saturation': 1e-4,
    'courant_number': 0.5,
    'maximum_ionic_strength': 14,
    'weighting_factor': 1}

default_readio = {
    'database': 'thddem.dat',
    'iteration_info': 'iter.out',
    'aqueous_concentration': 'kdd_conc.tec',
    'minerals': 'kdd_min.tec',
    'gas': 'kdd_gas.tec',
    'time': 'kdd_tim.tec'}

default_weight_diffusion = {
    'time_weighting': 1,
    'upstream_weighting': 1,
    'aqueous_diffusion_coefficient': 1.65e-10,
    'gas_diffusion_coefficient': 0}

default_tolerance = {
    'maximum_iterations_transport': 1,
    'transport_tolerance': 0.0001,
    'maximum_iterations_chemistry': 300,
    'chemistry_tolerance': 0.0001,
    'not_used1': 0.000,
    'not_used2': 0.000,
    'relative_concentration_change': 0.000,
    'relative_kinetics_change': 0.000
}

default_printout = {
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

default_zone = {
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


def primary_to_region_we(primary):
    """Returns thermodynamic region deduced from primary variables for EOS we."""
    from t2thermo import region
    if primary[1] < 1.:
        return 4
    else:
        return region(primary[1], primary[0])


def primary_to_region_wge(primary):
    """Returns thermodynamic region deduced from primary variables for wge
    (NCG) EOS (wce, wae)."""
    pwater = primary[0] - primary[2]
    return primary_to_region_we([pwater, primary[1]])


primary_to_region_funcs = {'w': primary_to_region_we, 'we': primary_to_region_we,
                           'wce': primary_to_region_wge, 'wae': primary_to_region_wge}
waiwera_eos_num_primary = {'w': 1, 'we': 2, 'wce': 3, 'wae': 3}


def trim_trailing_nones(vals):
    """Trim trailing None values from a list."""
    while vals and vals[-1] is None:
        vals.pop()
    return vals


t2solute_format_specification = {
    'title': [['title'], ['82s']],
    'options': [['ISPIA', 'itersfa', 'ISOLVC', 'NGAMM', 'NGAS1', 'ichdump', 'kcpl', 'Ico2h2o', 'nu'], ['6.1d'] * 9],
    'constraints': [['SL1MIN', 'rcour', 'STIMAX', 'CNFACT'], ['1.2e', '12.1f', '10.1d', '10.1d']],
    'readio': [['name', 'nad', 'density', 'porosity',
                'k1', 'k2', 'k3', 'conductivity', 'specific_heat'],
               ['5s', '5d'] + ['10.4e'] * 7],
    'weight_diffu': [['ITIME', 'WUPC', 'DFFUN', 'DFFUNG'],
                     ['6.1f', '9.1f', '12.4e', '12.4e']],
    'tolerance': [['MAXITPTR', 'TOLTR', 'MAXITPCH', 'TOLCH', 'NOT-USED', 'NOT-USED', 'TOLDC', 'TOLDR'],
                  ['6d', '15.4e', '8d'] + ['15.4e'] * 5],
    'printout': [
        ['NWTI', 'NWNOD', 'NWCOM', 'NWMIN', 'NWAQ', 'NWADS', 'NWEXC', 'iconflag', 'minflag', 'igasflag'],
        ['6d'] * 10],
    'nodes': [
        ['ELEM(a5)'],
        ['5s']],
    'primary_species': [
        ['number_pH'],
        ['20.1d']],
    'minerals': [
        ['rate_constant', 'activationEnergy', 'number_of_species', 'specie_name', 'species_exp'],
        ['30.4e', '5.1f', '5.1d', '10s', '5.1f']],
    'aqueous_species': [['type', ''] + ['parameter'] * 7, ['5d', '5x'] + ['10.3e'] * 7],
    'adsorption_species': [['max_iterations', 'print_level', 'max_timesteps',
                            'max_duration', 'print_interval',
                            '_option_str', 'diff0', 'texp', 'be'],
                           ['2d'] * 2 + ['4d'] * 3 + ['24s'] + ['10.3e'] * 3],
    'exchange_species': [['max_iterations', 'print_level', 'max_timesteps',
                          'max_duration', 'print_interval', '_option_str', 'texp', 'be'],
                         ['2d'] * 2 + ['4d'] * 3 + ['24s'] + ['10.3e'] * 2],
    'chemical_zones': [['IZIWDF', 'IZBWDF', 'IZMIDF', 'IZGSDF', 'IZADDF', 'IZEXDF', 'IZPPDF', 'IZKDDF', 'IZBGDF'],
                       ['4.1d'] + ['10.1d'] * 8],
    'chemical_zones_to_nodes': [
        ['ELEM(a5)', 'NSEQ', 'NADD', 'IZIWDF', 'IZBWDF', 'IZMIDF', 'IZGSDF', 'IZADDF', 'IZEXDF', 'IZPPDF', 'IZKDDF',
         'IZBGDF'],
        ['5s', '10.1d', '13.1d', '14.1d', '8.1d', '8.1d', '10.1d', '10.1d', '10.1d', '10.1d', '10.1d', '10.1d']],
}


class t2solute_parser(fixed_format_file):
    """Class for parsing TOUGH2 data file."""

    def __init__(self, filename, mode, read_function=default_read_function):
        super(t2solute_parser, self).__init__(filename, mode,
                                              t2solute_format_specification, read_function)


class fortran_unformatted_file(object):
    """Class for 'unformatted' binary file written by Fortran.  These are
    different from plain binary files in that the byte length of each
    'record' is written at its start and end.
    """

    def __init__(self, filename, mode):
        self.file = open(filename, mode)

    def close(self):
        self.file.close()

    def readrec(self, fmt):
        nb, = struct.unpack('i', self.file.read(4))
        packed = self.file.read(nb)
        self.file.read(4)
        return struct.unpack(fmt, packed)

    def writerec(self, fmt, val):
        nb = struct.calcsize(fmt)
        if isinstance(val, (tuple, list, np.ndarray)):
            packed = struct.pack(fmt, *val)
        else:
            packed = struct.pack(fmt, val)
        head = struct.pack('i', nb)
        self.file.write(head)
        self.file.write(packed)
        self.file.write(head)


t2solute_sections = [
    'TITLE', 'OPTIONS', 'CONSTRAINTS', 'READIO', 'WEIGHT_DIFFU', 'TOLERANCE', 'PRINTOUT', 'NODES',
    'PRIMARY_SPECIES', 'MINERALS', 'AQUEOUS_SPECIES', 'ADSORPTION_SPECIES',
    'EXCHANGE_SPECIES', 'CHEMICAL_ZONES', 'CHEMICAL_ZONES_TO_NODES']


class t2solute(object):
    def __init__(self, t2chemical=None, read_function=default_read_function):
        self.t2chemical = t2chemical
        self._sections = []
        if self.t2chemical is not None:
            self.title = self.t2chemical.title
        else:
            self.title = ''
        self.options = deepcopy(default_options)
        self.constraints = deepcopy(default_constraints)
        self.readio = deepcopy(default_readio)
        self.weight_diffusion = deepcopy(default_weight_diffusion)
        self.tolerance = deepcopy(default_tolerance)
        self.printout = deepcopy(default_printout)
        self.nodes_to_write = [-1]
        if self.t2chemical is not None:
            self.primary_species = self.t2chemical.primary_aqueous
        else:
            self.primary_species = []
        if self.t2chemical is not None:
            self.minerals = self.t2chemical.minerals
        else:
            self.minerals = []
        self.aqueous_species = [-1]
        self.adsorption_species = [-1]
        self.exchange_species = [-1]
        self.chemical_zones = deepcopy(default_zone)
        self.end_keyword = '# this "end" record is needed ' \
                           '\nend\n*************************************************************************** '
        self.initial_water_index = self.t2chemical.initial_water_index
        self.boundary_water_index = self.t2chemical.boundary_water_index
        self.mineral_index = self.t2chemical.mineral_index
        self.initial_gas_index = self.t2chemical.initial_gas_index
        self.injection_gas_index = self.t2chemical.injection_gas_index
        self.perm_poro_index = self.t2chemical.perm_poro_index
        self.read_function = read_function
        self.chemical_zones_to_nodes = self.getgrid_info()

    def getZoneValue(self, dict_to_check, value):
        key_list = list(dict_to_check.keys())
        val_list = list(dict_to_check.values())
        position = key_list.index(value)
        zone_number = val_list[position]
        return zone_number

    def getgrid_info(self):
        output = []
        viewer = []
        try:
            for block in self.t2chemical.t2grid.blocklist:
                initial_water = block.zone.water[0][0]
                mineral_in_block = block.zone.mineral_zone
                perm_poro = block.zone.permporo
                try:
                    initial_gas = block.zone.gas[0][0]
                except IndexError:
                    initial_gas = 0
                try:
                    boundary_water = block.zone.water[1][0]
                except IndexError:
                    boundary_water = 0
                try:
                    injection_gas = block.zone.gas[1][0]
                except IndexError:
                    injection_gas = 0
                initial_water_zone = self.getZoneValue(self.initial_water_index, initial_water)
                mineral_zone = self.getZoneValue(self.mineral_index, mineral_in_block)
                perm_poro_zone = self.getZoneValue(self.perm_poro_index, perm_poro)
                try:
                    initial_gas_zone = self.getZoneValue(self.initial_gas_index, initial_gas)
                    boundary_water_zone = self.getZoneValue(self.boundary_water_index, boundary_water)
                    injection_gas_zone = self.getZoneValue(self.injection_gas_index, injection_gas)
                except ValueError:
                    boundary_water_zone = 1
                    injection_gas_zone = 1
                    initial_gas_zone = 1
                appender = [block.name, 0, 0, initial_water_zone, boundary_water_zone, mineral_zone, initial_gas_zone, 0, 0,
                            perm_poro_zone, 0, injection_gas_zone]
                output.append(appender)
                viewer.append(block)
            return output
        except:
            return output

    # chemical_zones_to_nodes = property(getgrid_info)

    def update_read_write_functions(self):
        """Updates functions for reading and writing sections of data file."""

        self.read_fn = dict(zip(
            t2solute_sections,
            [self.read_title,
             self.read_options,
             self.read_constraints,
             self.read_readio,
             self.read_weight_diffu,
             self.read_tolerance,
             self.read_printout,
             self.read_nodes,
             self.read_primary_species,
             self.read_minerals,
             self.read_aqueous_species,
             self.read_adsorption_species,
             self.read_exchange_species,
             self.read_chemical_zones,
             self.read_chemical_zones_to_nodes
             ]))

        self.write_fn = dict(zip(
            t2solute_sections,
            [self.write_title,
             self.write_options,
             self.write_constraints,
             self.write_readio,
             self.write_weight_diffu,
             self.write_tolerance,
             self.write_printout,
             self.write_nodes,
             self.write_primary_species,
             self.write_minerals,
             self.write_aqueous_species,
             self.write_adsorption_species,
             self.write_exchange_species,
             self.write_chemical_zones,
             self.write_chemical_zones_to_nodes]))

    def get_present_sections(self):
        """Returns a list of TOUGH2 section keywords for which there are
        corresponding data in the t2bio object."""
        data_present = dict(zip(
            t2solute_sections,
            [self.title,
             self.options,
             self.constraints,
             self.readio,
             self.weight_diffusion,
             self.tolerance,
             self.printout,
             self.nodes_to_write,
             self.primary_species,
             self.minerals,
             self.aqueous_species,
             self.adsorption_species,
             self.exchange_species,
             self.chemical_zones,
             self.chemical_zones_to_nodes]))
        return [keyword for keyword in t2solute_sections if data_present[keyword]]

    present_sections = property(get_present_sections)

    def getGridBlocks(self):
        blk = []
        for t2block in self.t2chemical.t2grid.blocklist:
            blk.append(t2block.name)
        return blk

    def getInitialWaterIndex(self):
        water_dict = self.t2chemical.initial_water_index
        key_list = list(water_dict.keys())
        val_list = list(water_dict.values())
        return key_list, val_list

    def getInitialWater(self):
        zone_water = []
        for blk in self.t2chemical.t2grid.blocklist:
            zone_water.append(blk.zone.water[0])
        return zone_water

    def getBoundaryWaterIndex(self):
        water_dict = self.t2chemical.boundary_water_index
        key_list = list(water_dict.keys())
        val_list = list(water_dict.values())
        return key_list, val_list

    def getBoundaryWater(self):
        zone_water = []
        for blk in self.t2chemical.t2grid.blocklist:
            zone_water.append(blk.zone.water[1])
        return zone_water

    def getMineral(self):
        mineral_zone = []
        for blk in self.t2chemical.t2grid.blocklist:
            mineral_zone.append(blk.zone.mineral)
        return mineral_zone

    def insert_section(self, section):
        """Inserts a new section into the internal list of data file
        sections."""
        if section not in self._sections:
            i = self.section_insertion_index(section)
            self._sections.insert(i, section)

    def delete_section(self, section):
        """Deletes a section from the internal list of data file sections."""
        try:
            self._sections.remove(section)
        except ValueError:
            pass

    def section_insertion_index(self, section):
        """Determines an appropriate position to insert the specified section
        in the internal list of data file sections.
        """
        try:
            listindex = t2solute_sections.index(section)
            if listindex == 0:
                return 0  # SIMUL section
            else:
                # first look for sections above the one specified,
                # and put new one just after the last found:
                for i in reversed(range(listindex)):
                    try:
                        section_index = self._sections.index(t2solute_sections[i])
                        return section_index + 1
                    except ValueError:
                        pass
                # look for sections below the one specified,
                # and put new one just before the first found:
                for i in range(listindex, len(t2solute_sections)):
                    try:
                        section_index = self._sections.index(t2solute_sections[i])
                        return section_index
                    except ValueError:
                        pass
                return len(self._sections)
        except ValueError:
            return len(self._sections)

    def update_sections(self):
        """Updates internal section list, based on which properties are present."""
        present = self.present_sections
        missing = [keyword for keyword in present if keyword not in self._sections]
        for keyword in missing: self.insert_section(keyword)
        extra = [keyword for keyword in self._sections if keyword not in present]
        for keyword in extra: self.delete_section(keyword)

    def __repr__(self):
        return self.title

    def convert_to_t2solute(self, keyword):
        if 'options' in keyword.lower() and 'reactive' in keyword.lower():
            return 'OPTIONS'
        elif 'constraints' in keyword.lower() and 'reactive' in keyword.lower():
            return 'CONSTRAINTS'
        elif 'weighting' in keyword.lower() and 'diffusion' in keyword.lower():
            return 'WEIGHT_DIFFU'
        elif 'read' in keyword.lower() and 'input' in keyword.lower():
            return 'READIO'
        elif 'convergence' in keyword.lower() and 'tolerance' in keyword.lower():
            return 'TOLERANCE'
        elif 'printout' in keyword.lower() and 'control' in keyword.lower():
            return 'PRINTOUT'
        elif 'nodes' in keyword.lower() and 'output' in keyword.lower():
            return 'NODES'
        elif 'primary' in keyword.lower() and 'aqueous' in keyword.lower():
            return 'PRIMARY_SPECIES'
        elif 'mineral' in keyword.lower() and 'output' in keyword.lower():
            return 'MINERALS'
        elif 'aqueous' in keyword.lower() and 'output' in keyword.lower():
            return 'AQUEOUS_SPECIES'
        elif 'adsorption' in keyword.lower() and 'output' in keyword.lower():
            return 'ADSORPTION_SPECIES'
        elif 'exchange' in keyword.lower() and 'output' in keyword.lower():
            return 'EXCHANGE_SPECIES'
        elif 'chemical' in keyword.lower() and 'default' in keyword.lower():
            return 'CHEMICAL_ZONES'
        elif 'chemical' in keyword.lower() and 'zones' in keyword.lower():
            return 'CHEMICAL_ZONES_TO_NODES'
        else:
            return 'false'

    def read_title(self, infile):
        """Reads simulation title"""
        infile.read_value_line(self.__dict__, 'title')

    def write_title(self, outfile):
        if self.t2chemical is not None:
            self.title = self.t2chemical.title
        outfile.write('#Title' + '\n')
        outfile.write(self.title.strip() + '\n')

    def read_options(self, infile):
        """Reads reaction options"""
        params = infile.get_reactive_options()
        if len(params) == 0:
            raise ReactiveOptionsError
        else:
            self.__dict__['options']['iterative_scheme'] = int(params[0])
            self.__dict__['options']['rsa_newton_raphson'] = int(params[1])
            self.__dict__['options']['linear_equation_solver'] = int(params[2])
            self.__dict__['options']['activity_coefficient_calculation'] =int(params[3])
            self.__dict__['options']['gaseous_species_in_transport'] = int(params[4])
            self.__dict__['options']['result_printout'] = int(params[5])
            self.__dict__['options']['poro_perm'] =int(params[6])
            self.__dict__['options']['co2_h2o_effects'] = int(params[7])
            self.__dict__['options']['itds_react'] = int(params[8])

    def write_options(self, outfile):
        outfile.write('#options for reactive chemical transport ' + '\n')
        outfile.write('# ISPIA itersfa ISOLVC NGAMM NGAS1 ichdump kcpl Ico2h2o  nu' + '\n')
        vals = [self.options['iteration_scheme'], self.options['rsa_newton_raphson'],
                self.options['linear_equation_solver'], self.options['activity_coefficient_calculation'],
                self.options['gaseous_species_in_transport'], self.options['result_printout'],
                self.options['poro_perm'], self.options['co2_h2o_effects'],
                self.options['itds_react']]
        outfile.write_values(vals, 'options')

    def read_constraints(self, infile):
        """Reads simulation constraints"""
        params = infile.get_reactive_constraints()
        if len(params) == 0:
            raise ReactiveConstraintsError
        else:
            self.__dict__['constraints']['skip_saturation'] = float(params[0])
            self.__dict__['constraints']['courant_number'] = float(params[1])
            self.__dict__['constraints']['maximum_ionic_strength'] = float(params[2])
            self.__dict__['constraints']['weighting_factor'] = float(params[3])


    def write_constraints(self, outfile):
        outfile.write('#constraints for reactive chemical transport ' + '\n')
        outfile.write('# SL1MIN        rcour     STIMAX    CNFACT(=1 fully implicit)' + '\n')
        vals = [self.constraints['skip_saturation'], self.constraints['courant_number'],
                self.constraints['maximum_ionic_strength'], self.constraints['weighting_factor']]
        outfile.write_values(vals, 'constraints')

    def read_readio(self, infile):
        """Reads simulation title"""
        params = infile.get_readio()
        if len(params) == 0:
            raise RequiredInput
        else:
            self.__dict__['readio']['database'] = params[0]
            self.__dict__['readio']['iteration_info'] = params[1]
            self.__dict__['readio']['aqueous_concentration'] = params[2]
            self.__dict__['readio']['minerals'] = params[3]
            self.__dict__['readio']['gas'] = params[4]
            self.__dict__['readio']['time'] = params[5]

    def write_readio(self, outfile):
        outfile.write('#Read input and output file names' + '\n')
        outfile.write(self.readio['database'] + '\n')
        outfile.write(self.readio['iteration_info'] + '\n')
        outfile.write(self.readio['aqueous_concentration'] + '\n')
        outfile.write(self.readio['minerals'] + '\n')
        outfile.write(self.readio['gas'] + '\n')
        outfile.write(self.readio['time'] + '\n')

    def read_weight_diffu(self, infile):
        """Reads weight and diffusion"""
        params = infile.get_weight_diffusion()
        if len(params) == 0:
            raise RequiredInput
        else:
            self.__dict__['weight_diffusion']['time_weighting'] = float(params[0])
            self.__dict__['weight_diffusion']['upstream_weighting'] = float(params[1])
            self.__dict__['weight_diffusion']['aqueous_diffusion_coefficient'] = float(params[2])
            self.__dict__['weight_diffusion']['gas_diffusion_coefficient'] = float(params[3])

    def write_weight_diffu(self, outfile):
        outfile.write('# Weighting space/time, aq. and gas diffusion coeffs' + '\n')
        outfile.write('# ITIME     WUPC   DFFUN     DFFUNG' + '\n')
        vals = [self.weight_diffusion['time_weighting'], self.weight_diffusion['upstream_weighting'],
                self.weight_diffusion['aqueous_diffusion_coefficient'],
                self.weight_diffusion['gas_diffusion_coefficient']]
        outfile.write_values(vals, 'weight_diffu')

    def read_tolerance(self, infile):
        """Reads tolerance values"""
        params = infile.get_tolerance_values()
        if len(params) == 0:
            raise RequiredInput
        else:
            self.__dict__['tolerance']['maximum_iterations_transport'] = int(params[0])
            self.__dict__['tolerance']['transport_tolerance'] = float(params[1])
            self.__dict__['tolerance']['maximum_iterations_chemistry'] = int(params[2])
            self.__dict__['tolerance']['chemistry_tolerance'] = float(params[3])
            self.__dict__['tolerance']['not_used1'] = float(params[4])
            self.__dict__['tolerance']['not_used2'] = float(params[5])
            self.__dict__['tolerance']['relative_concentration_change'] = float(params[6])
            self.__dict__['tolerance']['relative_kinetics_change'] = float(params[7])

    def write_tolerance(self, outfile):
        outfile.write('# Convergence and tolerance parameters' + '\n')
        outfile.write('#  MAXITPTR  TOLTR    MAXITPCH  TOLCH    NOT-USED  NOT-USED    TOLDC    TOLDR' + '\n')
        vals = [self.tolerance['maximum_iterations_transport'], self.tolerance['transport_tolerance'],
                self.tolerance['maximum_iterations_chemistry'], self.tolerance['chemistry_tolerance'],
                self.tolerance['not_used1'], self.tolerance['not_used2'],
                self.tolerance['relative_concentration_change'], self.tolerance['relative_kinetics_change']]
        outfile.write_values(vals, 'tolerance')

    def read_printout(self, infile):
        """Reads printout_options"""
        params = infile.get_printout_options()
        if len(params) == 0:
            raise RequiredInput
        else:
            self.__dict__['printout']['printout_frequency'] = int(params[0])
            self.__dict__['printout']['number_of_gridblocks'] = int(params[1])
            self.__dict__['printout']['number_of_chemical_components'] = int(params[2])
            self.__dict__['printout']['number_of_minerals'] = int(params[3])
            self.__dict__['printout']['number_of_aqueous'] = int(params[4])
            self.__dict__['printout']['number_of_surface_complexes'] = int(params[5])
            self.__dict__['printout']['number_of_exchange_species'] = int(params[6])
            self.__dict__['printout']['aqueous_unit'] = int(params[7])
            self.__dict__['printout']['mineral_unit'] = int(params[8])
            self.__dict__['printout']['gas_unit'] =int(params[9])

    def write_printout(self, outfile):
        outfile.write('# Printout control variables:' + '\n')
        outfile.write('# NWTI NWNOD NWCOM NWMIN NWAQ NWADS NWEXC iconflag minflag igasflag' + '\n')
        vals = [self.printout['printout_frequency'], self.printout['number_of_gridblocks'],
                self.printout['number_of_chemical_components'], self.printout['number_of_minerals'],
                self.printout['number_of_aqueous'], self.printout['number_of_surface_complexes'],
                self.printout['number_of_exchange_species'], self.printout['aqueous_unit'],
                self.printout['mineral_unit'], self.printout['gas_unit']]
        outfile.write_values(vals, 'printout')

    def read_nodes(self, infile):
        """Reads nodes to write"""
        params = infile.get_nodes_to_read(self.t2chemical.t2grid)
        if len(params) == 0:
            pass
        else:
            self.__dict__['nodes_to_write'] = params


    def write_nodes(self, outfile):
        if self.nodes_to_write[0] == -1:
            outfile.write('# Nodes for which to output data in time file (15a5):' + '\n')
        else:
            outfile.write('# Nodes for which to output data in time file (15a5):' + '\n')
            nodes = []
            for i in range(len(self.nodes_to_write)):
                nodes.append(self.t2chemical.t2grid.blocklist[i].name)
            for node in nodes:
                outfile.write(node + '\n')

    def read_primary_species(self, infile):
        """Reads primary species to write"""
        params = infile.get_primary_species_to_read(self.t2chemical.primary_aqueous)
        if len(params) == 0:
            pass
        else:
            self.__dict__['primary_species'] = params

    def write_primary_species(self, outfile):
        outfile.write(
            '# Primary (total) aqueous species for which to output concentrations in time and plot files:' + '\n')
        if self.t2chemical is not None:
            vals = []
            for species in self.primary_species:
                vals.append(species.NAME.strip())
            for val in vals:
                outfile.write(val + '\n')
        else:
            vals = self.primary_species
            for val in vals:
                outfile.write(val + '\n')

    def read_minerals(self, infile):
        """Reads minerals to write"""
        params = infile.get_minerals_to_write(self.t2chemical.minerals)
        if len(params) == 0:
            pass
        else:
            self.__dict__['minerals'] = params

    def write_minerals(self, outfile):
        outfile.write('# Minerals for which to output data in time and plot files:' + '\n')
        if self.t2chemical is not None:
            vals = []
            for mineral in self.minerals:
                vals.append(mineral.name)
            for val in vals:
                outfile.write(val + '\n')
        else:
            vals = []
            for mineral in self.minerals:
                vals.append(mineral.name)
            for val in vals:
                outfile.write(val + '\n')

    def read_aqueous_species(self, infile):
        """Reads aqueous species to write"""
        pass

    def write_aqueous_species(self, outfile):
        # TODO find out why leaving a space doesnt run
        if self.aqueous_species[0] == -1:
            outfile.write("\n")
            # outfile.write('# Individual aqueous species for which to output concentrations in time and plot files:' + ' \n tr' )
            outfile.write(
                '# Individual aqueous species for which to output concentrations in time and plot files:' + '\n')


    def read_adsorption_species(self, infile):
        """Reads adsorption_species to write"""
        pass

    def write_adsorption_species(self, outfile):
        if self.adsorption_species[0] == -1:
            outfile.write('# Adsorption species for which to output concentrations in time and plot files:' + ' \n')

    def read_exchange_species(self, infile):
        """Reads exchange species to write"""
        pass

    def write_exchange_species(self, outfile):
        if self.exchange_species[0] == -1:
            outfile.write('# Exchange species for which to output concentrations in time and plot files:' + ' \n')

    def read_chemical_zones(self, infile):
        """Reads default chemical zones"""
        params = infile.get_default_chemical_zones()
        if len(params) == 0:
            raise RequiredInput
        else:
            self.__dict__['chemical_zones']['IZIWDF'] = int(params[0])
            self.__dict__['chemical_zones']['IZBWDF'] = int(params[1])
            self.__dict__['chemical_zones']['IZMIDF'] = int(params[2])
            self.__dict__['chemical_zones']['IZGSDF'] = int(params[3])
            self.__dict__['chemical_zones']['IZADDF'] = int(params[4])
            self.__dict__['chemical_zones']['IZEXDF'] = int(params[5])
            self.__dict__['chemical_zones']['IZPPDF'] = int(params[6])
            self.__dict__['chemical_zones']['IZKDDF'] = int(params[7])
            self.__dict__['chemical_zones']['IZBGDF'] = int(params[8])


    def write_chemical_zones(self, outfile):
        outfile.write('# Default types of chemical zones' + '\n')
        outfile.write('# Initial  Boundary                                      Porosity/ ' + '\n')
        outfile.write(
            '#  Water    Water   Minerals   Gases Adsorption Exchange  Permeab  Kd zones  Injection Gas Zones' + '\n')
        outfile.write('# IZIWDF   IZBWDF    IZMIDF   IZGSDF   IZADDF    IZEXDF   IZPPDF    IZKDDF     IZBGDF' + '\n')
        vals = [self.chemical_zones['IZIWDF'], self.chemical_zones['IZBWDF'],
                self.chemical_zones['IZMIDF'], self.chemical_zones['IZGSDF'],
                self.chemical_zones['IZADDF'], self.chemical_zones['IZEXDF'],
                self.chemical_zones['IZPPDF'], self.chemical_zones['IZKDDF'],
                self.chemical_zones['IZBGDF']]
        outfile.write_values(vals, 'chemical_zones')

    def map_zone_to_blocks(self, params):
        for param in params:
            grid_name = param[0]
            zone = self.t2chemical.t2grid.block[grid_name].zone
            if zone.water is None:
                zone.gas = [[], []]
                zone.water = [[], []]
                nseq = int(param[1])
                nadd = int(param[2])
                initial_water = int(param[3])
                boundary_water = int(param[4])
                mineral = int(param[5])
                initial_gas = int(param[6])
                adsorption = int(param[7])
                exchange = int(param[8])
                perm_poro = int(param[9])
                decay_zone = int(param[10])
                injection_gas = int(param[11])
                zone.mineral_zone = self.t2chemical.initial_minerals_mapping[mineral]
                zone.gas[0] = self.t2chemical.initial_gas_mapping[initial_gas]
                try:
                    zone.gas[1] = self.t2chemical.injection_gas_mapping[injection_gas]
                except:
                    pass
                zone.water[0] = self.t2chemical.initial_waters_mapping[initial_water]
                try:
                    zone.water[1] = self.t2chemical.boundary_waters_mapping[boundary_water]
                except:
                    pass
                zone.permporo = self.t2chemical.initial_perm_poro_mapping[perm_poro]
            else:
                pass


    def read_chemical_zones_to_nodes(self, infile):
        """Reads simulation title"""
        params = infile.get_default_chemical_zone_to_nodes()
        if len(params) == 0:
            block_data = self.generate_zone_to_blocks()
            self.map_zone_to_blocks( block_data)
            self.__dict__['chemical_zones_to_nodes'] =  block_data
        else:
            self.map_zone_to_blocks(params)
            self.__dict__['chemical_zones_to_nodes'] = params

    def generate_zone_to_blocks(self):
        all_blocks = []
        for block in self.t2chemical.t2grid.blocklist:
            all_blocks.append([block.name, 0, 0] + list(self.chemical_zones.values()))
        return all_blocks

    def write_chemical_zones_to_nodes(self, outfile):
        outfile.write('# Types of chemical zones for specific nodes (optional)' + '\n')
        outfile.write('# Gridblock  Gridblocks Increment   Water    Water     Minerals   Gases  Adsorption Exchange  '
                      'Permeab  Kd zones Injection Gas Zones' + '\n')
        outfile.write('# ELEM(a5)   NSEQ         NADD       IZIWDF   IZBWDF    IZMIDF   IZGSDF   IZADDF    IZEXDF    '
                      'IZPPDF   IZKDDF     IZBGDF' + '\n')
        for vals in self.chemical_zones_to_nodes:
            outfile.write_values(vals, 'chemical_zones_to_nodes')

    def write(self, filename='', meshfilename='',runlocation='',
              extra_precision=None, echo_extra_precision=None):
        if runlocation:
            if not os.path.isdir(runlocation): os.mkdir(runlocation)
            os.chdir(runlocation)
        if filename == '': filename = 'solute.inp'
        self.update_sections()
        self.update_read_write_functions()
        outfile = t2solute_parser(filename, 'w')
        for keyword in self._sections:
            self.write_fn[keyword](outfile)
            outfile.write('\n')
        outfile.write(self.end_keyword + '\n')
        self.status = 'successful'
        outfile.close()

    def read(self, filename='', meshfilename='', runlocation='',
              extra_precision=None, echo_extra_precision=None):
        if runlocation:
            if not os.path.isdir(runlocation): os.mkdir(runlocation)
            os.chdir(runlocation)
        if filename: self.filename = filename
        mode = 'r' if sys.version_info > (3,) else 'rU'
        infile = t2solute_parser(self.filename, mode, read_function=self.read_function)
        self.read_title(infile)
        self._sections = []
        self.update_read_write_functions()
        more = True
        next_line = None
        countline = 0
        while more:
            if next_line:
                line = next_line
            else:
                line = infile.readline()
            if line:
                # keyword = line[0: 5].strip()
                keyword = line[1:]
                check_presence = self.convert_to_t2solute(keyword)
                if keyword in ['ENDCY', 'ENDFI', 'end']:
                    more = False
                    self.end_keyword = keyword
                # elif keyword in t2chemical_read_sections:
                # elif any(ext in keyword for ext in t2chemical_read_sections):
                elif check_presence != 'false':
                    keyword = check_presence
                    fn = self.read_fn[keyword]
                    next_line = None
                    if keyword == 'SHORT':
                        fn(infile, line)
                    elif keyword == 'PARAM':
                        next_line = fn(infile)
                    else:
                        fn(infile)
                    self._sections.append(keyword)
            else:
                more = False
        self.status = 'successful'
        infile.close()


