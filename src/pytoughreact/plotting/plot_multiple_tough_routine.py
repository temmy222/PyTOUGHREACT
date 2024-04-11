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

import itertools
from pytoughreact.utilities.t2_utilities import T2Utilities
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pytoughreact.results.result_tough_3 import ResultTough3
from pytoughreact.results.result_tough_react import ResultReact
from pytoughreact.results.simple_experiment_data import Experiment
import pytoughreact.constants.generalconstants as gc
import pytoughreact.constants.plotconstants as pc
from pytoughreact.exceptions.custom_error import ParameterLessThanThreeError


class PlotMultiTough(object):
    def __init__(self, simulatortype, filelocations, filetitles, **kwargs):
        """
        Class for processing multiple file results

        Parameters
        -----------
        file_location :  str
            specifies the location of the file on the system
        file_title : str
            gives the title of the file e.g 'kdd.conc' or 'OUTPUT.csv'.
        simulator_type: str
            can either be toughreact, tmvoc or tough3

        **kwargs

        generation : str
            generation file location
        restart_files : str
            restart file location
        experiment : str
            experimental file location


        Returns
        --------

        """
        self.filelocations = filelocations
        self.filetitles = filetitles
        self.simulatortype = simulatortype
        self.modifier = T2Utilities()
        self.generation = kwargs.get(gc.GENERATION)
        self.args = kwargs.get(gc.RESTART_FILES)
        self.expt = kwargs.get(gc.EXPERIMENT)
        self.x_slice_value = kwargs.get(gc.X_SLICE_VALUE)

    def read_file(self):
        os.chdir(self.filelocations)
        if (self.simulatortype.lower() == gc.TMVOC or
                self.simulatortype.lower() == gc.TOUGH3):
            file_reader = ResultTough3(self.simulatortype, self.filelocations,
                                       self.filetitles, generation=self.generation)
        else:
            file_reader = ResultReact(self.simulatortype, self.filelocations,
                                      self.filetitles)
        return file_reader

    def read_file_multi(self, file, filetitle):
        os.chdir(file)
        if (self.simulatortype.lower() == gc.TMVOC or
                self.simulatortype.lower() == gc.TOUGH3):
            file_reader = ResultTough3(self.simulatortype, file, filetitle)
        else:
            file_reader = ResultReact(self.simulatortype, file, filetitle)
        return file_reader

    def get_restart_locations(self):
        restart_files = list()
        restart_files.append(self.filelocations)
        restart_files = restart_files + self.args
        return restart_files

    def get_restart_data_time(self, format_of_date):
        locations = self.get_restart_locations()
        final_time = []
        for i in range(0, len(locations)):
            if (self.simulatortype.lower() == gc.TMVOC or
                    self.simulatortype.lower() == gc.TOUGH3):
                file_reader = ResultTough3(self.simulatortype, locations[i],
                                           self.filetitle)
            else:
                file_reader = ResultReact(self.simulatortype, locations[i],
                                          self.filetitles)
            if i == 0:
                time_year = file_reader.convert_times(format_of_date)
                final_time.append(time_year)
            else:
                time_year = file_reader.convert_times(format_of_date)
                time_year = time_year[1:]
                final_time.append(time_year)
        final_time = list(itertools.chain.from_iterable(final_time))
        return final_time

    def get_restart_data_element(self, param, gridblocknumber):
        locations = self.get_restart_locations()
        final_result = []
        for i in range(0, len(locations)):
            if (self.simulatortype.lower() == gc.TMVOC or
                    self.simulatortype.lower() == gc.TOUGH3):
                file_reader = ResultTough3(self.simulatortype, locations[i],
                                           self.filetitles)
            else:
                file_reader = ResultReact(self.simulatortype, locations[i],
                                          self.filetitles)
            if i == 0:
                result_array = file_reader.get_timeseries_data(param,
                                                               gridblocknumber)
                final_result.append(result_array)
            else:
                result_array = file_reader.get_timeseries_data(param,
                                                               gridblocknumber)
                result_array = result_array[1:]
                final_result.append(result_array)
        final_result = list(itertools.chain.from_iterable(final_result))
        return final_result

    def _raw_multi_plot_restart_horizontal(self, param, format_of_date,
                                           gridblocknumber):
        """ Line Plots of a multiple parameter in the results file as a
        function of time in horizontal orientation with restart

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year


        Returns
        --------

        """
        time_year = self.get_restart_data_time(format_of_date)
        j = 0
        fig, axs = plt.subplots(len(param), sharex=False)
        for parameter in param:
            result_array = self.get_restart_data_element(parameter,
                                                         gridblocknumber)
            parameters = T2Utilities()
            time_year, result_array = parameters.remove_repetiting(time_year, result_array)
            axs[j].plot(time_year, result_array, marker=pc.CARET,
                        label=self.modifier.param_label_full(
                            parameter.upper()))
            axs[j].set_ylabel(self.modifier.param_label_full(
                parameter.upper()), fontsize=12)
            axs[j].spines[pc.BOTTOM].set_linewidth(1.5)
            axs[j].spines[pc.LEFT].set_linewidth(1.5)
            axs[j].spines[pc.TOP].set_linewidth(0)
            axs[j].spines[pc.RIGHT].set_linewidth(0)
            if format_of_date.lower() == pc.YEAR:
                axs[j].set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
            elif format_of_date.lower() == pc.DAY:
                axs[j].set_xlabel(pc.X_LABEL_TIME_DAY, fontsize=12)
            elif format_of_date.lower() == pc.HOUR:
                axs[j].set_xlabel(pc.X_LABEL_TIME_HOUR, fontsize=12)
            elif format_of_date.lower() == pc.MINUTE:
                axs[j].set_xlabel(pc.X_LABEL_TIME_MINUTE, fontsize=12)
            axs[j].ticklabel_format(useOffset=False)
            plt.setp(axs[j].get_xticklabels(), fontsize=12)
            plt.setp(axs[j].get_yticklabels(), fontsize=12)
            j = j + 1
        plt.tight_layout()
        plt.show()
        fig.savefig(pc.MULTI_PLOT_DESCRIPTION_LABEL, bbox_inches=pc.TIGHT_BBOX,
                    dpi=600)

    def _raw_multi_plot_restart_vertical(self, param, gridblocknumber,
                                         format_of_date):
        """ Line Plots of a multiple parameter in the results file as a
        function of time in vertical orientation with restart

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year


        Returns
        --------

        """
        time_year = self.get_restart_data_time(format_of_date)
        fig = plt.figure()
        for number in range(1, len(param) + 1):
            ax = fig.add_subplot(1, len(param), number)
            result_array = self.get_restart_data_element(param[number - 1],
                                                         gridblocknumber)
            ax.plot(time_year, result_array, marker=pc.CARET_SYMBOL,
                    label=self.modifier.param_label_full(
                        param[number - 1].upper()))
            ax.set_ylabel(self.modifier.param_label_full(
                param[number - 1].upper()), fontsize=12)
            ax.spines[pc.BOTTOM].set_linewidth(1.5)
            ax.spines[pc.LEFT].set_linewidth(1.5)
            ax.spines[pc.TOP].set_linewidth(0)
            ax.spines[pc.RIGHT].set_linewidth(0)
            ax.ticklabel_format(useOffset=False)
            plt.setp(ax.get_xticklabels(), fontsize=12)
            plt.setp(ax.get_yticklabels(), fontsize=12)
            # ax.legend(loc=pc.LOC_BEST,borderpad=0.1)
            if format_of_date.lower() == pc.YEAR:
                ax.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
            elif format_of_date.lower() == pc.DAY:
                ax.set_xlabel(pc.X_LABEL_TIME_DAY, fontsize=12)
            elif format_of_date.lower() == pc.HOUR:
                ax.set_xlabel(pc.X_LABEL_TIME_HOUR, fontsize=12)
            elif format_of_date.lower() == pc.MINUTE:
                ax.set_xlabel(pc.X_LABEL_TIME_MINUTE, fontsize=12)
        plt.tight_layout()
        plt.show()
        fig.savefig(pc.MULTI_PLOT_DESCRIPTION_LABEL, bbox_inches=pc.TIGHT_BBOX,
                    dpi=600)

    def multi_time_plot_restart(self, param, gridblocknumber, format_of_date,
                                style=pc.HORIZONTAL):
        """ Line Plots of a multiple parameter in the results file as a
        function of time for restart files

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year



        Returns
        --------

        """
        if style.lower() == pc.HORIZONTAL:
            if self.expt:
                if isinstance(param, list) and len(param) < 3:
                    try:
                        with plt.style.context(pc.MY_STYLE):
                            self._raw_multi_plot_restart_horizontal_with_expt(
                                param, format_of_date, gridblocknumber)
                    except Exception:
                        with plt.style.context(pc.CLASSIC):
                            self._raw_multi_plot_restart_horizontal_with_expt(
                                param, format_of_date, gridblocknumber)
                else:
                    raise ParameterLessThanThreeError()
            else:
                if isinstance(param, list) and len(param) < 3:
                    try:
                        with plt.style.context(pc.MY_STYLE):
                            self._raw_multi_plot_horizontal(param,
                                                            format_of_date,
                                                            gridblocknumber)
                    except Exception:
                        with plt.style.context(pc.CLASSIC):
                            self._raw_multi_plot_horizontal(param,
                                                            format_of_date,
                                                            gridblocknumber)
                else:
                    raise ParameterLessThanThreeError()
        elif style.lower() == pc.VERTICAL:
            if self.expt:
                if isinstance(param, list) and len(param) < 3:
                    try:
                        with plt.style.context(pc.MY_STYLE):
                            self._raw_multi_plot_vertical_with_expt(
                                param, format_of_date, gridblocknumber)
                    except Exception:
                        with plt.style.context(pc.CLASSIC):
                            self._raw_multi_plot_vertical_with_expt(
                                param, format_of_date, gridblocknumber)
                else:
                    raise ParameterLessThanThreeError()
            else:
                if isinstance(param, list) and len(param) < 3:
                    try:
                        with plt.style.context(pc.MY_STYLE):
                            self._raw_multi_plot_vertical(
                                param, format_of_date, gridblocknumber)
                    except Exception:
                        with plt.style.context(pc.CLASSIC):
                            self._raw_multi_plot_vertical(
                                param, format_of_date, gridblocknumber)
                else:
                    raise ParameterLessThanThreeError()

    def _raw_multi_plot_horizontal(self, param, format_of_date,
                                   gridblocknumber):
        """ Line Plots of a multiple parameter in the results file as a
        function of time in horizontal orientation

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year

        Returns
        --------

        """
        file_reader = self.read_file()
        time_year = file_reader.convert_times(format_of_date)
        j = 0
        fig, axs = plt.subplots(len(param), sharex=False)
        for parameter in param:
            result_array = file_reader.get_timeseries_data(parameter,
                                                           gridblocknumber)
            axs[j].plot(time_year, result_array, marker=pc.CARET_SYMBOL,
                        label=self.modifier.param_label_full(
                            parameter.upper()))
            axs[j].set_ylabel(self.modifier.param_label_full(
                parameter.upper()), fontsize=12)
            axs[j].spines[pc.BOTTOM].set_linewidth(1.5)
            axs[j].spines[pc.LEFT].set_linewidth(1.5)
            axs[j].spines[pc.TOP].set_linewidth(0)
            axs[j].spines[pc.RIGHT].set_linewidth(0)
            if format_of_date.lower() == pc.YEAR:
                axs[j].set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
            elif format_of_date.lower() == pc.DAY:
                axs[j].set_xlabel(pc.X_LABEL_TIME_DAY, fontsize=12)
            elif format_of_date.lower() == pc.HOUR:
                axs[j].set_xlabel(pc.X_LABEL_TIME_HOUR, fontsize=12)
            elif format_of_date.lower() == pc.MINUTE:
                axs[j].set_xlabel(pc.X_LABEL_TIME_MINUTE, fontsize=12)
            axs[j].ticklabel_format(useOffset=False)
            plt.setp(axs[j].get_xticklabels(), fontsize=12)
            plt.setp(axs[j].get_yticklabels(), fontsize=12)
            j = j + 1
        plt.tight_layout()
        plt.show()
        fig.savefig(pc.MULTI_PLOT_DESCRIPTION_LABEL, bbox_inches=pc.TIGHT_BBOX,
                    dpi=600)

    def _raw_multi_plot_horizontal_with_expt(self, param,
                                             format_of_date, gridblocknumber,
                                             data_file='data_file.csv'):
        """ Line Plots of a multiple parameter in the results file as a
        function of time in horizontal orientation with experiment

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        data_file: str
            The name of the data file containing the experimental data



        Returns
        --------

        """
        file_reader = self.read_file()
        time_year = file_reader.convert_times(format_of_date)
        expt_test = Experiment(self.expt[0], data_file)
        time_year_expt = expt_test.get_times()
        j = 0
        fig, axs = plt.subplots(len(param), sharex=False)
        for parameter in param:
            result_array = file_reader.get_timeseries_data(parameter,
                                                           gridblocknumber)
            result_array_expt = expt_test.get_timeseries_data(parameter)
            axs[j].plot(time_year, result_array, marker=pc.CARET_SYMBOL,
                        label=gc.SIMULATION)
            if max(result_array_expt) <= 0:
                dy = 0.1 * abs(min(result_array_expt))
            else:
                dy = 0.1 * abs(max(result_array_expt))
            axs[j].errorbar(time_year_expt, result_array_expt, yerr=dy,
                            fmt=pc.COLOR_FORMAT, color=pc.RED_SYMBOL,
                            label=gc.EXPERIMENT)
            axs[j].set_ylabel(self.modifier.param_label_full(
                parameter.upper()), fontsize=12)
            axs[j].spines[pc.BOTTOM].set_linewidth(1.5)
            axs[j].spines[pc.LEFT].set_linewidth(1.5)
            axs[j].spines[pc.TOP].set_linewidth(0)
            axs[j].spines[pc.RIGHT].set_linewidth(0)
            if format_of_date.lower() == pc.YEAR:
                axs[j].set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
            elif format_of_date.lower() == pc.DAY:
                axs[j].set_xlabel(pc.X_LABEL_TIME_DAY, fontsize=12)
            elif format_of_date.lower() == pc.HOUR:
                axs[j].set_xlabel(pc.X_LABEL_TIME_HOUR, fontsize=12)
            elif format_of_date.lower() == pc.MINUTE:
                axs[j].set_xlabel(pc.X_LABEL_TIME_MINUTE, fontsize=12)
            axs[j].ticklabel_format(useOffset=False)
            axs[j].legend(loc=pc.LOC_BEST)
            plt.setp(axs[j].get_xticklabels(), fontsize=12)
            plt.setp(axs[j].get_yticklabels(), fontsize=12)
            j = j + 1
        plt.tight_layout()
        plt.show()
        os.chdir(self.filelocations)
        fig.savefig(pc.MULTI_PLOT_DESCRIPTION_LABEL, bbox_inches=pc.TIGHT_BBOX,
                    dpi=600)

    def _raw_multi_plot_restart_horizontal_with_expt(self,
                                                     param,
                                                     format_of_date,
                                                     gridblocknumber,
                                                     data_file='data_file.csv'
                                                     ):
        """ Line Plots of a multiple parameter in the results file as a
        function of time in horizontal orientation for restart files

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        data_file: str
            The name of the data file containing the experimental data



        Returns
        --------

        """
        time_year = self.get_restart_data_time(format_of_date)
        j = 0
        fig, axs = plt.subplots(len(param), sharex=False)
        expt_test = Experiment(self.expt[0], data_file)
        time_year_expt = expt_test.get_times()
        for parameter in param:
            result_array = self.get_restart_data_element(parameter,
                                                         gridblocknumber)
            parameters = T2Utilities()
            time_year, result_array = parameters.remove_repetiting(time_year, result_array)
            result_array_expt = expt_test.get_timeseries_data(parameter)
            axs[j].plot(time_year, result_array, marker=pc.CARET_SYMBOL,
                        label=gc.SIMULATION)
            if max(result_array_expt) <= 0:
                dy = 0.15 * abs(min(result_array_expt))
            else:
                dy = 0.15 * abs(max(result_array_expt))
            axs[j].errorbar(time_year_expt, result_array_expt, yerr=dy,
                            fmt=pc.COLOR_FORMAT, color=pc.RED_SYMBOL,
                            label=gc.EXPERIMENT)
            axs[j].set_ylabel(self.modifier.param_label_full(
                parameter.upper()), fontsize=12)
            axs[j].spines[pc.BOTTOM].set_linewidth(1.5)
            axs[j].spines[pc.LEFT].set_linewidth(1.5)
            axs[j].spines[pc.TOP].set_linewidth(0)
            axs[j].spines[pc.RIGHT].set_linewidth(0)
            if format_of_date.lower() == pc.YEAR:
                axs[j].set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
            elif format_of_date.lower() == pc.DAY:
                axs[j].set_xlabel(pc.X_LABEL_TIME_DAY, fontsize=12)
            elif format_of_date.lower() == pc.HOUR:
                axs[j].set_xlabel(pc.X_LABEL_TIME_HOUR, fontsize=12)
            elif format_of_date.lower() == pc.MINUTE:
                axs[j].set_xlabel(pc.X_LABEL_TIME_MINUTE, fontsize=12)
            axs[j].ticklabel_format(useOffset=False)
            plt.setp(axs[j].get_xticklabels(), fontsize=12)
            plt.setp(axs[j].get_yticklabels(), fontsize=12)
            axs[j].legend()
            j = j + 1
        plt.tight_layout()
        plt.show()
        os.chdir(self.filelocations)
        fig.savefig(pc.MULTI_PLOT_EXPERIMENT_RESTART_LABEL,
                    bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def _raw_multi_plot_vertical(self, param, format_of_date, gridblocknumber):
        """ Line Plots of a multiple parameter in the results file as a
        function of time in vertical orientation

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year


        Returns
        --------

        """
        file_reader = self.read_file()
        time_year = file_reader.convert_times(format_of_date)
        j = 0
        fig = plt.figure()
        for number in range(1, len(param) + 1):
            ax = fig.add_subplot(1, len(param), number)
            result_array = file_reader.get_timeseries_data(param[number - 1],
                                                           gridblocknumber)
            ax.plot(time_year, result_array, marker=pc.CARET_SYMBOL,
                    label=self.modifier.param_label_full(
                        param[number - 1].upper()))
            ax.set_ylabel(self.modifier.param_label_full(
                param[number - 1].upper()), fontsize=12)
            ax.spines[pc.BOTTOM].set_linewidth(1.5)
            ax.spines[pc.LEFT].set_linewidth(1.5)
            ax.spines[pc.TOP].set_linewidth(0)
            ax.spines[pc.RIGHT].set_linewidth(0)
            ax.ticklabel_format(useOffset=False)
            plt.setp(ax.get_xticklabels(), fontsize=12)
            plt.setp(ax.get_yticklabels(), fontsize=12)
            if format_of_date.lower() == pc.YEAR:
                ax.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
            elif format_of_date.lower() == pc.DAY:
                ax.set_xlabel(pc.X_LABEL_TIME_DAY, fontsize=12)
            elif format_of_date.lower() == pc.HOUR:
                ax.set_xlabel(pc.X_LABEL_TIME_HOUR, fontsize=12)
            elif format_of_date.lower() == pc.MIN:
                ax.set_xlabel(pc.X_LABEL_TIME_MIN, fontsize=12)
            j = j + 1
        plt.tight_layout()
        plt.show()
        fig.savefig(pc.MULTI_PLOT_DESCRIPTION_LABEL, bbox_inches=pc.TIGHT_BBOX,
                    dpi=600)

    def _raw_multi_plot_vertical_with_expt(self, param, format_of_date,
                                           grid_block_number,
                                           data_file='data_file.csv'):
        """ Line Plots of a multiple parameter in the results file as a
        function of time in vertical orientation

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        data_file: str
            The name of the data file containing the experimental data



        Returns
        --------

        """
        file_reader = self.read_file()
        time_year = file_reader.convert_times(format_of_date)
        expt_test = Experiment(self.expt[0], data_file)
        time_year_expt = expt_test.get_times()
        j = 0
        fig = plt.figure()
        for number in range(1, len(param) + 1):
            ax = fig.add_subplot(1, len(param), number)
            result_array_expt = expt_test.get_timeseries_data(
                param[number - 1])
            result_array = file_reader.get_timeseries_data(param[number - 1],
                                                           grid_block_number)
            ax.plot(time_year, result_array, marker=pc.CARET,
                    label=gc.SIMULATION)
            ax.plot(time_year_expt, result_array_expt, '--', marker='o',
                    color=pc.RED_COLOR, label=gc.EXPERIMENT)
            ax.set_ylabel(self.modifier.param_label_full(
                param[number - 1].upper()), fontsize=12)
            ax.spines[pc.BOTTOM].set_linewidth(1.5)
            ax.spines[pc.LEFT].set_linewidth(1.5)
            ax.spines[pc.TOP].set_linewidth(0)
            ax.spines[pc.RIGHT].set_linewidth(0)
            ax.ticklabel_format(useOffset=False)
            plt.setp(ax.get_xticklabels(), fontsize=12)
            plt.setp(ax.get_yticklabels(), fontsize=12)
            ax.legend(loc=pc.LOC_BEST, borderpad=0.1)
            if format_of_date.lower() == pc.YEAR:
                ax.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
            elif format_of_date.lower() == pc.DAY:
                ax.set_xlabel(pc.X_LABEL_TIME_DAY, fontsize=12)
            elif format_of_date.lower() == pc.HOUR:
                ax.set_xlabel(pc.X_LABEL_TIME_HOUR, fontsize=12)
            elif format_of_date.lower() == pc.MIN:
                ax.set_xlabel(pc.X_LABEL_TIME_MIN, fontsize=12)
            j = j + 1
        plt.tight_layout()
        plt.show()
        fig.savefig(pc.MULTI_PLOT_DESCRIPTION_LABEL, bbox_inches=pc.TIGHT_BBOX,
                    dpi=600)

    def multi_time_plot(self, param, gridblocknumber, format_of_date,
                        style=pc.HORIZONTAL):
        """ Line Plots of a multiple parameter in the results file as a
        function of time

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or yeart


        Returns
        --------

        """
        if style.lower() == pc.HORIZONTAL:
            if self.expt:
                if isinstance(param, list) and len(param) < 3:
                    try:
                        with plt.style.context(pc.MY_STYLE):
                            self._raw_multi_plot_horizontal_with_expt(
                                param, format_of_date, gridblocknumber)
                    except Exception:
                        with plt.style.context(pc.CLASSIC):
                            self._raw_multi_plot_horizontal_with_expt(
                                param, format_of_date, gridblocknumber)
                else:
                    raise ParameterLessThanThreeError()
            else:
                if isinstance(param, list) and len(param) < 3:
                    try:
                        with plt.style.context(pc.MY_STYLE):
                            self._raw_multi_plot_horizontal(
                                param, format_of_date, gridblocknumber)
                    except Exception:
                        with plt.style.context(pc.CLASSIC):
                            self._raw_multi_plot_horizontal(
                                param, format_of_date, gridblocknumber)
                else:
                    raise ParameterLessThanThreeError()
        elif style.lower() == pc.VERTICAL:
            if self.expt:
                if isinstance(param, list) and len(param) < 3:
                    try:
                        with plt.style.context(pc.MY_STYLE):
                            self._raw_multi_plot_vertical_with_expt(
                                param, format_of_date, gridblocknumber)
                    except Exception:
                        with plt.style.context(pc.CLASSIC):
                            self._raw_multi_plot_vertical_with_expt(
                                param, format_of_date, gridblocknumber)
                else:
                    raise ParameterLessThanThreeError()
            else:
                if isinstance(param, list) and len(param) < 3:
                    try:
                        with plt.style.context(pc.MY_STYLE):
                            self._raw_multi_plot_vertical(
                                param, format_of_date, gridblocknumber)
                    except Exception:
                        with plt.style.context(pc.CLASSIC):
                            self._raw_multi_plot_vertical(
                                param, format_of_date, gridblocknumber)
                else:
                    raise ParameterLessThanThreeError()

    def _retrieve_multi_data(self, param, gridblocknumber):
        data_storage = {}
        file_names = []
        for parameter in param:
            file_number = 0
            for file in self.filelocations:
                file_reader = self.read_file_multi(
                    file, self.filetitles[file_number])
                filename = parameter + str(file_number)
                data_storage[filename] = file_reader.get_timeseries_data(
                    parameter, gridblocknumber)
                file_names.append(filename)
                file_number = file_number + 1
        return file_names, data_storage

    def _retrieve_multi_data_generation(self, param, format_of_date):
        """ Retrieve multi data for plotting

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        format_of_date: str
            The format of the date; could be minute, hour, day or year


        Returns
        --------
        data_table: pd.Dataframe
            returns the data in dataframe

        """
        data_table = pd.DataFrame()
        file_reader = self.read_file()
        for i in range(len(param)):
            time_data_label = pc.TIME + str(i)
            result_data_label = pc.RESULT + str(i)
            time_data = file_reader.convert_times(format_of_date=format_of_date)
            result_data = file_reader.get_generation_data(param[i])
            data_table[time_data_label] = pd.Series(time_data)
            data_table[result_data_label] = pd.Series(result_data)
        return data_table

    def _slice_value(self, time, result):
        last_time = time[-1]
        last_result = result[-1]
        time_array = np.array(time)
        result_array = np.array(result)
        time_array = time_array[0:len(time_array) + 8:10]
        result_array = result_array[0:len(result_array) + 8:10]
        if len(time_array) > 10:
            return self._slice_value(time_array, result_array)
        time_array = np.append(time_array, last_time)
        result_array = np.append(result_array, last_result)
        return time_array, result_array

    def plot_multi_param_single_plot(self, param, gridblocknumber, format_of_date,
                                     labels=None):
        """ Line Multiple parameters in a single Plot

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        labels: list[str]
            labels of the different plots in the chart
        Returns
        --------

        """
        if self.generation is True:
            with plt.style.context(pc.CLASSIC):
                fig, axs = plt.subplots(1, 1)
                data_file = self._retrieve_multi_data_generation(param,
                                                                 format_of_date)
                legend_index = 0
                for i in range(0, len(data_file.columns), 2):
                    if labels is None:
                        axs.plot(data_file.iloc[:, i], data_file.iloc[:, i + 1],
                                 label=param[legend_index])
                    else:
                        axs.plot(data_file.iloc[:, i], data_file.iloc[:, i + 1],
                                 label=labels[legend_index])
                    axs.set_xlabel(pc.TIME_CAPS + ' ' + pc.OPEN_BRACKET +
                                   format_of_date + pc.CLOSE_BRACKET,
                                   fontsize=14)
                    axs.set_ylabel(pc.Mass_Fraction, fontsize=14)
                    legend_index += 1
                plt.setp(axs.get_xticklabels(), fontsize=14)
                plt.setp(axs.get_yticklabels(), fontsize=14)
                plt.legend()
                plt.tight_layout()
                plt.show()
                fig.savefig(pc.MULTIPLE_PARAM + ' ' + pc.VERSUS + ' ' +
                            pc.TIME + pc.IMAGE_TYPE, bbox_inches=pc.TIGHT_BBOX,
                            dpi=600)
        else:
            with plt.style.context(pc.CLASSIC):
                fig, axs = plt.subplots(1, 1)
                markers = pc.ALL_MARKERS
                file_reader = self.read_file()
                for i in range(0, len(param)):
                    time_year = file_reader.convert_times(format_of_date)
                    result_array = file_reader.get_timeseries_data(
                        param[i], gridblocknumber)
                    if len(time_year) > 50:
                        time_year, result_array = self._slice_value(
                            time_year, result_array)
                    if labels is None:
                        axs.plot(time_year, result_array, label=param[i],
                                 marker=markers[i])
                    else:
                        axs.plot(time_year, result_array, label=labels[i],
                                 marker=markers[i])
                    axs.set_xlabel(pc.TIME_CAPS + ' ' + pc.OPEN_BRACKET
                                   + format_of_date + pc.CLOSE_BRACKET,
                                   fontsize=14)
                    axs.set_ylabel(pc.MASS_FRACTION, fontsize=14)
                    axs.ticklabel_format(useOffset=False,
                                         style=pc.PLAIN_STYLE, axis=pc.BOTH)
                plt.setp(axs.get_xticklabels(), fontsize=14)
                plt.setp(axs.get_yticklabels(), fontsize=14)
                plt.legend(loc=pc.LOC_BEST)
                plt.tight_layout()
                plt.show()
                plt.tick_params(axis=pc.X, which=pc.MAJOR, labelsize=3)
                fig.savefig(param[0] + pc.MULTIPLE_PARAM_OUTPUT
                            + ' ' + pc.VERSUS + ' ' + pc.TIME + pc.IMAGE_TYPE,
                            bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def multi_param_multi_file_plot(self, param, gridblocknumber, labels,
                                    format_of_date=pc.YEAR,
                                    style=pc.HORIZONTAL,
                                    width=12, height=8):
        """ Line Plots of a multiple parameter in the results file as a
        function of time

        Parameters
        -----------
        param :  list[str]
            The parameters to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        labels: list[str]
            Labels for the plots
        style : str
            orientation for multiple plots; could be horizontal or vertical
        width : int
            width of plot
        height : int
            height of plot


        Returns
        --------

        """
        fig = plt.figure(figsize=(width, height))
        file_reader = self.read_file_multi(self.filelocations[0],
                                           self.filetitles[0])
        time_year = file_reader.convert_times(format_of_date)
        lst, dictionary = self._retrieve_multi_data(param, gridblocknumber)
        colors = pc.ALL_COLORS
        markers = pc.ALL_MARKERS
        counter_2 = 0
        param_counter = 0
        subplot_i = 2
        k = 0
        subplot_j = 2
        fig, axs = plt.subplots(subplot_i, subplot_j)
        for number in range(subplot_i):
            for i in range(subplot_j):
                for j in range(len(self.filelocations)):
                    axs[number, i].plot(time_year,
                                        dictionary[lst[counter_2 + j]],
                                        label=labels[k], linewidth=2,
                                        color=colors[j], marker=markers[j])
                    axs[number, i].set_ylabel(self.modifier.convert_parameter_name(
                        param[param_counter]))
                    axs[number, i].set_title(self.modifier.param_label_full(
                        [param_counter].upper()))
                    axs[number, i].set_xlabel(pc.X_LABEL_TIME_YEAR)
                    axs[number, i].spines[pc.BOTTOM].set_linewidth(1.5)
                    axs[number, i].spines[pc.LEFT].set_linewidth(1.5)
                    axs[number, i].spines[pc.TOP].set_linewidth(0.0)
                    axs[number, i].spines[pc.RIGHT].set_linewidth(0.0)
                counter_2 = counter_2 + len(self.filelocations)
                param_counter = param_counter + 1
            k = k + 1
        plt.subplots_adjust(left=0.125, wspace=0.4, top=0.95)
        plt.tight_layout()
        plt.show()
