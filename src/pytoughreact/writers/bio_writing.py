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
import os
import sys
from os.path import splitext, basename
from math import ceil
from os import devnull, remove
from subprocess import call
from copy import deepcopy
from t2grids import t2grid, rocktype
from t2data import t2data, trim_trailing_nones
from mulgrids import unfix_blockname, padstring
from fixed_format_file import fixed_format_file
from fixed_format_file import default_read_function
from pytoughreact.constants.format_specifications import t2bio_format_specification
from pytoughreact.constants.sections import t2bio_sections
from pytoughreact.constants.defaults_constants import DEFAULT_PARAMETERS
from pytoughreact.chemical.biomass_composition import BaseComponent, Gas, Water_Bio, Biomass
from pytoughreact.chemical.bio_process_description import Process, BIODG


class t2bio_parser(fixed_format_file):
    """Class for parsing TMVOC data file."""

    def __init__(self, filename, mode, read_function=default_read_function):
        super(t2bio_parser, self).__init__(filename, mode,
                                           t2bio_format_specification, read_function)


class t2bio(t2data):
    """Class for TMVOC data."""

    def __init__(self, filename='', meshfilename='',
                 read_function=default_read_function):
        super().__init__(filename='', meshfilename='', read_function=default_read_function)
        self.filename = filename
        self.meshfilename = meshfilename
        self.title = ''
        self.simulator = ''
        self.parameter = deepcopy(DEFAULT_PARAMETERS)
        self._more_option_str = '0' * 21,
        self.more_option = np.zeros(22, int)
        self.multi = {}
        self.start = False
        self.relative_permeability = {}
        self.capillarity = {}
        self.components = []
        self.gas = []
        self.biodg = []
        self.solids = []
        self.lineq = {}
        self.output_times = {}
        self.grid = t2grid()
        self.generatorlist = []
        self.generator = {}
        self.short_output = {}
        self.incon = {}
        self.solver = {}
        self.history_block = []
        self.history_connection = []
        self.history_generator = []
        self.indom = {}
        self.noversion = False
        self.diffusion = []
        self.selection = {}
        self.meshmaker = []
        self._sections = []
        self.end_keyword = 'ENDCY'
        self._extra_precision, self._echo_extra_precision = [], True
        self.update_read_write_functions()
        self.read_function = read_function
        if self.filename:
            self.read(filename, meshfilename)

    def set_echo_extra_precision(self, value):
        if value != self._echo_extra_precision:
            if value is False:  # remove previously echoed sections from section list
                for section in self._extra_precision:
                    self.delete_section(section)
            else:  # add sections previously not echoed to section list
                for section in self._extra_precision:
                    self.insert_section(section)
            self._echo_extra_precision = value
            self.update_read_write_functions()

    def update_read_write_functions(self):
        """Updates functions for reading and writing sections of data file."""

        self.read_fn = dict(zip(
            t2bio_sections,
            [self.read_simulator,
             self.read_rocktypes,
             self.read_multi,
             self.read_chem,
             self.read_gas,
             self.read_biodg,
             self.read_solids,
             self.read_parameters,
             self.read_more_options,
             self.read_start,
             self.read_noversion,
             self.read_rpcap,
             self.read_lineq,
             self.read_solver,
             self.read_times,
             self.read_selection,
             self.read_diffusion,
             self.read_blocks,
             self.read_connections,
             self.read_meshmaker,
             self.read_generators,
             self.read_short_output,
             self.read_history_blocks,
             self.read_history_connections,
             self.read_history_generators,
             self.read_incons,
             self.read_indom]))

        self.write_fn = dict(zip(
            t2bio_sections,
            [self.write_simulator,
             self.write_rocktypes,
             self.write_multi,
             self.write_chem,
             self.write_gas,
             self.write_biodg,
             self.write_solids,
             self.write_parameters,
             self.write_more_options,
             self.write_start,
             self.write_noversion,
             self.write_rpcap,
             self.write_lineq,
             self.write_solver,
             self.write_times,
             self.write_selection,
             self.write_diffusion,
             self.write_blocks,
             self.write_connections,
             self.write_meshmaker,
             self.write_generators,
             self.write_short_output,
             self.write_history_blocks,
             self.write_history_connections,
             self.write_history_generators,
             self.write_incons,
             self.write_indom]))

    def get_present_sections(self):
        """Returns a list of TOUGH2 section keywords for which there are
        corresponding data in the t2bio object."""
        data_present = dict(zip(
            t2bio_sections,
            [self.simulator,
             self.grid and self.grid.rocktypelist,
             self.multi,
             self.components,
             self.gas,
             self.biodg,
             self.solids,
             self.parameter,
             np.any(self.more_option),
             self.start,
             self.noversion,
             self.relative_permeability or self.capillarity,
             self.lineq,
             self.solver,
             self.output_times,
             self.selection,
             self.diffusion,
             self.grid,
             self.grid,
             self.meshmaker,
             self.generatorlist,
             self.short_output,
             self.history_block,
             self.history_connection,
             self.history_generator,
             self.incon,
             self.indom]))
        return [keyword for keyword in t2bio_sections if data_present[keyword]]

    present_sections = property(get_present_sections)

    def section_insertion_index(self, section):
        """Determines an appropriate position to insert the specified section
        in the internal list of data file sections.
        """
        try:
            listindex = t2bio_sections.index(section)
            if listindex == 0:
                return 0  # SIMUL section
            else:
                # first look for sections above the one specified,
                # and put new one just after the last found:
                for i in reversed(range(listindex)):
                    try:
                        section_index = self._sections.index(t2bio_sections[i])
                        return section_index + 1
                    except ValueError:
                        pass
                # look for sections below the one specified,
                # and put new one just before the first found:
                for i in range(listindex, len(t2bio_sections)):
                    try:
                        section_index = self._sections.index(t2bio_sections[i])
                        return section_index
                    except ValueError:
                        pass
                return len(self._sections)
        except ValueError:
            return len(self._sections)

    def run(self, save_filename='', incon_filename='', runlocation='', simulator='AUTOUGH2_2',
            silent=False, output_filename=''):
        """ Runs simulation using TMVOC """
        if runlocation:
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
            print(os.path.dirname(os.path.realpath(__file__)))
            # newPath = shutil.copy('tmvoc.exe', runlocation)
            os.chdir(runlocation)
        if self.filename:
            datbase, ext = splitext(self.filename)
            if (self.type == 'AUTOUGH2'):
                if save_filename == '':
                    save_filename = datbase + '.save'
                if incon_filename == '':
                    incon_filename = datbase + '.incon'
                savebase, ext = splitext(save_filename)
                inconbase, ext = splitext(incon_filename)
                runfilename = datbase + '_' + basename(simulator) + '.in'
                open(runfilename, 'w').write('\n'.join([savebase, inconbase, datbase]))
                infile = open(runfilename, 'r')
                cmd = [simulator]
                if silent:
                    outfile = open(devnull, 'w')
                else:
                    outfile = None
                # run AUTOUGH2:
                call(cmd, stdin=infile, stdout=outfile)
                infile.close()
                remove(runfilename)
            else:  # run TOUGH2 (need to specify simulator executable name)
                if runlocation:
                    os.chdir(runlocation)
                # if os.path.exists("GENER"): os.remove("GENER")
                # if os.path.exists("OUTPUT_ELEME.csv"): os.remove("OUTPUT_ELEME.csv")
                cmd = [simulator]
                infile = open(self.filename, 'r')
                if silent:
                    outfile = None
                else:
                    if output_filename == '':
                        datbase = 'iter'
                        outfilename = datbase + '.out'
                    else:
                        outfilename = output_filename
                    outfile = open(outfilename, 'w')
                call(cmd, stdin=infile, stdout=outfile)

    def read_rocktypes(self, infile):
        """Reads grid rock types"""
        self.grid.rocktypelist = []
        self.grid.rocktype = {}
        line = padstring(infile.readline())
        while line.strip():
            [name, nad, density, porosity,
             k1, k2, k3, conductivity, specific_heat] = infile.parse_string(line, 'rocks1')
            self.grid.add_rocktype(rocktype(name, nad,
                                            density, porosity,
                                            [k1, k2, k3],
                                            conductivity, specific_heat))
            if nad is None:
                nad = 0
            if nad >= 1:  # additional lines:
                infile.read_multi_value_line2(self.grid.rocktype[name].__dict__, 'rocks1.1')
                if nad >= 2:
                    vals = infile.read_values('rocks1.2')
                    self.grid.rocktype[name].relative_permeability['type'] = vals[0]
                    self.grid.rocktype[name].relative_permeability['parameters'] = vals[2: -1]
                    vals = infile.read_values('rocks1.3')
                    self.grid.rocktype[name].capillarity['type'] = vals[0]
                    self.grid.rocktype[name].capillarity['parameters'] = vals[2: -1]
            line = padstring(infile.readline())

    def read_chem(self, infile):
        """ Reads chemical components """
        params = infile.read_values('chemp')
        all_comp = []
        for i in range(int(params[0])):
            comp_name = infile.read_values('chemp1')
            first_line = infile.read_values('chemp1.1')
            second_line = infile.read_values('chemp1.2')
            third_line = infile.read_values('chemp1.3')
            fourth_line = infile.read_values('chemp1.4')
            fifth_line = infile.read_values('chemp1.5')
            sixth_line = infile.read_values('chemp1.6')
            seventh_line = infile.read_values('chemp1.7')
            comp = BaseComponent(name=comp_name[0], critTemp=first_line[0], critPres=first_line[1],
                                 critComp=first_line[2],
                                 acentricFactor=first_line[3], dipoleMoment=first_line[4],
                                 boilPoint=second_line[0], vapPressA=second_line[1], vapPressB=second_line[2],
                                 vapPressC=second_line[3], vapPressD=second_line[4],
                                 molWeight=third_line[0], heatCapConstantA=third_line[1],
                                 heatCapConstantB=third_line[2], heatCapConstantC=third_line[3],
                                 heatCapConstantD=third_line[4],
                                 liqDensity=fourth_line[0], refTempForDensity=fourth_line[1],
                                 refBinaryDif=fourth_line[2], refTempForDif=fourth_line[3], expChemDif=fourth_line[4],
                                 liqVisConstA=fifth_line[0], liqVisConstB=fifth_line[1], liqVisConstC=fifth_line[2],
                                 liqVisConstD=fifth_line[3], liqCritVol=fifth_line[4],
                                 liqChemSolA=sixth_line[0], liqChemSolB=sixth_line[1], liqChemSolC=sixth_line[2],
                                 liqChemSolD=sixth_line[3],
                                 carbonPartCoefficient=seventh_line[0], fracCarbon=seventh_line[1],
                                 decayConstant=seventh_line[2])
            all_comp.append(comp)
        self.components = all_comp

    def write_chem(self, outfile):
        """ Writes chemical components """
        outfile.write('CHEMP\n')
        vals = [len(self.components)]
        outfile.write_values(vals, 'chemp')
        for component in self.components:
            vals = component.name
            outfile.write(vals + '\n')
            vals = component.getFirstSet()
            outfile.write_values(vals, 'chemp1.1')
            vals = component.getSecondSet()
            outfile.write_values(vals, 'chemp1.2')
            vals = component.getThirdSet()
            outfile.write_values(vals, 'chemp1.3')
            vals = component.getFourthSet()
            outfile.write_values(vals, 'chemp1.4')
            vals = component.getFifthSet()
            outfile.write_values(vals, 'chemp1.5')
            vals = component.getSixthSet()
            outfile.write_values(vals, 'chemp1.6')
            vals = component.getSeventhSet()
            outfile.write_values(vals, 'chemp1.7')
        # outfile.write(str(comp_total) + '\n')
        pass

    def read_gas(self, infile):
        """ Reads Gases """
        params = infile.read_values('ncgas')
        all_comp = []
        for i in range(int(params[0])):
            first_line = infile.read_values('ncgas1')
            comp = Gas(name=first_line[0], index=i + 2)
            all_comp.append(comp)

        self.gas = all_comp

    def write_gas(self, outfile):
        """ Writes Gases """
        outfile.write('NCGAS\n')
        vals = [len(self.gas)]
        outfile.write_values(vals, 'ncgas')
        for i in range(len(self.gas)):
            vals = self.gas[i].name
            outfile.write(vals + '\n')

    def reset_bio_dicta(self, all_components):
        """ Resets the BIO dicitonary """
        dicta_all = []
        for i in range(len(all_components)):
            dicta = {}
            dicta[all_components[i]] = []
            dicta_all.append(dicta)
        return dicta_all

    def read_biodg(self, infile):
        """ Reads Biodegradation Block """
        params = infile.read_values('biodg')
        number_of_processes = int(infile.read_values('biodg1')[0])
        process_details = []
        for i in range(number_of_processes):
            first_line = infile.read_values('biodg1.1')
            second_line = infile.read_values('biodg1.1.1')
            third_line = infile.read_values('biodg1.1.2')
            fourth_line = infile.read_values('biodg1.1.3')
            fifth_line = infile.read_values('biodg1.1.4')
            sixth_line = infile.read_values('biodg1.1.5')
            comp = [first_line, second_line, third_line, fourth_line, fifth_line, sixth_line]
            process_details.append(comp)
        number_of_biomass = int(infile.read_values('biodg2')[0])
        biomass_details = []
        for i in range(number_of_biomass):
            biomass_1 = infile.read_values('biodg2.1')
            biomass_class = Biomass(index=i + 1, name='biom' + str(i), init_conc=biomass_1[0], min_conc=biomass_1[1],
                                    max_temp=biomass_1[2], death_rate=biomass_1[3], inhibition_constant=biomass_1[4])
            biomass_details.append(biomass_class)
        water_component = [Water_Bio('H2O')]
        all_components = water_component + self.gas + self.components
        dicta_all = []
        # for i in range(len(all_components)):
        #     dicta = {}
        #     dicta[all_components[i]] = []
        #     dicta_all.append(dicta)
        all_processes = []
        for i in range(len(process_details)):
            dicta_all = self.reset_bio_dicta(all_components)
            process = Process(biomass=biomass_details[process_details[i][0][1] - 1], numberOfComponents=process_details[i][0][0],
                              mumax=process_details[i][0][2], yield_mass=process_details[i][0][3],
                              NumOfCompetiting=process_details[i][0][4], NumOfNonCompetiting=process_details[i][0][5],
                              NumOfHaldane=process_details[i][0][6], enthalpy=process_details[i][0][7])
            for j in range(len(all_components)):
                dicta_all[j][all_components[j]].append(process_details[i][5][j])
                for k in range(len(process_details[i][1])):
                    if process_details[i][1][k] == j + 1:
                        dicta_all[j][all_components[j]].append(process_details[i][1][k + 1])
                if len(dicta_all[j][all_components[j]]) == 1:
                    all_components[j].addToProcess(process, dicta_all[j][all_components[j]][0])
                elif len(dicta_all[j][all_components[j]]) == 2:
                    all_components[j].addToProcess(process, dicta_all[j][all_components[j]][0], dicta_all[j][all_components[j]][1])
                elif len(dicta_all[j][all_components[j]]) == 3:
                    all_components[j].addToProcess(process, dicta_all[j][all_components[j]][0], dicta_all[j][all_components[j]][1],
                                                   dicta_all[j][all_components[j]][2])
                elif len(dicta_all[j][all_components[j]]) == 4:
                    all_components[j].addToProcess(process, dicta_all[j][all_components[j]][0], dicta_all[j][all_components[j]][1],
                                                   dicta_all[j][all_components[j]][2], dicta_all[j][all_components[j]][3])
                elif len(dicta_all[j][all_components[j]]) == 5:
                    all_components[j].addToProcess(process, dicta_all[j][all_components[j]][0], dicta_all[j][all_components[j]][1],
                                                   dicta_all[j][all_components[j]][2], dicta_all[j][all_components[j]][3], dicta_all[j][all_components[j]][4])
            all_processes.append(process)
        biodegradation = BIODG(imonod=params[0], bfac=params[2], sw1=params[4], sw2=params[5], wea=params[6], wsub=params[7],
                               processes=all_processes, biomass=biomass_details, icflag=params[1])
        self.biodg.append(biodegradation)

    def write_biodg(self, outfile):
        """ Writes Biodegradation Block """
        outfile.write('BIODG\n')
        value = self.biodg[0]
        vals = value.getFirstSet()
        # numberOfBiomass = value.getNumberOfBiomasses()
        outfile.write_values(vals, 'biodg')
        vals = [len(value.processes)]
        outfile.write_values(vals, 'biodg1')
        for i in range(len(value.processes)):
            sub_degrade = value.processes[i].getKs()
            comp_degrade = value.processes[i].getKc()
            ncomp_degrade = value.processes[i].getKnc()
            h_degrade = value.processes[i].getKh()
            uptake = value.processes[i].getUptake()
            vals = [len(sub_degrade), value.processes[i].biomass.index, value.processes[i].mumax,
                    value.processes[i].yield_mass,
                    value.processes[i].NumOfCompetiting, value.processes[i].NumOfNonCompetiting,
                    value.processes[i].NumOfHaldane, value.processes[i].enthalpy]
            outfile.write_values(vals, 'biodg1.1')
            vals = []
            for j in sub_degrade:
                component = list(j.keys())[0]
                vals.append(component)
                value1 = list(j.values())[0]
                vals.append(value1)
            outfile.write_values(vals, 'biodg1.1.1')
            vals = []
            if len(comp_degrade) != 0:
                for j in comp_degrade:
                    component = list(j.keys())[0]
                    vals.append(component)
                    value1 = list(j.values())[0]
                    vals.append(value1)
            else:
                vals = [0]
            outfile.write_values(vals, 'biodg1.1.2')
            vals = []
            if len(ncomp_degrade) != 0:
                for j in ncomp_degrade:
                    component = list(j.keys())[0]
                    vals.append(component)
                    value1 = list(j.values())[0]
                    vals.append(value1)
            else:
                vals = [0]
            outfile.write_values(vals, 'biodg1.1.3')
            vals = []
            if len(h_degrade) != 0:
                for j in h_degrade:
                    component = list(j.keys())[0]
                    vals.append(component)
                    value1 = list(j.values())[0]
                    vals.append(value1)
            else:
                vals = [0]
            outfile.write_values(vals, 'biodg1.1.4')
            vals = uptake
            outfile.write_values(vals, 'biodg1.1.5')
        vals = [len(value.biomass)]
        outfile.write_values(vals, 'biodg2')
        for i in range(len(value.biomass)):
            vals = [value.biomass[i].init_conc, value.biomass[i].min_conc, value.biomass[i].max_temp,
                    value.biomass[i].death_rate, value.biomass[i].inhibition_constant]
            outfile.write_values(vals, 'biodg2.1')

    def read_solids(self, infile):
        """ Reads Solids Block """
        pass

    def write_solids(self, outfile):
        outfile.write('SOLIDS\n')
        outfile.write_values(len(self.solids), 'solids1')
        for i in range(len(self.solids)):
            value = self.solids[i]
            vals = value.getFirstSet()
            outfile.write_values(vals, 'solids2')

    def read_parameters(self, infile):
        """ Reads Parameters Block """
        """Reads simulation parameters"""
        spec = ['param1', 'param1_autough2'][self.type == 'AUTOUGH2']
        # infile.read_value_line(self.parameter, spec)
        infile.read_params_value_line(self.parameter, spec)
        mops = self.parameter['_option_str'].rstrip().ljust(24).replace(' ', '0')
        self.parameter['option'] = np.array([0] + [int(mop) for mop in mops], int)
        # infile.read_value_line(self.parameter, 'param2')
        infile.read_params_value_line(self.parameter, 'param2')
        if (self.parameter['print_block'] is not None) and \
                (self.parameter['print_block'].strip() == ''):
            self.parameter['print_block'] = None
        self.read_timesteps(infile)
        # infile.read_value_line(self.parameter, 'param3')
        infile.read_params_value_line(self.parameter, 'param3')
        infile.read_value_line(self.parameter, 'param4')
        for val in infile.read_values('default_incons'):
            self.parameter['default_incons'].append(val)
        self.parameter['default_incons'] = trim_trailing_nones(self.parameter['default_incons'])
        # read any additional lines of default incons:
        more = True
        while more:
            line = padstring(infile.readline())
            if line.strip():
                section = any([line.startswith(keyword) for keyword in t2bio_sections])
                if section:
                    more = False
                else:
                    more_incons = infile.parse_string(line, 'default_incons')
                    more_incons = trim_trailing_nones(more_incons)
                    self.parameter['default_incons'] += more_incons
            else:
                more, line = False, None
        return line

    def write_parameters(self, outfile):
        """ Writes Parameters Block """
        outfile.write('PARAM\n')
        from copy import copy
        paramw = copy(self.parameter)
        if paramw['print_block'] is not None:
            paramw['print_block'] = unfix_blockname(paramw['print_block'])
        self.parameter['_option_str'] = ''.join([str(m) for m in self.parameter['option'][1:]])
        spec = ['param1', 'param1_autough2'][self.type == 'AUTOUGH2']
        outfile.write_value_line(self.parameter, spec)
        outfile.write_value_line(paramw, 'param2')
        self.write_timesteps(outfile)
        outfile.write_value_line(self.parameter, 'param3')
        outfile.write_value_line(self.parameter, 'param4')
        num_vars = len(self.parameter['default_incons'])
        if num_vars > 0:
            nlines = int(ceil(num_vars / 4.))
            for i in range(nlines):
                i1, i2 = i * 4, min((i + 1) * 4, num_vars)
                vals = list(self.parameter['default_incons'][i1: i2])
                if len(vals) < 4:
                    vals += [None] * (4 - len(vals))
                outfile.write_values(vals, 'default_incons')
        else:
            outfile.write('\n')

    def read_more_options(self, infile):
        """Reads additional parameter options"""
        infile.read_value_line(self.__dict__, '_more_option_str')
        momops = self._more_option_str.rstrip().ljust(21).replace(' ', '0')
        self.more_option = np.array([0] + [int(mop) for mop in momops], int)

    def read_multi(self, infile):
        """Reads EOS parameters"""
        spec = ['multi', 'multi_autough2'][self.type == 'AUTOUGH2']
        # spec = self.specification[spec]
        # vals = infile.read_values('multi')
        # for var, val in zip(spec[0], vals):
        #     if val is not None: self.multi[var] = val
        infile.read_multi_value_line(self.multi, spec)
        if 'eos' in self.multi:
            self.multi['eos'] = self.multi['eos'].strip()

    def write_start(self, outfile):
        """ Writes Start Block """
        if self.start:
            outfile.write('START\n')

    def read(self, filename='', meshfilename='', runlocation=''):
        """Reads data from file.  Mesh data can optionally be read from an
        auxiliary file.  Extra precision data will also be read from
        an associated '.pdat' file, if it exists.
        """
        if runlocation:
            if not os.path.isdir(runlocation):
                os.mkdir(runlocation)
            os.chdir(runlocation)
        if filename:
            self.filename = filename
        mode = 'r' if sys.version_info > (3,) else 'rU'
        infile = t2bio_parser(self.filename, mode, read_function=self.read_function)
        self.read_title(infile)
        self._sections = []
        more = True
        next_line = None
        while more:
            if next_line:
                line = next_line
            else:
                line = infile.readline()
            if line:
                keyword = line[0: 5].strip()
                if keyword in ['ENDCY', 'ENDFI']:
                    more = False
                    self.end_keyword = keyword
                elif keyword in t2bio_sections:
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
        infile.close()
        if meshfilename and (self.grid.num_blocks == 0):
            self.meshfilename = meshfilename
            if isinstance(meshfilename, str):
                mode = 'r' if sys.version_info > (3,) else 'rU'
                meshfile = t2bio_parser(self.meshfilename, mode, read_function=self.read_function)
                self.read_meshfile(meshfile)
                meshfile.close()
            elif isinstance(meshfilename, (list, tuple)):
                if len(meshfilename) == 2:
                    self.read_binary_meshfiles()
            else:
                print('Mesh filename must be either a string or a two-element tuple or list.')
        self.status = 'successful'
        return self

    def write(self, filename='', meshfilename='', runlocation='',
              extra_precision=None, echo_extra_precision=None):
        """Writes data to file.  Mesh data can optionally be written to an
        auxiliary file.  For AUTOUGH2, if extra_precision is True or a
        list of section names, the corresponding data sections will be
        written to an extra precision file; otherwise, the same
        sections (if any) that were read in as extra precision will
        also be written out as extra precision.  If
        echo_extra_precision is True, the extra precision sections
        will also be written to the main data file.
        """

        if runlocation:
            if not os.path.isdir(runlocation):
                os.mkdir(runlocation)
            os.chdir(runlocation)
        if filename:
            self.filename = filename
        if self.filename == '':
            self.filename = 't2bio.dat'
        self.update_sections()
        mesh_sections = []
        if meshfilename:
            self.meshfilename = meshfilename
        if self.meshfilename:
            if isinstance(self.meshfilename, str):
                meshfile = t2bio_parser(self.meshfilename, 'w')
                self.write_blocks(meshfile)
                self.write_connections(meshfile)
                meshfile.close()
                mesh_sections = ['ELEME', 'CONNE']
            elif isinstance(self.meshfilename, (list, tuple)):
                if len(self.meshfilename) == 2:
                    self.write_binary_meshfiles()
                    mesh_sections = ['ELEME', 'CONNE']
        if self.type == 'AUTOUGH2':
            self.write_extra_precision(extra_precision, echo_extra_precision)
        outfile = t2bio_parser(self.filename, 'w')
        self.write_title(outfile)
        for keyword in self._sections:
            if (keyword not in mesh_sections) and \
                    ((keyword not in self.extra_precision) or (keyword in self.extra_precision and self.echo_extra_precision)):
                self.write_fn[keyword](outfile)
        outfile.write(self.end_keyword + '\n')
        self.status = 'successful'
        outfile.close()
