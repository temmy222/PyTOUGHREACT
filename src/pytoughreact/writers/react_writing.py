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

from pytoughreact.constants.format_specifications import t2react_format_specification, t2react_extra_precision_format_specification
from pytoughreact.constants.defaults_constants import DEFAULT_REACT as default_react
from pytoughreact.constants.defaults_constants import DEFAULT_PARAMETERS as default_parameters
from pytoughreact.constants.sections import t2react_sections
from fixed_format_file import default_read_function, fixed_format_file
from pytoughreact.pytough_wrapper.wrapper.reactgrid import t2reactgrid
from pytoughreact.exceptions.custom_error import NotFoundError
from copy import deepcopy
from t2data import t2data
import numpy as np
import os
import sys
from pathlib import Path
from os.path import splitext, basename
from os import devnull, remove
from t2data import trim_trailing_nones
from mulgrids import padstring
from subprocess import call


class t2react_parser(fixed_format_file):
    """Class for parsing REACTION data file."""
    def __init__(self, filename, mode, read_function=default_read_function):
        super(t2react_parser, self).__init__(filename, mode,
                                             t2react_format_specification, read_function)


class t2_extra_precision_data_parser(fixed_format_file):
    """Class for parsing AUTOUGH2 extra-precision auxiliary data file."""
    def __init__(self, filename, mode, read_function=default_read_function):
        super(t2_extra_precision_data_parser,
              self).__init__(filename, mode,
                             t2react_extra_precision_format_specification,
                             read_function)


class t2react(t2data):
    def __init__(self, filename='', meshfilename='', read_function=default_read_function):
        """
        Main class for structuring the writing , reading and running of reaction simulations
        """
        super().__init__(filename='', meshfilename='', read_function=default_read_function)
        self.react = default_react.copy()
        self.grid = t2reactgrid()
        self.title = ''
        self.simulator = ''
        self.parameter = deepcopy(default_parameters)
        self._more_option_str = '0' * 21,
        self.more_option = np.zeros(22, int)
        self.multi = {}
        self.start = False
        self.relative_permeability = {}
        self.capillarity = {}
        self.lineq = {}
        self.output_times = {}
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

    def update_read_write_functions(self):
        """Updates functions for reading and writing sections of data file."""
        self.read_fn = dict(zip(
            t2react_sections,
            [self.read_simulator,
             self.read_rocktypes,
             self.read_parameters,
             self.read_react,
             self.read_more_options,
             self.read_start,
             self.read_noversion,
             self.read_rpcap,
             self.read_lineq,
             self.read_solver,
             self.read_multi,
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
            t2react_sections,
            [self.write_simulator,
             self.write_rocktypes,
             self.write_parameters,
             self.write_react,
             self.write_more_options,
             self.write_start,
             self.write_noversion,
             self.write_rpcap,
             self.write_lineq,
             self.write_solver,
             self.write_multi,
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
        corresponding data in the t2react object."""
        data_present = dict(zip(
            t2react_sections,
            [self.simulator,
             self.grid and self.grid.rocktypelist,
             self.parameter,
             self.react,
             np.any(self.more_option),
             self.start,
             self.noversion,
             self.relative_permeability or self.capillarity,
             self.lineq,
             self.solver,
             self.multi,
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
        return [keyword for keyword in t2react_sections if data_present[keyword]]
    present_sections = property(get_present_sections)

    def section_insertion_index(self, section):
        """Determines an appropriate position to insert the specified section
        in the internal list of data file sections.
        """
        try:
            listindex = t2react_sections.index(section)
            if listindex == 0:
                return 0  # SIMUL section
            else:
                # first look for sections above the one specified,
                # and put new one just after the last found:
                for i in reversed(range(listindex)):
                    try:
                        section_index = self._sections.index(t2react_sections[i])
                        return section_index + 1
                    except ValueError:
                        pass
                # look for sections below the one specified,
                # and put new one just before the first found:
                for i in range(listindex, len(t2react_sections)):
                    try:
                        section_index = self._sections.index(t2react_sections[i])
                        return section_index
                    except ValueError:
                        pass
                return len(self._sections)
        except ValueError:
            return len(self._sections)

    def check_for_executable(self, executable_name, directory):
        """
        check if the executable exists in the folder
        """
        path = Path(directory + '/' + executable_name)
        output = path.is_file()
        if output is True:
            return
        else:
            raise NotFoundError('Tough React Executable', path.resolve())

    def check_for_thermodynamic_database(self, directory, t2solute):
        """
        check if the thermodynamic database exists in the folder
        """
        database_name = t2solute.readio['database']
        path = Path(directory + '/' + database_name)
        output = path.is_file()
        if output is True:
            return
        else:
            raise NotFoundError('Thermodynamic Database', path.resolve())

    def run(self, t2solute, save_filename='', incon_filename='', runlocation='', simulator='AUTOUGH2_2',
            silent=False, output_filename=''):
        """Runs simulation using TOUGH2 ,AUTOUGH2, TOUGHREACT, TMVOC or TMVOCBIO.  It's assumed that the
        data object has been written to file using write().  For
        AUTOUGH2, if the filenames for the save file or initial
        conditions file are not specified, they are constructed by
        changing the extensions of the data filename.  Set silent to
        True to suppress screen output. The output_filename applies
        only to TOUGH2, and specifies the name of the main output
        listing file."""
        if runlocation:
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
            os.chdir(runlocation)
            self.check_for_thermodynamic_database(runlocation, t2solute)
            self.check_for_executable(simulator, runlocation)
        if self.filename:
            ROOT_DIR = os.path.abspath(os.curdir)
            self.check_for_executable(simulator, ROOT_DIR)
            self.check_for_thermodynamic_database(ROOT_DIR, t2solute)
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
                if os.path.exists("GENER"):
                    os.remove("GENER")
                if os.path.exists("OUTPUT_ELEME.csv"):
                    os.remove("OUTPUT_ELEME.csv")
                cmd = [simulator]
                infile = open(self.filename, 'r')
                if silent:
                    outfile = None
                else:
                    if output_filename == '':
                        datbase = 'screen_info'
                        outfilename = datbase + '.out'
                    else:
                        outfilename = output_filename
                    outfile = open(outfilename, 'w')
                # p = Popen(os.path.join(current_dir,">treacteos1<flow.inp"),cwd=current_dir)
                call(cmd, stdin=infile, stdout=outfile)
                # status_2 = run(["treacteos1<flow.inp"],
                #               stdout=PIPE,
                #               text=True,
                #               input="Hello from the other side")
                # print(status_2)

    def read_parameters(self, infile):
        """Reads simulation parameters"""
        spec = ['param1', 'param1_autough2'][self.type == 'AUTOUGH2']
        infile.read_value_line(self.parameter, spec)
        mops = self.parameter['_option_str'].rstrip().ljust(24).replace(' ', '0')
        self.parameter['option'] = np.array([0] + [int(mop) for mop in mops], int)
        infile.read_value_line(self.parameter, 'param2')
        if (self.parameter['print_block'] is not None) and (self.parameter['print_block'].strip() == ''):
            self.parameter['print_block'] = None
        self.read_timesteps(infile)
        infile.read_value_line(self.parameter, 'param3')
        for val in infile.read_values('default_incons'):
            self.parameter['default_incons'].append(val)
        self.parameter['default_incons'] = trim_trailing_nones(self.parameter['default_incons'])
        # read any additional lines of default incons:
        more = True
        while more:
            line = padstring(infile.readline())
            if line.strip():
                section = any([line.startswith(keyword) for keyword in t2react_sections])
                if section:
                    more = False
                else:
                    more_incons = infile.parse_string(line, 'default_incons')
                    more_incons = trim_trailing_nones(more_incons)
                    self.parameter['default_incons'] += more_incons
            else:
                more, line = False, None
        return line

    def read_react(self, infile):
        pass

    def write_react(self, outfile):
        outfile.write('REACT\n')
        vals = self.react
        outfile.write_values(vals, 'REACT')

    def read(self, filename='', meshfilename=''):
        """Reads data from file.  Mesh data can optionally be read from an
        auxiliary file.  Extra precision data will also be read from
        an associated '.pdat' file, if it exists.
        """
        if filename:
            self.filename = filename
        mode = 'r' if sys.version_info > (3,) else 'rU'
        infile = t2react_parser(self.filename, mode, read_function=self.read_function)
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
                elif keyword in t2react_sections:
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
                meshfile = t2react_parser(self.meshfilename, mode, read_function=self.read_function)
                self.read_meshfile(meshfile)
                meshfile.close()
            elif isinstance(meshfilename, (list, tuple)):
                if len(meshfilename) == 2:
                    self.read_binary_meshfiles()
            else:
                print('Mesh filename must be either a string or a two-element tuple or list.')
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
            self.filename = 't2react.dat'
        self.update_sections()
        mesh_sections = []
        if meshfilename:
            self.meshfilename = meshfilename
        if self.meshfilename:
            if isinstance(self.meshfilename, str):
                meshfile = t2react_parser(self.meshfilename, 'w')
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
        outfile = t2react_parser(self.filename, 'w')
        self.write_title(outfile)
        for keyword in self._sections:
            if (keyword not in mesh_sections) and ((keyword not in self.extra_precision) or
                                                   (keyword in self.extra_precision and self.echo_extra_precision)):
                self.write_fn[keyword](outfile)
        outfile.write(self.end_keyword + '\n')
        outfile.close()
