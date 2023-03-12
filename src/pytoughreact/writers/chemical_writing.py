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

import os
import sys
from t2data import t2data
from fixed_format_file import default_read_function, fixed_format_file
from pytoughreact.constants.format_specifications import t2chemical_format_specification
from pytoughreact.constants.sections import t2chemical_sections
from pytoughreact.chemical.chemical_composition import PrimarySpecies


class SynergyChemical(fixed_format_file):
    """Class for parsing CHEMICAL.INP data file."""

    def __init__(self, filename, mode, read_function=default_read_function):
        super(SynergyChemical, self).__init__(filename, mode,
                                              t2chemical_format_specification, read_function)


class t2chemical(t2data):
    """
        Main class for structuring the writing , reading  of chemical parameters
    """
    def __init__(self, filename='', meshfilename='', t2reactgrid=None, path=None, read_function=default_read_function):
        self.t2grid = t2reactgrid
        self._sections = []
        self.title = ''
        self.primary_aqueous = []
        self.aqueous_kinetics = [-1]
        self.aqueous_complexes = [-1]
        self.minerals = []
        self.surface_complexes = [-1]
        self.decay_species = [-1]
        self.exchangeable_cations = [-1]
        # self.gases = self.ij_gas
        self.surface_adsorption = [-1]
        self.linear_equilibrium = [-1]
        self.cation_exchange = [-1]
        # self.waters = self.ib_waters
        self.end_keyword = '#end'
        self.read_function = read_function
        self.ib_waters = self.getib_waters()
        self.waters = self.ib_waters
        self.ij_gas = self.getij_gas()
        self.gases = self.ij_gas
        super().__init__(filename, meshfilename, read_function)

    def getib_waters(self):
        """ Get initial and boundary waters """
        ib_waters = [[], []]
        if self.t2grid.zonelist[0].gas is None:
            return ib_waters
        for zone in self.t2grid.zonelist:
            if zone.water[0]:
                if zone.water[0] not in ib_waters[0]:
                    ib_waters[0].append((zone.water[0]))
            if zone.water[1]:
                if zone.water[1] not in ib_waters[1]:
                    ib_waters[1].append((zone.water[1]))
        return ib_waters

    # ib_waters = property(getib_waters)

    def getij_gas(self):
        """ Get initial and injection gas """
        ij_gas = [[], []]
        if self.t2grid.zonelist[0].gas is None:
            return ij_gas
        try:
            for zone in self.t2grid.zonelist:
                if zone.gas[0]:
                    if zone.gas[0] not in ij_gas[0]:
                        ij_gas[0].append((zone.gas[0]))
                if zone.gas[1]:
                    if zone.gas[1] not in ij_gas[1]:
                        ij_gas[1].append((zone.gas[1]))
        except AttributeError:
            pass
        return ij_gas

    # ij_gas = property(getij_gas)

    def get_mineral_zones(self):
        """ Get Mineral zones"""
        mineral_zone = []
        for zone in self.t2grid.zonelist:
            mineral_zone.append(zone.mineral_zone)
        if len(mineral_zone) != len(set(mineral_zone)):
            mineral_zone = list(set(mineral_zone))
        return mineral_zone

    mineral_zones = property(get_mineral_zones)

    def get_perm_poro_zones(self):
        """ Get Porosity / Permeability zones"""
        perm_poro_zone = []
        for zone in self.t2grid.zonelist:
            perm_poro_zone.append(zone.permporo)
        return perm_poro_zone

    perm_poro = property(get_perm_poro_zones)

    def map_mineral_to_zone(self):
        """ Map Mineral to Zone"""
        zoning = {}
        index = 1
        for zone in self.t2grid.zonelist:
            zoning[index] = zone.mineral
            index = index + 1
        return zoning

    def update_read_write_functions(self):
        """Updates functions for reading and writing sections of data file."""

        self.read_fn = dict(zip(
            t2chemical_sections,
            [self.read_title,
             self.read_primary_aqueous,
             self.read_aqueous_kinetics,
             self.read_aqueous_complexes,
             self.read_minerals,
             self.read_gases,
             self.read_surface_complexes,
             self.read_decay_species,
             self.read_exchangeable_cations,
             self.read_ib_waters,
             self.read_mineral_zones,
             self.read_ij_gas,
             self.read_perm_poro,
             self.read_surface_adsorption,
             self.read_linear_equilibrium,
             self.read_cation_exchange]))

        self.write_fn = dict(zip(
            t2chemical_sections,
            [self.write_title,
             self.write_primary_aqueous,
             self.write_aqueous_kinetics,
             self.write_aqueous_complexes,
             self.write_minerals,
             self.write_gases,
             self.write_surface_complexes,
             self.write_decay_species,
             self.write_exchangeable_cations,
             self.write_ib_waters,
             self.write_mineral_zones,
             self.write_ij_gas,
             self.write_perm_poro,
             self.write_surface_adsorption,
             self.write_linear_equilibrium,
             self.write_cation_exchange]))

    def get_present_sections(self):
        """Returns a list of TOUGH2 section keywords for which there are
        corresponding data in the t2bio object."""
        data_present = dict(zip(
            t2chemical_sections,
            [self.title,
             self.primary_aqueous,
             self.aqueous_kinetics,
             self.aqueous_complexes,
             self.minerals,
             self.gases,
             self.surface_complexes,
             self.decay_species,
             self.exchangeable_cations,
             self.ib_waters,
             self.mineral_zones,
             self.ij_gas,
             self.perm_poro,
             self.surface_adsorption,
             self.linear_equilibrium,
             self.cation_exchange]))
        return [keyword for keyword in t2chemical_sections if data_present[keyword]]

    present_sections = property(get_present_sections)

    def section_insertion_index(self, section):
        """Determines an appropriate position to insert the specified section
        in the internal list of data file sections.
        """
        try:
            listindex = t2chemical_sections.index(section)
            if listindex == 0:
                return 0  # SIMUL section
            else:
                # first look for sections above the one specified,
                # and put new one just after the last found:
                for i in reversed(range(listindex)):
                    try:
                        section_index = self._sections.index(t2chemical_sections[i])
                        return section_index + 1
                    except ValueError:
                        pass
                # look for sections below the one specified,
                # and put new one just before the first found:
                for i in range(listindex, len(t2chemical_sections)):
                    try:
                        section_index = self._sections.index(t2chemical_sections[i])
                        return section_index
                    except ValueError:
                        pass
                return len(self._sections)
        except ValueError:
            return len(self._sections)

    def write_title(self, outfile):
        """ Write Title od Chemical file (chemical.inp)"""
        outfile.write('#Title' + '\n')
        outfile.write(self.title.strip() + '\n')

    def read_primary_aqueous(self, infile):
        """ Read Primary Aqueous Species """
        params = infile.get_param_values('primary_aqueous')
        all_species = []
        for parameter in params:
            all_species.append(PrimarySpecies(parameter[0], parameter[1]))
        self.__dict__['primary_aqueous'] = all_species

    def write_primary_aqueous(self, outfile):
        """ Write Primary Aqueous Species """
        outfile.write('#----------------------------------------------------------------------------\n')
        outfile.write('#DEFINITION OF THE GEOCHEMICAL SYSTEM\n')
        outfile.write('#PRIMARY AQUEOUS SPECIES\n')
        for specie in self.primary_aqueous:
            vals = specie.getNameTrans()
            outfile.write_values(vals, 'primary_aqueous')
        outfile.write("'*'\n")

    def read_aqueous_kinetics(self, infile):
        """ Read Aqueous Kinetic Species """
        params = infile.get_param_values('aqueous_kinetics')
        if len(params) == 0:
            self.__dict__['aqueous_kinetics'] = [-1]
        else:
            self.__dict__['aqueous_kinetics'] = params

    def write_aqueous_kinetics(self, outfile):
        """ Write Aqueous Kinetic Species """
        if self.aqueous_kinetics[0] == -1:
            outfile.write('# AQUEOUS KINETICS\n')
            outfile.write("'*'\n")
        pass

    def read_aqueous_complexes(self, infile):
        """ Read Aqueous Complexes """
        params = infile.get_param_values('aqueous_complex')
        if len(params) == 0:
            self.__dict__['aqueous_complexes'] = [-1]
        else:
            self.__dict__['aqueous_complexes'] = params

    def write_aqueous_complexes(self, outfile):
        """ Write Aqueous Complexes """
        if self.aqueous_complexes[0] == -1:
            outfile.write('# AQUEOUS COMPLEXES\n')
            outfile.write("'*'\n")

    def read_minerals(self, infile):
        """ Read Minerals """
        params = infile.get_param_values_mineral()
        if len(params) == 0:
            self.__dict__['minerals'] = [-1]
        else:
            self.__dict__['minerals'] = params

    def write_dissolution_precipitation(self, outfile, mineral, format):
        """ Write Dissolution and Precipitation Parameters """
        if format.lower() == 'dissolution':
            try:
                vals = mineral.getDissolutionParams()
            except Exception:
                raise ValueError("Dissolution parameters are not given")
        elif format.lower() == 'precipitation':
            try:
                vals = mineral.getPrecipitationParams()
                vals2 = mineral.getPrecipitationParams2()
            except Exception:
                raise ValueError("Precipitation parameters are not given")
        outfile.write_values(vals, 'minerals1.1')
        if vals[1] == 1:
            try:
                vals = mineral.getpHDependency1()
            except Exception:
                raise ValueError("The dependency on pH has to be provided. See manual for more")
            outfile.write_values(vals, 'minerals1.1.1')
        elif vals[1] == 2:
            vals1 = mineral.getNumberOfpHDependence()
            outfile.write_values(vals1, 'minerals1.1.2a')
            for ph in mineral.dissolution[0].pHDependence:
                try:
                    vals = mineral.getpHDependency2(ph)
                except Exception:
                    raise ValueError("The dependency on pH has to be provided. See manual for more")
                outfile.write_values(vals, 'minerals1.1.2')
        if format.lower() == 'precipitation':
            outfile.write_values(vals2, 'minerals1.1.1a')

    def write_equilibrium(self, outfile, mineral):
        """ Write Equilibirum Parameters """
        vals = mineral.getEquilibriumData()
        outfile.write_values(vals, 'minerals1.1.1a')

    def write_minerals(self, outfile):
        """ Write Minerals to file """
        outfile.write('#MINERALS\n')
        for mineral in self.minerals:
            vals = mineral.getFirstRow()
            outfile.write_values(vals, 'minerals')
            if vals[1] == 1 and (vals[2] == 1 or vals[2] == 3):
                self.write_dissolution_precipitation(outfile, mineral, 'dissolution')
            if vals[1] == 1 and (vals[2] == 2 or vals[2] == 3):
                self.write_dissolution_precipitation(outfile, mineral, 'precipitation')
            if vals[1] == 0:
                self.write_equilibrium(outfile, mineral)
        outfile.write("'*'\n")

    def read_gases(self, infile):
        """ Read gases from file """
        params = infile.get_param_values_gas()
        if len(params) == 0:
            # self.__dict__['gas_init'] = [-1]
            self.__dict__['gases'] = [-1]
        else:
            # self.__dict__['gas_init'] = params
            self.__dict__['gases'] = params

    def write_gases(self, outfile):
        """ Write gases to file """
        outfile.write('# GASES\n')
        gas_name = []
        try:
            for gas in self.ij_gas[0][0]:
                if gas.name not in gas_name:
                    vals = [gas.name, gas.fugacity_flag]
                outfile.write_values(vals, 'gases')
                gas_name.append(gas.name)
            outfile.write("'*'\n")
        except Exception:
            for gas in self.ij_gas[0]:
                if gas.name not in gas_name:
                    vals = [gas.name, gas.fugacity_flag]
                outfile.write_values(vals, 'gases')
                gas_name.append(gas.name)
            outfile.write("'*'\n")

    def read_surface_complexes(self, infile):
        """ Read surface complexes from file """
        params = infile.get_param_values_surface_complex()
        if len(params) == 0:
            self.__dict__['surface_complexes'] = [-1]
        else:
            self.__dict__['surface_complexes'] = params

    def write_surface_complexes(self, outfile):
        """ Write surface complexes to file """
        if self.surface_complexes[0] == -1:
            outfile.write('# SURFACE COMPLEXES\n')
            outfile.write("'*'\n")

    def read_decay_species(self, infile):
        """ Read decay species from file """
        params = infile.get_param_values_decay_species()
        if len(params) == 0:
            self.__dict__['decay_species'] = [-1]
        else:
            self.__dict__['decay_species'] = params

    def write_decay_species(self, outfile):
        """ Write decay species to file """
        if self.decay_species[0] == -1:
            outfile.write('# SPECIES WITH Kd AND DECAY\n')
            outfile.write("'*'\n")

    def read_exchangeable_cations(self, infile):
        """ Read Exchangeable Cations from file """
        params = infile.get_param_values_exchangeable_cations()
        if len(params) == 0:
            self.__dict__['exchangeable_cations'] = [-1]
        else:
            self.__dict__['exchangeable_cations'] = params

    def write_exchangeable_cations(self, outfile):
        """ Write Exchangeable Cations to file """
        if self.exchangeable_cations[0] == -1:
            outfile.write('# EXCHANGEABLE CATIONS\n')
            outfile.write("'*'\n")
        pass

    def read_ib_waters(self, infile):
        """ Read Initial and Boundary waters from file """
        initial_waters_list, boundary_waters_list, initial_waters_mapping, boundary_waters_mapping = infile.get_param_values_ib_waters(
            self.primary_aqueous, self.t2grid)
        if len(initial_waters_list) == 0:
            self.__dict__['ib_waters'] = [-1]
        else:
            self.__dict__['waters'][0] = initial_waters_list
            if len(boundary_waters_list) > 0:
                self.__dict__['waters'][1] = boundary_waters_list
            self.initial_waters_mapping = initial_waters_mapping
            if len(list(boundary_waters_mapping.keys())) > 0:
                self.boundary_waters_mapping = boundary_waters_mapping

    def getInitialWaterRow(self, water):
        pass
        # print(water[0]['initial'])

    def getInitialWatersTemperature(self, all_waters):
        pass
        # print(all_waters[0]['initial'])

    def getInitialWatersPressure(self, all_waters):
        pass
        # print(all_waters[0]['initial'])

    def getBoundaryWaters(self, all_waters):
        pass
        # for i in range(len(all_waters)):
        #     print(all_waters[0][0]['boundary'])

    def write_ib_waters(self, outfile):
        """ Write Initial and Boundary waters to file """
        outfile.write('#----------------------------------------------------------------------------\n')
        outfile.write('# # INITIAL AND BOUNDARY WATER TYPES\n')
        initial_waters = self.ib_waters[0]
        vals = [len(self.ib_waters[0]), len(self.ib_waters[1])]
        outfile.write_values(vals, 'water_comp')
        try:
            for i in range(len(initial_waters)):
                outfile.write('# Index  Speciation T(C)  P(bar)  \n')
                vals = [i + 1, initial_waters[i][0].temperature, initial_waters[i][0].pressure]
                outfile.write_values(vals, 'water_comp1')
                species = initial_waters[i][0].primary_species
                outfile.write('#        icon       NRguess(molal)  ctot (molal)   \n')
                for specie in species:
                    vals = [specie.primary_species.NAME.strip(), specie.icon, specie.nrguess, specie.ctot, specie.nameq,
                            specie.qksat]
                    outfile.write_values(vals, 'water_comp2')
                outfile.write("'*'\n")
        except Exception:
            for i in range(len(initial_waters)):
                outfile.write('# Index  Speciation T(C)  P(bar)  \n')
                vals = [i + 1, initial_waters[i].temperature, initial_waters[i].pressure]
                outfile.write_values(vals, 'water_comp1')
                species = initial_waters[i].primary_species
                outfile.write('#        icon       NRguess(molal)  ctot (molal)   \n')
                for specie in species:
                    vals = [specie.primary_species.NAME.strip(), specie.icon, specie.nrguess, specie.ctot, specie.nameq,
                            specie.qksat]
                    outfile.write_values(vals, 'water_comp2')
                outfile.write("'*'\n")

        boundary_water = self.ib_waters[1]
        if boundary_water:
            try:
                for i in range(len(boundary_water)):
                    outfile.write('# Index  Speciation T(C)  P(bar)  \n')
                    vals = [i + 1, boundary_water[i][0].temperature, boundary_water[i][0].pressure]
                    outfile.write_values(vals, 'water_comp1')
                    species = boundary_water[i][0].primary_species
                    outfile.write('#        icon       NRguess(molal)  ctot (molal)   \n')
                    for specie in species:
                        vals = [specie.primary_species.NAME.strip(), specie.icon, specie.nrguess, specie.ctot, specie.nameq,
                                specie.qksat]
                        outfile.write_values(vals, 'water_comp2')
                    outfile.write("'*'\n")
            except Exception:
                for i in range(len(boundary_water)):
                    outfile.write('# Index  Speciation T(C)  P(bar)  \n')
                    vals = [i + 1, boundary_water[i].temperature, boundary_water[i].pressure]
                    outfile.write_values(vals, 'water_comp1')
                    species = boundary_water[i].primary_species
                    outfile.write('#        icon       NRguess(molal)  ctot (molal)   \n')
                    for specie in species:
                        vals = [specie.primary_species.NAME.strip(), specie.icon, specie.nrguess, specie.ctot, specie.nameq,
                                specie.qksat]
                        outfile.write_values(vals, 'water_comp2')
                    outfile.write("'*'\n")

    def getInitialWaterIndex(self):
        """ Get Initial Water Index """
        water_index = {}
        initial_waters = self.ib_waters[0]
        for i in range(len(initial_waters)):
            water_index[initial_waters[i][0]] = i + 1

        return water_index

    initial_water_index = property(getInitialWaterIndex)

    def getBoundaryWaterIndex(self):
        """ Get Boundary Water Index """
        water_index = {}
        boundary_water = self.ib_waters[1]
        for i in range(len(boundary_water)):
            water_index[boundary_water[i][0]] = i + 1

        return water_index

    boundary_water_index = property(getBoundaryWaterIndex)

    def getMineralIndex(self):
        """ Get Mineral Index """
        mineral_index = {}
        all_mineral = self.mineral_zones
        if len(all_mineral) != len(set(all_mineral)):
            all_mineral = list(set(all_mineral))
        for i in range(len(all_mineral)):
            mineral_index[all_mineral[i]] = i + 1
        return mineral_index

    mineral_index = property(getMineralIndex)

    def getInitialGasIndex(self):
        """ Get Initial Gas Index """
        gas_index = {}
        initial_gas = self.ij_gas[0]
        for i in range(len(initial_gas)):
            gas_index[initial_gas[i][0]] = i + 1
        return gas_index

    initial_gas_index = property(getInitialGasIndex)

    def getInjectionGasIndex(self):
        """ Get Injection Gas Index """
        gas_index = {}
        initial_gas = self.ij_gas[1]
        for i in range(len(initial_gas)):
            gas_index[initial_gas[i][0]] = i + 1
        return gas_index

    injection_gas_index = property(getInjectionGasIndex)

    def getPermPoroIndex(self):
        """ Get Permeability Porosity Index"""
        perm_poro_index = {}
        perm_poro = self.perm_poro
        perm_poro_all = []
        for i in range(len(perm_poro)):
            if perm_poro[i] not in perm_poro_all:
                perm_poro_index[perm_poro[i]] = i + 1
                perm_poro_all.append(perm_poro[i])
        return perm_poro_index

    perm_poro_index = property(getPermPoroIndex)

    def read_mineral_zones(self, infile):
        " Read Mineral Zones "
        initial_minerals_list, initial_minerals_mapping = infile.get_param_values_mineral_zones(
            self.minerals)
        if len(initial_minerals_list) == 0:
            self.__dict__['mineral_zones'] = [-1]
        else:
            self.__dict__['mineral_zones'] = initial_minerals_list
            self.initial_minerals_mapping = initial_minerals_mapping

    def countZones(self):
        " Count number of zones"
        count = len(self.mineral_zones)
        return count

    def countMineralZones(self):
        " Count number of mineral zones"
        return len(set(self.mineral_zones))

    def write_mineral_zones(self, outfile):
        " Write mineral zones"
        outfile.write('#----------------------------------------------------------------------------\n')
        outfile.write('# INITIAL MINERAL ZONES\n')
        vals = [len(self.mineral_zones)]
        # masa = self.countMineralZones()
        outfile.write_values(vals, 'mineral_zone')
        index = 1
        for zone in self.mineral_zones:
            indexer = [index]
            outfile.write_values(indexer, 'mineral_zone1')
            outfile.write('# mineral         vol.frac\n')
            for mineralcomp in zone.minerals:
                vals = [mineralcomp.mineral.name, mineralcomp.init_volume_fraction, mineralcomp.reaction_type]
                outfile.write_values(vals, 'mineral_zone2')
                if mineralcomp.radius is not None and mineralcomp.reactive_surface_area is not None and mineralcomp.unit is not None:
                    vals = [mineralcomp.radius, mineralcomp.reactive_surface_area, mineralcomp.unit]
                    outfile.write_values(vals, 'mineral_zone2.1')
            index += 1
            outfile.write("'*'\n")

    def read_ij_gas(self, infile):
        """ Read Initial and Injection Gas"""
        initial_gas_list, injection_gas_list, initial_gas_mapping, injection_gas_mapping = infile.get_param_values_ij_gases(
            self.gases)
        if len(initial_gas_list) == 0:
            self.__dict__['ij_gas'] = [[], []]
        else:
            self.__dict__['ij_gas'][0] = initial_gas_list
            self.initial_gas_mapping = initial_gas_mapping
            if len(injection_gas_list) > 0:
                self.__dict__['ij_gas'][1] = injection_gas_list
            if len(list(injection_gas_mapping.keys())) > 0:
                self.injection_gas_mapping = injection_gas_mapping

    def write_ij_gas(self, outfile):
        """ Write Initial and Injection Gas"""
        outfile.write('#----------------------------------------------------------------------------\n')
        outfile.write('# INITIAL and Injection gas ZONES \n')
        initial_gas = self.ij_gas[0]
        vals = [len(self.ij_gas[0]), len(self.ij_gas[1])]
        outfile.write_values(vals, 'gas_zone')
        try:
            for i in range(len(initial_gas)):
                vals = [i + 1]
                outfile.write_values(vals, 'gas_zone1')
                outfile.write('#gas      partial pressure (bar) !if zero or blank, equil with solution   \n')
                vals = [initial_gas[i][0].name, initial_gas[i][0].partial_pressure]
                outfile.write_values(vals, 'gas_zone2')
            outfile.write("'*'\n")
        except Exception:
            for i in range(len(initial_gas)):
                vals = [i + 1]
                outfile.write_values(vals, 'gas_zone1')
                outfile.write('#gas      partial pressure (bar) !if zero or blank, equil with solution   \n')
                vals = [initial_gas[i].name, initial_gas[i].partial_pressure]
                outfile.write_values(vals, 'gas_zone2')
            outfile.write("'*'\n")
        boundary_gas = self.ij_gas[1]
        if boundary_gas:
            try:
                for i in range(len(boundary_gas)):
                    vals = [i + 1]
                    outfile.write_values(vals, 'gas_zone1')
                    outfile.write('#gas      partial pressure (bar) !if zero or blank, equil with solution   \n')
                    vals = [boundary_gas[i][0].name, boundary_gas[i][0].partial_pressure]
                    outfile.write_values(vals, 'gas_zone2')
                outfile.write("'*'\n")
            except Exception:
                for i in range(len(boundary_gas)):
                    vals = [i + 1]
                    outfile.write_values(vals, 'gas_zone1')
                    outfile.write('#gas      partial pressure (bar) !if zero or blank, equil with solution   \n')
                    vals = [boundary_gas[i].name, boundary_gas[i].partial_pressure]
                    outfile.write_values(vals, 'gas_zone2')
                outfile.write("'*'\n")

    def read_perm_poro(self, infile):
        """ Read Peremability and Porosity Regions"""
        initial_perm_poro_list, initial_perm_poro_mapping = infile.get_param_values_perm_poro(
            self.minerals, self.t2grid)
        if len(initial_perm_poro_list) == 0:
            self.__dict__['perm_poro'] = [-1]
        else:
            self.__dict__['perm_poro'] = initial_perm_poro_list
            self.initial_perm_poro_mapping = initial_perm_poro_mapping

    def write_perm_poro(self, outfile):
        """ Write Peremability and Porosity Regions"""
        outfile.write('#----------------------------------------------------------------------------\n')
        outfile.write('# Permeability-Porosity Zones\n')
        all_perm_zones = []
        for i in range(len(self.perm_poro)):
            try:
                all_perm_zones.append(self.perm_poro[i].permporo[0])
            except Exception:
                pass
        outfile.write(str(len(set(all_perm_zones))) + '\n')
        total_perm_poro = []
        try:
            for i in range(len(self.perm_poro)):
                if self.perm_poro[i].permporo[0] not in total_perm_poro:
                    vals = [self.perm_poro[i].permporo[0].law_type, self.perm_poro[i].permporo[0].a_param,
                            self.perm_poro[i].permporo[0].b_param]
                    outfile.write(str(i + 1) + '\n')
                    outfile.write('# Perm law  a-parameter  b-parameter\n')
                    total_perm_poro.append(self.perm_poro[i].permporo[0])
                    outfile.write_values(vals, 'perm_poro_zone')
                    outfile.write("'*'\n")
        except Exception:
            for i in range(len(all_perm_zones)):
                if all_perm_zones[i].permporo[0] not in total_perm_poro:
                    outfile.write(str(i + 1) + '\n')
                    outfile.write('# Perm law  a-parameter  b-parameter\n')
                    vals = [int(all_perm_zones[i].permporo[0].law_type), float(all_perm_zones[i].permporo[0].a_param),
                            float(all_perm_zones[i].permporo[0].b_param)]
                    total_perm_poro.append(all_perm_zones[i].permporo[0])
                    outfile.write_values(vals, 'perm_poro_zone')
                    outfile.write("'*'\n")

    def read_surface_adsorption(self, infile):
        """ Read Surface adsorption """
        pass

    def write_surface_adsorption(self, outfile):
        """ Write Surface adsorption """
        if self.surface_adsorption[0] == -1:
            outfile.write('# INITIAL SURFACE ADSORPTION ZONES\n')
            outfile.write("'*'\n")

    def read_linear_equilibrium(self, infile):
        """ Read Linear Equilibrium """
        pass

    def write_linear_equilibrium(self, outfile):
        """ Write Linear Equilibrium """
        if self.linear_equilibrium[0] == -1:
            outfile.write('# INITIAL LINEAR EQUILIBRIUM Kd ZONE\n')
            outfile.write("'*'\n")

    def read_cation_exchange(self, infile):
        """ Read Cation Exchange """
        pass

    def write_cation_exchange(self, outfile):
        """ Write Cation Exchange """
        if self.cation_exchange[0] == -1:
            outfile.write('# INITIAL ZONES OF CATION EXCHANGE\n')
            outfile.write("'*'\n")
        pass

    def write(self, filename='', meshfilename='', runlocation='',
              extra_precision=None, echo_extra_precision=None):
        """ Write to file (chemical.inp)"""
        if runlocation:
            if not os.path.isdir(runlocation):
                os.mkdir(runlocation)
            os.chdir(runlocation)
        if filename == '':
            filename = 'chemical.inp'
        self.update_sections()
        self.update_read_write_functions()
        outfile = SynergyChemical(filename, 'w')
        for keyword in self._sections:
            self.write_fn[keyword](outfile)
            outfile.write('\n')
        outfile.write(self.end_keyword + '\n')
        outfile.close()

    def convert_to_t2chemical(self, keyword):
        """ Get corresponding t2chemical keywords """
        if 'primary' in keyword.lower() and 'aqueous' in keyword.lower():
            return 'PRIMARY_AQUEOUS'
        elif 'kinetics' in keyword.lower() and 'aqueous' in keyword.lower():
            return 'AQUEOUS_KINETICS'
        elif 'complexes' in keyword.lower() and 'aqueous' in keyword.lower():
            return 'AQUEOUS_COMPLEXES'
        elif 'minerals' in keyword.lower() and 'zone' not in keyword.lower():
            return 'MINERALS'
        elif 'gases' in keyword.lower() and 'initial' not in keyword.lower():
            return 'GASES'
        elif 'complexes' in keyword.lower() and 'surface' in keyword.lower():
            return 'SURFACE_COMPLEXES'
        elif 'decay' in keyword.lower() and 'species' in keyword.lower():
            return 'DECAY_SPECIES'
        elif 'exchangeable' in keyword.lower() and 'cation' in keyword.lower():
            return 'EXCHANGEABLE_CATIONS'
        elif 'initial' in keyword.lower() and 'water' in keyword.lower():
            return 'IB_WATERS'
        elif 'mineral' in keyword.lower() and 'zones' in keyword.lower():
            return 'MINERAL_ZONES'
        elif 'initial' in keyword.lower() and 'gas' in keyword.lower():
            return 'IJ_GAS'
        elif 'permeability' in keyword.lower() and 'zone' in keyword.lower():
            return 'PERM_PORO'
        elif 'adsorption' in keyword.lower() and 'surface' in keyword.lower():
            return 'SURFACE_ADSORPTION'
        elif 'linear' in keyword.lower() and 'equilibrium' in keyword.lower():
            return 'LINEAR_EQUILIBRIUM'
        elif 'cation' in keyword.lower() and 'zone' in keyword.lower():
            return 'CATION_EXCHANGE'
        else:
            return 'false'

    def read(self, filename='', meshfilename='', runlocation='', extra_precision=None, echo_extra_precision=None):
        """ Read from file """
        if runlocation:
            if not os.path.isdir(runlocation):
                os.mkdir(runlocation)
            os.chdir(runlocation)
        if filename:
            self.filename = filename
        mode = 'r' if sys.version_info > (3,) else 'rU'
        infile = SynergyChemical(self.filename, mode, read_function=self.read_function)
        self.read_title(infile)
        self._sections = []
        self.update_read_write_functions()
        more = True
        next_line = None
        # countline = 0
        while more:
            if next_line:
                line = next_line
            else:
                line = infile.readline()
            if line:
                # keyword = line[0: 5].strip()
                keyword = line[1:]
                check_presence = self.convert_to_t2chemical(keyword)
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
