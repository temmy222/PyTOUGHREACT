"""For reading, parsing and writing fixed format text files.

Copyright 2013 University of Auckland.

This file is part of PyTOUGH.

PyTOUGH is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

PyTOUGH is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with PyTOUGH.  If not, see <http://www.gnu.org/licenses/>."""
import copy

from numpy import nan

from pytoughreact.ChemicalCompositions.mineral import Mineral, Dissolution, pHDependenceType2, pHDependenceType1, \
    Precipitation, MineralComp, MineralZone, PermPoroZone
from pytoughreact.ChemicalCompositions.primaryspecies import ReactGas, WaterComp, Water
from pytoughreact.ChemicalCompositions.zone import PermPoro
from functools import partial


def fortran_float(s, blank_value=0.0):
    """Returns float of a string written by Fortran.
    Its behaviour is different from the float() function in the following ways:
    - a blank string will return the specified blank value (default zero)
    - embedded spaces are ignored
    - 'd' specifier will be treated the same as 'e'
    - underflow or overflow in exponent, with the 'e' omitted,
      are treated as if the 'e' was present
    If any other errors are encountered, np.nan is returned."""
    try:
        return float(s)
    except ValueError:
        s = s.strip()
        if not s:
            return blank_value
        else:
            try:
                s = s.lower().replace('d', 'e').replace(' ', '')
                return float(s)
            except:
                try:
                    return float(''.join([s[0], s[1:].replace('-', 'e-')]))
                except ValueError:
                    try:
                        return float(''.join([s[0], s[1:].replace('+', 'e')]))
                    except ValueError:
                        return nan
    except:
        return nan


def fortran_int(s, blank_value=0):
    """Returns float of a string written by Fortran.
    Its behaviour is different from the float() function in the following ways:
    - a blank string will return the specified blank value (default zero)
    - embedded spaces are ignored
    If any other errors are encountered, None is returned."""
    try:
        return int(s)
    except ValueError:
        s = s.strip()
        if not s:
            return blank_value
        else:
            try:
                s = s.replace(' ', '')
                return int(s)
            except:
                return None


def value_error_none(f):
    """Wraps a function with a handler to return None on a ValueError
    exception."""

    def fn(x):
        try:
            return f(x)
        except ValueError:
            return None

    return fn


default_read_float = value_error_none(float)
default_read_int = value_error_none(int)
default_read_str = value_error_none(lambda x: x.rstrip('\n'))
default_read_space = lambda x: None
fortran_read_float = partial(fortran_float, blank_value=None)
fortran_read_int = partial(fortran_int, blank_value=None)


def read_function_dict(floatfn=default_read_float, intfn=default_read_int,
                       strfn=default_read_str, spacefn=default_read_space):
    """Returns a conversion function dictionary using the specified functions for float,
    int, string and space."""
    result = {'s': strfn, 'x': spacefn, 'd': intfn}
    for typ in ['f', 'e', 'g']:
        result[typ] = floatfn
    return result


default_read_function = read_function_dict()
fortran_read_function = read_function_dict(fortran_read_float, fortran_read_int)


class fixed_format_file(object):
    """Class for fixed format text file.  Values from the file may be
    parsed into variables, according to a specification dictionary.
    The keys of the specification dictionary are arbitrary and may be
    assigned for convenience, e.g. referring to specific sections or
    lines in the file.  Each value in the specification dictionary is
    a list of two lists: first a list of the names of variables in the
    specification, then a list of the corresponding format
    specifications.  The individual format specifications are like
    those in Python formats, consisting of an integer width value
    followed by a type ('d' for integer, 'f' for float etc.).  The
    default conversion functions also allow an 'x' specifier for
    blanks (like fortran), which returns None.
    """

    def __init__(self, filename, mode, specification,
                 read_function=default_read_function):
        self.specification = specification
        self.read_function = read_function
        self.preprocess_specification()
        self.file = open(filename, mode)

    def readline(self):
        """Returns next line from file."""
        return self.file.readline()

    def write(self, s):
        """Writes string s to file."""
        self.file.write(s)

    def close(self):
        """Closes file."""
        self.file.close()

    def preprocess_specification(self):
        """Pre-process specifications to speed up parsing."""
        self.line_spec, self.spec_width = {}, {}
        for section, [names, specs] in self.specification.items():
            self.line_spec[section] = []
            pos = 0
            for spec in specs:
                fmt, typ = spec[:-1], spec[-1]
                w = int(fmt.partition('.')[0])
                nextpos = pos + w
                self.line_spec[section].append(((pos, nextpos), typ))
                pos = nextpos
                self.spec_width[fmt] = w

    def parse_string(self, line, linetype):
        """Parses a string into values according to specified input format
        (d,f,s, or x for integer, float, string or skip).  Blanks are
        converted to None.
        """
        return [self.read_function[typ](line[i1:i2]) for
                (i1, i2), typ in self.line_spec[linetype]]

    def write_values_to_string(self, vals, linetype):
        """Inverse of parse_string()."""
        fmt = self.specification[linetype][1]
        strs = []
        for val, f in zip(vals, fmt):
            if (val is not None) and (f[-1] != 'x'):
                valstr = ('%%%s' % f) % val
            else:
                valstr = ' ' * self.spec_width[f[0:-1]]  # blank
            strs.append(valstr)
        return ''.join(strs)

    def read_values(self, linetype):
        """Reads a line from the file, parses it and returns the values."""
        line = self.file.readline()
        if line.startswith('#'):
            line = self.file.readline()
        return self.parse_string(line, linetype)

    def get_param_values(self, linetype):
        line = 'start'
        all_lines = []
        while line.startswith("'*") is False:
            line = self.file.readline()
            particular_line = self.parse_string(line, linetype)
            if line.startswith("'*") is False:
                all_lines.append(particular_line)
        return all_lines

    def get_param_values_mineral(self):
        line = 'start'
        all_lines = []
        line = self.file.readline()
        while line.startswith("'*") is False:
            liner = (line.split())
            precip_presence = int(liner[2])
            presence = any(c.isalpha() for c in liner[0])
            if presence is True:
                mineral = Mineral(liner[0], int(liner[1]), int(liner[2]), int(liner[3]), int(liner[4]))
                line = self.file.readline()
                liner = (line.split())
                read_dissolution = Dissolution(float(liner[0]), int(liner[1]), float(liner[2]), float(liner[3]), float(liner[4]), float(liner[5]), float(liner[6]),
                                               float(liner[7]))
                type_of_pH = liner[1]
                if int(type_of_pH) == 0:
                    mineral.dissolution = [read_dissolution]
                else:
                    line = self.file.readline()
                    liner = (line.split())
                    if liner[0].isnumeric():
                        number_of_ph = int(liner[0])
                        ph_deps = []
                        for i in range(number_of_ph):
                            line = self.file.readline()
                            liner = (line.split())
                            if type_of_pH == '2':
                                ph_dep = pHDependenceType2(float(liner[0]), float(liner[1]), int(liner[2]), liner[3], float(liner[4]))
                            elif type_of_pH == '1':
                                ph_dep = pHDependenceType1(float(liner[0]), int(liner[1]), float(liner[2]), int(liner[3]))
                            ph_deps.append(ph_dep)
                        read_dissolution.pHDependence = ph_deps
                        mineral.dissolution = [read_dissolution]
                presence = any(c.isalpha() for c in liner[0])
                if precip_presence > 1:
                    line = self.file.readline()
                    liner = (line.split())
                    init_line = liner
                    line = self.file.readline()
                    liner = (line.split())
                    liner = init_line + liner
                    read_precipitation = Precipitation(float(liner[0]), int(liner[1]), float(liner[2]), float(liner[3]), float(liner[4]), float(liner[5]), float(liner[6]),
                                                       float(liner[7]), float(liner[8]), int(liner[9]), float(liner[10]), float(liner[11]), float(liner[12]))
                    mineral.precipitation = [read_precipitation]
            all_lines.append(mineral)
            line = self.file.readline()
        return all_lines

    def get_param_values_gas(self):
        all_lines = []
        line = self.file.readline()
        while line.startswith("'*") is False:
            liner = (line.split())
            react_gas = ReactGas(liner[0], int(liner[1]), 0)
            all_lines.append(react_gas)
            line = self.file.readline()

        return all_lines

    def get_param_values_surface_complex(self):
        all_lines = []
        # line = self.file.readline()
        # while line.startswith("'*") is False:
        #     liner = (line.split())

        return all_lines

    def get_param_values_decay_species(self):
        all_lines = []
        # line = self.file.readline()
        # while line.startswith("'*") is False:
        #     liner = (line.split())

        return all_lines

    def get_param_values_exchangeable_cations(self):
        all_lines = []
        # line = self.file.readline()
        # while line.startswith("'*") is False:
        #     liner = (line.split())

        return all_lines

    def get_reactive_options(self):
        line = self.file.readline()
        line = self.file.readline()
        liner = (line.split())
        return liner

    def get_reactive_constraints(self):
        line = self.file.readline()
        line = self.file.readline()
        liner = (line.split())
        return liner

    def get_readio(self):
        all_values = []
        for i in range(6):
            line = self.file.readline()
            liner = (line.split())
            all_values.append(liner[0])

        return all_values

    def get_weight_diffusion(self):
        line = self.file.readline()
        line = self.file.readline()
        liner = (line.split())
        return liner

    def get_tolerance_values(self):
        line = self.file.readline()
        line = self.file.readline()
        liner = (line.split())
        return liner

    def get_printout_options(self):
        line = self.file.readline()
        line = self.file.readline()
        liner = (line.split())
        return liner

    def search_for_node_index(self, blocks, nodes):
        indexes = []
        for i in range(len(nodes)):
            for j in range(len(blocks)):
                if blocks[j].name == nodes[i]:
                    indexes.append(j)
        return indexes

    def get_nodes_to_read(self, grid):
        all_values = []
        line = self.file.readline()
        while len(line.strip()) != 0:
            all_values.append(line.rstrip())
            line = self.file.readline()

        output = self.search_for_node_index(grid.blocklist, all_values)
        return output

    def get_primary_species_to_read(self, primary_aqueous):
        all_values = []
        line = self.file.readline()
        while len(line.strip()) != 0:
            specie = self.find_primary_aqueous(primary_aqueous, line.rstrip())
            all_values.append(specie)
            line = self.file.readline()

        return all_values

    def get_minerals_to_write(self, minerals):
        all_values = []
        line = self.file.readline()
        while len(line.strip()) != 0:
            specie = self.find_minerals(minerals, line.rstrip())
            all_values.append(specie)
            line = self.file.readline()

        return all_values

    def get_default_chemical_zones(self):
        line = self.file.readline()
        line = self.file.readline()
        line = self.file.readline()
        line = self.file.readline()
        liner = (line.split())
        return liner

    def get_default_chemical_zone_to_nodes(self):
        line = self.file.readline()
        line = self.file.readline()
        line = self.file.readline()
        all_values = []
        while len(line.strip()) != 0:
            grid_name = []
            grid_name.append(line[0:5])
            liner = (line.split())
            value = grid_name + liner[2:]
            for i in range(1, len(value)):
                value[i] = int(value[i])
            line = self.file.readline()
            all_values.append(value)
        return all_values

    def find_primary_aqueous(self, primary_aqueous, name):
        startIndex = name.find('\'')
        if startIndex >= 0:
            name = name.replace("'", "")
        for i in range(len(primary_aqueous)):
            if name.lower() == primary_aqueous[i].NAME.strip().lower():
                return primary_aqueous[i]

    def get_param_values_ib_waters(self, primary_aqueous, grid):
        initial_waters_mapping = {}
        initial_waters_list = []
        boundary_waters_mapping = {}
        boundary_waters_list = []
        line = self.file.readline()
        liner = (line.split())
        number_of_initial_waters = int(liner[0])
        if len(liner) > 1:
            number_of_boundary_waters = int(liner[1])
        line = self.file.readline()
        line = self.file.readline()
        liner = (line.split())
        counter = 1
        while int(liner[0]) < number_of_initial_waters + 1 and counter < number_of_initial_waters + 1:
            water_num = int(liner[0])
            temp = float(liner[1])
            pressure = float(liner[2])
            line = self.file.readline()
            line = self.file.readline()
            all_comp = []
            while line.startswith("'*") is False:
                liner = (line.split())
                specie = self.find_primary_aqueous(primary_aqueous, liner[0])
                all_comp.append(WaterComp(specie, int(liner[1]), float(liner[2]), float(liner[3]), liner[4], float(liner[5])))
                line = self.file.readline()
            line = self.file.readline()
            line = self.file.readline()
            liner = (line.split())
            water_composition = [Water(all_comp, temp, pressure)]
            # grid.zonelist[water_num -1].water = water_composition
            initial_waters_mapping[water_num] = water_composition
            initial_waters_list.append(water_composition)
            if liner[0].isnumeric() is False:
                break
            counter = counter + 1
        counter = 1
        if liner[0].isnumeric() is False:
            return initial_waters_list, boundary_waters_list, initial_waters_mapping, boundary_waters_mapping
        while int(liner[0]) < number_of_boundary_waters + 1 and counter < number_of_boundary_waters + 1:
            water_num = int(liner[0])
            temp = float(liner[1])
            pressure = float(liner[2])
            line = self.file.readline()
            line = self.file.readline()
            all_comp = []
            while line.startswith("'*") is False:
                liner = (line.split())
                specie = self.find_primary_aqueous(primary_aqueous, liner[0])
                all_comp.append(WaterComp(specie, int(liner[1]), float(liner[2]), float(liner[3]), liner[4], float(liner[5])))
                line = self.file.readline()
            line = self.file.readline()
            line = self.file.readline()
            liner = (line.split())
            water_composition = [Water(all_comp, temp, pressure)]
            # grid.zonelist[water_num -1].water = water_composition
            boundary_waters_mapping[water_num] = water_composition
            boundary_waters_list.append(water_composition)
            counter = counter + 1
            if liner[0].isnumeric() is False:
                break

        return initial_waters_list, boundary_waters_list, initial_waters_mapping, boundary_waters_mapping

    def find_minerals(self, minerals, name):
        startIndex = name.find('\'')
        if startIndex >= 0:
            name = name.replace("'", "")
        for i in range(len(minerals)):
            if name.lower() == minerals[i].name.strip().lower():
                return minerals[i]

    def get_param_values_mineral_zones(self, minerals):
        initial_minerals_mapping = {}
        initial_minerals_list = []
        line = self.file.readline()
        liner = (line.split())
        number_of_mineral_zones = int(liner[0])
        line = self.file.readline()
        liner = (line.split())
        counter = 1
        while int(liner[0]) < number_of_mineral_zones + 1 and counter < number_of_mineral_zones + 1:
            mineral_num = int(liner[0])
            line = self.file.readline()
            line = self.file.readline()
            all_comp = []
            while line.startswith("'*") is False:
                liner = (line.split())
                initial_mineral_value = liner
                mineral_found = self.find_minerals(minerals, liner[0])
                line = self.file.readline()
                liner = (line.split())
                initial_mineral_value = initial_mineral_value + liner
                spec_mineral = MineralComp(mineral_found, float(initial_mineral_value[1]), int(initial_mineral_value[2]), float(initial_mineral_value[3]), float(initial_mineral_value[4]), int(initial_mineral_value[5]))
                all_comp.append(spec_mineral)
                line = self.file.readline()
            line = self.file.readline()
            liner = (line.split())
            # grid.zonelist[mineral_num -1].mineral_zone = MineralZone(all_comp)
            initial_minerals_mapping[mineral_num] = MineralZone(all_comp)
            initial_minerals_list.append(MineralZone(all_comp))
            counter = counter + 1
            if len(liner) == 0:
                break

        return initial_minerals_list, initial_minerals_mapping

    def find_gas(self, gases, name):
        startIndex = name.find('\'')
        if startIndex >= 0:
            name = name.replace("'", "")
        for i in range(len(gases)):
            if name.lower() == gases[i].name.strip().lower():
                return gases[i]

    def get_param_values_ij_gases(self, gases):
        initial_gas_mapping = {}
        initial_gas_list = []
        injection_gas_mapping = {}
        injection_gas_list = []
        line = self.file.readline()
        liner = (line.split())
        number_of_initial_gas = int(liner[0])
        if len(liner) > 1:
            number_of_injection_gas = int(liner[1])
        line = self.file.readline()
        liner = (line.split())
        counter = 1
        while int(liner[0]) < number_of_initial_gas + 1 and counter < number_of_initial_gas + 1:
            gas_num = int(liner[0])
            line = self.file.readline()
            line = self.file.readline()
            all_comp = []
            while line.startswith("'*") is False:
                liner = (line.split())
                spec_gas = copy.deepcopy(self.find_gas(gases, liner[0]))
                spec_gas.partial_pressure = float(liner[1])
                all_comp.append(spec_gas)
                line = self.file.readline()
            line = self.file.readline()
            liner = (line.split())
            # grid.zonelist[gas_num -1].gas = spec_gas
            initial_gas_mapping[gas_num] = spec_gas
            initial_gas_list.append([spec_gas])
            if len(liner) == 0:
                break
            counter = counter + 1
        counter = 1
        if len(liner) == 0:
            return initial_gas_list, injection_gas_list, initial_gas_mapping, injection_gas_mapping
        while int(liner[0]) < number_of_injection_gas + 1 and counter < number_of_injection_gas + 1:
            gas_num = int(liner[0])
            line = self.file.readline()
            line = self.file.readline()
            all_comp = []
            while line.startswith("'*") is False:
                liner = (line.split())
                spec_gas2 = copy.deepcopy(self.find_gas(gases, liner[0]))
                spec_gas2.partial_pressure = float(liner[1])
                all_comp.append(spec_gas2)
                line = self.file.readline()
            line = self.file.readline()
            liner = (line.split())
            # grid.zonelist[gas_num -1].gas = spec_gas
            injection_gas_mapping[gas_num] = spec_gas2
            injection_gas_list.append([spec_gas2])
            counter = counter + 1
            if len(liner) == 0:
                break

        return initial_gas_list, injection_gas_list, initial_gas_mapping, injection_gas_mapping

    def get_param_values_perm_poro(self, minerals, grid):
        initial_perm_poro_mapping = {}
        initial_perm_poro_list = []
        line = self.file.readline()
        liner = (line.split())
        number_of_perm_poro_zones = int(liner[0])
        line = self.file.readline()
        liner = (line.split())
        counter = 1
        while int(liner[0]) < number_of_perm_poro_zones + 1 and counter < number_of_perm_poro_zones + 1:
            perm_poro_num = int(liner[0])
            line = self.file.readline()
            line = self.file.readline()
            all_comp = []
            while line.startswith("'*") is False:
                liner = (line.split())
                initial_perm_poro_value = liner
                liner = (line.split())
                spec_perm_poro = PermPoro(initial_perm_poro_value[0], initial_perm_poro_value[1], initial_perm_poro_value[2])
                spec_perm_poro_zone = PermPoroZone([spec_perm_poro])
                all_comp.append(spec_perm_poro_zone)
                initial_perm_poro_mapping[perm_poro_num] = PermPoroZone(all_comp)
                initial_perm_poro_list.append(PermPoroZone(all_comp))
                line = self.file.readline()
            line = self.file.readline()
            liner = (line.split())
            # grid.zonelist[perm_poro_num -1].permporo = all_comp
            counter = counter + 1
            if len(liner) == 0:
                break

        return initial_perm_poro_list, initial_perm_poro_mapping

    def write_values(self, vals, linetype):
        """Inverse of read_values()."""
        line = self.write_values_to_string(vals, linetype)
        self.write('%s\n' % line)

    def read_value_line(self, variable, linetype):
        """Reads a line of parameter values from the file into a dictionary variable.
        Null values are ignored."""
        spec = self.specification[linetype]
        vals = self.read_values(linetype)
        if len(spec[0]) < 2:
            for var, val in zip(spec[0], vals):
                if val is not None:
                    variable[var] = val
        else:
            variable[linetype] = vals

    def read_params_value_line(self, variable, linetype):
        spec = self.specification[linetype]
        vals = self.read_values(linetype)
        if len(spec[0]) > 2:
            for var, val in zip(spec[0], vals):
                if val is not None:
                    variable[var] = val
        else:
            variable[linetype] = vals

    def read_multi_value_line(self, variable, linetype):
        """Reads a line of parameter multi values from the file into a dictionary variable.
        Null values are ignored."""
        spec = self.specification[linetype]
        vals = self.read_values(linetype)
        if len(spec[0]) < 6:
            for var, val in zip(spec[0], vals):
                if val is not None:
                    variable[var] = val
        else:
            variable[linetype] = vals

    def read_multi_value_line2(self, variable, linetype):
        """Reads a line of parameter values from the file into a dictionary variable.
        Null values are ignored."""
        spec = self.specification[linetype]
        vals = self.read_values(linetype)
        if len(spec[0]) > 6:
            for var, val in zip(spec[0], vals):
                if val is not None:
                    variable[var] = val
        else:
            variable[linetype] = vals

    def write_value_line(self, variable, linetype):
        """Inverse of read_value_line()."""
        spec = self.specification[linetype]
        vals = []
        for name in spec[0]:
            if name in variable:
                val = variable[name]
            else:
                val = None
            vals.append(val)
        self.write_values(vals, linetype)
