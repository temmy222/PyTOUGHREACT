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
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.interpolate import griddata
from pytoughreact.utilities.t2_utilities import t2Utilities
from pytoughreact.results.result_tough_3 import ResultTough3
from pytoughreact.results.result_tough_react import ResultReact
from pytoughreact.results.simple_experiment_data import Experiment
import pytoughreact.constants.generalconstants as gc
import pytoughreact.constants.plotconstants as pc
import pytoughreact.constants.grid_constants as grc
import pandas as pd


class PlotTough(object):
    def __init__(self, simulator_type, file_location, file_title, **kwargs):
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
        self.file_location = file_location
        os.chdir(self.file_location)
        self.filetitle = file_title
        self.simulatortype = simulator_type
        self.modifier = t2Utilities()
        self.generation = kwargs.get(gc.GENERATION)
        self.args = kwargs.get(gc.RESTART_FILES)
        self.expt = kwargs.get(gc.EXPERIMENT)

    def _read_file(self):
        """ Read in the input files

        """
        if (self.simulatortype.lower() == gc.TMVOC or
                self.simulatortype.lower() == gc.TOUGH3):
            fileReader = ResultTough3(self.simulatortype, self.file_location,
                                      self.filetitle,
                                      generation=self.generation)
        else:
            fileReader = ResultReact(self.simulatortype, self.file_location,
                                     self.filetitle)
        return fileReader

    def _plotRaw(self, param, grid_block_number,
                 format_of_date, restart=False):
        """ Line Plots of a parameter in the results file as a function of time

        Parameters
        -----------
        param :  str
            The parameter to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        restart: boolean
            If restart was performed in the simulation or not


        Returns
        --------

        """
        parameters = t2Utilities()
        if restart is True:
            time_year = self._getRestartDataTime(format_of_date)
            result_array = self._getRestartDataElement(param,
                                                       grid_block_number)
            time_year, result_array = parameters.remove_repetiting(time_year,
                                                                  result_array)
        else:
            fileReader = self._read_file()
            time_year = fileReader.convert_times(format_of_date)
            if self.generation is True:
                result_array = fileReader.get_generation_data(param)
            else:
                result_array = fileReader.get_timeseries_data(
                    param, grid_block_number)
        fig, axs = plt.subplots(1, 1)
        axs.plot(time_year, result_array, marker=pc.CARET_SYMBOL)
        if format_of_date.lower() == pc.YEAR:
            axs.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
        elif format_of_date.lower() == pc.DAY:
            axs.set_xlabel(pc.X_LABEL_TIME_DAY, fontsize=12)
        elif format_of_date.lower() == pc.HOUR:
            axs.set_xlabel(pc.X_LABEL_TIME_HOUR, fontsize=12)
        elif format_of_date.lower() == pc.MINUTE:
            axs.set_xlabel(pc.X_LABEL_TIME_MIN, fontsize=12)
        axs.set_ylabel(parameters.param_label_full(param.upper()), fontsize=12)
        axs.spines[pc.BOTTOM].set_linewidth(1.5)
        axs.spines[pc.LEFT].set_linewidth(1.5)
        axs.spines[pc.TOP].set_linewidth(0)
        axs.spines[pc.RIGHT].set_linewidth(0)
        plt.setp(axs.get_xticklabels(), fontsize=12)
        plt.setp(axs.get_yticklabels(), fontsize=12)
        plt.tight_layout()
        plt.show()
        if restart is True:
            fig.savefig(param + ' ' + pc.VERSUS + ' ' + pc.TIME + ' '
                        + pc.RESTART + pc.IMAGE_TYPE,
                        bbox_inches=pc.TIGHT_BBOX, dpi=600)
        else:
            fig.savefig(param + ' ' + pc.VERSUS + ' ' + pc.TIME
                        + pc.IMAGE_TYPE, bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def plotParamWithTime(self, param, grid_block_number, format_of_date):
        """ Line Plots of a parameter in the results file as a function of time

        Parameters
        -----------
        param :  str
            The parameter to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year

        Returns
        --------

        """
        if self.expt:
            try:
                with plt.style.context(pc.MY_STYLE):
                    self._plotRawWithExpt(param, grid_block_number,
                                          format_of_date)
            except Exception:
                with plt.style.context(pc.CLASSIC):
                    self._plotRawWithExpt(param, grid_block_number,
                                          format_of_date)
        else:
            try:
                with plt.style.context(pc.MY_STYLE):
                    self._plotRaw(param, grid_block_number, format_of_date)
            except Exception:
                with plt.style.context(pc.CLASSIC):
                    self._plotRaw(param, grid_block_number, format_of_date)

    def _getRestartLocations(self):
        """ Get Restart Locations

        """
        restart_files = list()
        restart_files.append(self.file_location)
        restart_files = restart_files + self.args
        return restart_files

    def _getRestartDataTime(self, format_of_date):
        """ Get Restart Time Data

        Parameters
        -----------
        format_of_date: str
            The format of the date; could be minute, hour, day or year

        Returns
        --------
        restart_time : list
            restart time data in a list

        """
        locations = self._getRestartLocations()
        restart_time = []
        for i in range(0, len(locations)):
            if (self.simulatortype.lower() == gc.TMVOC or
                    self.simulatortype.lower() == gc.TOUGH3):
                fileReader = ResultTough3(self.simulatortype, locations[i],
                                          self.filetitle)
            else:
                fileReader = ResultReact(self.simulatortype, locations[i],
                                         self.filetitle)
            if i == 0:
                time_year = fileReader.convert_times(format_of_date)
                restart_time.append(time_year)
            else:
                time_year = fileReader.convert_times(format_of_date)
                time_year = time_year[1:]
                restart_time.append(time_year)
        restart_time = list(itertools.chain.from_iterable(restart_time))
        return restart_time

    def _getRestartDataElement(self, param, grid_block_number):
        """ Get Restart Data

        Parameters
        -----------
        param :  str
            The parameter to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.

        Returns
        --------
        restart_result : list
            restart data in a list

        """
        locations = self._getRestartLocations()
        restart_result = []
        for i in range(0, len(locations)):
            if (self.simulatortype.lower() == gc.TMVOC or
                    self.simulatortype.lower() == gc.TOUGH3):
                fileReader = ResultTough3(self.simulatortype, locations[i],
                                          self.filetitle)
            else:
                fileReader = ResultReact(self.simulatortype, locations[i],
                                         self.filetitle)
            if i == 0:
                result_array = fileReader.get_timeseries_data(
                    param, grid_block_number)
                restart_result.append(result_array)
            else:
                result_array = fileReader.get_timeseries_data(
                    param, grid_block_number)
                result_array = result_array[1:]
                restart_result.append(result_array)
        restart_result = list(itertools.chain.from_iterable(restart_result))
        return restart_result

    def _plotRawWithExpt(self, param, grid_block_number, format_of_date,
                         restart=False, data_file='data_file.csv'):
        """ Line Plots of a parameter in the results file as a function of
        time if restart and experiments was performed in the simulation

        Parameters
        -----------
        param :  str
            The parameter to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        restart: boolean
            If restart was performed in the simulation or not
        data_file: str
            Data containing the experimental result in csv format

        Returns
        --------

        """
        expt_test = Experiment(self.expt[0], data_file)
        time_year_expt = expt_test.get_times()
        result_array_expt = expt_test.get_timeseries_data(param)
        parameters = t2Utilities()
        if restart is True:
            time_year = self._getRestartDataTime(format_of_date)
            result_array = self._getRestartDataElement(
                param, grid_block_number)
            time_year, result_array = parameters.remove_repetiting(
                time_year, result_array)
        else:
            fileReader = self._read_file()
            time_year = fileReader.convert_times(format_of_date)
            result_array = fileReader.get_timeseries_data(
                param, grid_block_number)
        fig, axs = plt.subplots(1, 1)
        if max(result_array_expt) <= 0:
            dy = 0.15 * abs(min(result_array_expt))
        else:
            dy = 0.15 * abs(max(result_array_expt))
        axs.plot(time_year, result_array,
                 marker=pc.CARET_SYMBOL, label=gc.SIMULATION)
        axs.errorbar(time_year_expt, result_array_expt,
                     yerr=dy, fmt=pc.COLOR_FORMAT, color=pc.RED_SYMBOL,
                     label=gc.EXPERIMENT)
        if format_of_date.lower() == pc.YEAR:
            axs.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
        elif format_of_date.lower() == pc.DAY:
            axs.set_xlabel(pc.X_LABEL_TIME_DAY, fontsize=12)
        elif format_of_date.lower() == pc.HOUR:
            axs.set_xlabel(pc.X_LABEL_TIME_HOUR, fontsize=12)
        elif format_of_date.lower() == pc.MINUTE:
            axs.set_xlabel(pc.X_LABEL_TIME_MIN, fontsize=12)
        axs.set_ylabel(parameters.param_label_full(param.upper()), fontsize=12)
        axs.spines[pc.BOTTOM].set_linewidth(1.5)
        axs.spines[pc.LEFT].set_linewidth(1.5)
        axs.spines[pc.TOP].set_linewidth(0)
        axs.spines[pc.RIGHT].set_linewidth(0)
        plt.legend(loc=pc.LOC_BEST)
        plt.setp(axs.get_xticklabels(), fontsize=12)
        plt.setp(axs.get_yticklabels(), fontsize=12)
        plt.tight_layout()
        plt.show()
        if restart is True:
            os.chdir(self.file_location)
            fig.savefig(param + ' ' + pc.VERSUS + ' ' + pc.TIME + ' '
                        + pc.RESTART + ' ' + pc.EXPERIMENT + pc.IMAGE_TYPE,
                        bbox_inches=pc.TIGHT_BBOX, dpi=600)
        else:
            os.chdir(self.file_location)
            fig.savefig(param + ' ' + pc.VERSUS + ' '
                        + pc.TIME + ' ' + pc.EXPERIMENT + pc.IMAGE_TYPE,
                        bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def plotParamWithTimeRestart(self, param, grid_block_number,
                                 format_of_date):
        """ Line Plots of a parameter in the results file as a function of
        time if restart was performed in the simulation

        Parameters
        -----------
        param :  str
            The parameter to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.
        format_of_date: str
            The format of the date; could be minute, hour, day or year

        Returns
        --------

        """
        if self.expt:
            try:
                with plt.style.context(pc.MY_STYLE):
                    self._plotRawWithExpt(param, grid_block_number,
                                          format_of_date, restart=True)
            except Exception:
                with plt.style.context(pc.CLASSIC):
                    self._plotRawWithExpt(param, grid_block_number,
                                          format_of_date, restart=True)
        else:
            try:
                with plt.style.context(pc.MY_STYLE):
                    self._plotRaw(param, grid_block_number,
                                  format_of_date, restart=True)
            except Exception:
                with plt.style.context(pc.CLASSIC):
                    self._plotRaw(param, grid_block_number,
                                  format_of_date, restart=True)

    def _plotRawLayer(self, direction_x_axis, direction_y_axis,
                      param, layer_num, time):
        """ Line Plots to show the evolution of a particular parameter across
        a layer at a particular time

        Parameters
        -----------
        direction_x_axis :  str
            The direction to be plotted on the x axis
        direction_y_axis :  str
            The direction to be plotted on the y axis
        param :  list[str]
            List of parameters
        layer_num :  int
            The layer in the model to be plotted
        time : int
            the time at which the plot is to be made

        Returns
        --------

        """
        fileReader = self._read_file()
        if len(param) == 1:
            y_data = fileReader.get_layer_data(direction_y_axis, layer_num,
                                               time, param[0])
            x_data = fileReader.get_unique_coord_data(direction_x_axis, time)
            fig, axs = plt.subplots(1, 1)
            axs.plot(x_data, y_data, marker=pc.CARET_SYMBOL)
            axs.set_xlabel(pc.DISTANCE_MSG + ' ' + direction_x_axis
                           + ' ' + pc.DIRECTION + ' ' + pc.OPEN_BRACKET
                           + pc.METER + pc.CLOSE_BRACKET)
            axs.set_ylabel(self.modifier.param_label_full(param[0].upper()))
            plt.tight_layout()
            plt.show()
            os.chdir(self.file_location)
            fig.savefig(param[0] + ' ' + pc.LAYER_FOR_LAYER
                        + ' ' + str(layer_num) + pc.IMAGE_TYPE,
                        bbox_inches=pc.TIGHT_BBOX, dpi=600)
        else:
            fig = plt.figure(figsize=(10, 8))
            plot_counter = 1
            start_point = 0
            x_data = fileReader.get_unique_coord_data(direction_x_axis, time)
            for _ in range(1, len(param) + 1):
                axs = plt.subplot(math.ceil(len(param) / 2) + 1, 2,
                                  plot_counter)
                y_data = fileReader.get_layer_data(direction_y_axis,
                                                   layer_num, time, param[start_point])
                axs.plot(x_data, y_data)
                axs.set_xlabel(pc.DISTANCE_MSG + ' '
                               + direction_x_axis + ' ' + pc.DIRECTION
                               + ' ' + pc.OPEN_BRACKET + pc.METER
                               + pc.CLOSE_BRACKET, fontsize=14)
                axs.set_ylabel(self.modifier.param_label_full(
                    param[start_point].upper()), fontsize=14)
                plot_counter = plot_counter + 1
                start_point = start_point + 1
                plt.setp(axs.get_xticklabels(), fontsize=14)
                plt.setp(axs.get_yticklabels(), fontsize=14)
            fig.tight_layout()
            plt.show()

    def plotParamWithParam(self, param1, param2, grid_block_number):
        """ Line Plot of two parameters in the results file

        Parameters
        -----------
        param1 :  str
            The parameter to be plotted on the x-axis
        param2 :  str
            The parameter to be plotted on the y-axis
        grid_block_number : int
            the grid block in which its parameter evolution is to be observed.

        Returns
        --------

        """
        try:
            with plt.style.context(pc.MY_STYLE):
                fileReader = self._read_file()
                result_array_x = fileReader.get_timeseries_data(
                    param1, grid_block_number)
                result_array_y = fileReader.get_timeseries_data(
                    param2, grid_block_number)
                fig, axs = plt.subplots(1, 1)
                axs.plot(result_array_x, result_array_y,
                         marker=pc.CARET_SYMBOL)
                axs.set_xlabel(self.modifier.param_label_full(param1.upper()))
                axs.set_ylabel(self.modifier.param_label_full(param2.upper()))
                plt.tight_layout()
                plt.show()
                fig.savefig(param2 + ' ' + pc.VERSUS + ' '
                            + param1 + pc.IMAGE_TYPE,
                            bbox_inches=pc.TIGHT_BBOX, dpi=600)
        except Exception:
            with plt.style.context(pc.CLASSIC):
                fileReader = self._read_file()
                result_array_x = fileReader.get_timeseries_data(
                    param1, grid_block_number)
                result_array_y = fileReader.get_timeseries_data(
                    param2, grid_block_number)
                fig, axs = plt.subplots(1, 1)
                axs.plot(result_array_x, result_array_y,
                         marker=pc.CARET_SYMBOL)
                axs.set_xlabel(self.modifier.param_label_full(param1.upper()))
                axs.set_ylabel(self.modifier.param_label_full(param2.upper()))
                plt.tight_layout()
                plt.show()
                fig.savefig(param2 + ' ' + pc.VERSUS + ' '
                            + param1 + pc.IMAGE_TYPE,
                            bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def plotParamWithLayer(self, direction_x_axis, direction_y_axis,
                           param, layer_num, time):
        """ Line Plots to show the evolution of a particular parameter across
        a layer at a particular time

        Parameters
        -----------
        direction_x_axis :  str
            The direction to be plotted on the x axis
        direction_y_axis :  str
            The direction to be plotted on the y axis
        param :  list[str]
            List of parameters
        layer_num :  int
            The layer in the model to be plotted
        time : int
            the time at which the plot is to be made

        Returns
        --------

        """
        try:
            with plt.style.context(pc.MY_STYLE):
                self._plotRawLayer(direction_x_axis, direction_y_axis,
                                   param, layer_num, time)
        except Exception:
            with plt.style.context(pc.CLASSIC):
                self._plotRawLayer(direction_x_axis, direction_y_axis,
                                   param, layer_num, time)

    def plot2D_one(self, direction_y_axis, direction_x_axis, param, timer):
        """ 2D mesh plot (ungridded) to show the evolution of a particular
        parameter across a the entire domain at a particular time

        Parameters
        -----------
        direction_x_axis :  str
            The direction to be plotted on the x axis
        direction_y_axis :  str
            The direction to be plotted on the y axis
        param :  str
            parameter to be plotted
        time : int
            the time at which the plot is to be made

        Returns
        --------

        """
        fileReader = self._read_file()
        fig, ax = plt.subplots(1, 1)
        X = fileReader.get_coord_data(direction_y_axis, timer)
        Z = fileReader.get_coord_data(direction_x_axis, timer)
        data = fileReader.get_element_data(timer, param)
        xi, yi = np.meshgrid(X, Z)
        data1 = griddata((X, Z), data, (xi, yi), method=pc.METHOD)
        cs2 = plt.contourf(xi, yi, data1, 800, cmap=pc.CMAP_COLOR,
                           vmin=min(data), vmax=max(data))
        vmin = min(data)
        if vmin < 1 or vmin > 1000:
            cbar = fig.colorbar(cs2, pad=0.01,
                                format=ticker.FuncFormatter(self.modifier.fmt))
        else:
            cbar = fig.colorbar(cs2, pad=0.01)
        cbar.ax.set_ylabel(self.modifier.param_label_full(param.upper()),
                           fontsize=12)
        ticklabs = cbar.ax.get_yticklabels()
        try:
            cbar.ax.set_yticklabels(ticklabs, fontsize=12)
        except ValueError:
            pass
        plt.xlabel(pc.HORIZONTAL_ADDED.capitalize() + ' '
                   + pc.DISTANCE.capitalize() + pc.OPEN_BRACKET + pc.METER
                   + pc.CLOSE_BRACKET, fontsize=12)
        plt.ylabel(pc.VERTICAL_ADDED.capitalize()
                   + ' ' + pc.DEPTH.capitalize() + pc.OPEN_BRACKET + pc.METER
                   + pc.CLOSE_BRACKET, fontsize=12)
        plt.tick_params(axis=pc.X, labelsize=12)
        plt.tick_params(axis=pc.Y, labelsize=12)
        plt.tight_layout()
        plt.show()
        fig.savefig('2D plain' + str(timer) + param + pc.IMAGE_TYPE,
                    bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def plot2D_withgrid(self, direction_y_axis, direction_x_axis,
                        param, timer):
        """ 2D mesh plot (gridded) to show the evolution of a particular
        parameter across a the entire domain at a particular time

        Parameters
        -----------
        direction_x_axis :  str
            The direction to be plotted on the x axis
        direction_y_axis :  str
            The direction to be plotted on the y axis
        param :  str
            parameter to be plotted
        time : int
            the time at which the plot is to be made

        Returns
        --------

        """
        fileReader = self._read_file()
        X = fileReader.get_coord_data(direction_y_axis, timer)
        Z = fileReader.get_coord_data(direction_x_axis, timer)
        df = pd.DataFrame(index=range(len(X)))
        df[pc.X_CAPS] = X
        df[pc.Z_CAPS] = Z
        Zvalues, Ztotal = self.modifier.get_grid_number(df, pc.Z_CAPS)
        Xvalues, Xtotal = self.modifier.get_grid_number(df, pc.X_CAPS)
        xi, yi = np.meshgrid(X, Z)
        orig_data = fileReader.get_element_data(timer, param)
        data = np.asarray(orig_data)
        data = data.reshape(Ztotal, Xtotal)
        if Ztotal > 5:
            height = 10
        else:
            height = 4
        fig, ax = plt.subplots(1, 1, figsize=(10, height))
        # data1 = griddata((X, Z), orig_data, (xi, yi), method=pc.METHOD)
        # extent = [min(X), max(X), min(Z), max(Z)]
        cs2 = plt.imshow(np.reshape(data, newshape=(Ztotal, Xtotal)),
                         cmap=pc.CMAP_COLOR, interpolation=pc.INTERPOLATION,
                         aspect=pc.ASPECT)
        ax = plt.gca()
        slicer_X = len(Xvalues)
        slicer_Z = len(Zvalues)
        if slicer_Z < 10:
            slicer_Z = 1
        if slicer_X <= 10:
            slicer_X = 1
        while slicer_X > 10 or slicer_Z > 10:
            if slicer_X > 10:
                slicer_X = np.round(slicer_X / 2)
            if slicer_Z > 10:
                slicer_Z = np.round(slicer_Z / 2)
        x_tick = np.arange(0, Xtotal, slicer_X)
        z_tick = np.arange(0, Ztotal, slicer_Z)
        Z_array = np.asarray(Z)
        Z_array = np.abs(Z_array)
        ax.set_xticks(x_tick)
        num_tick_x = len(x_tick)
        num_tick_z = len(z_tick)
        ax.set_yticks(z_tick)
        # Labels for major ticks
        tick_x = max(X) - min(X)
        tick_z = max(Z) - min(Z)
        x_tick = x_tick.astype(int)
        if max(X) < 1 or max(Z) < 1:
            magoosh = [Xvalues[i] for i in x_tick]
            magoosh = np.asarray(magoosh)
            ax.set_xticklabels(magoosh, fontsize=12)
            ax.set_yticklabels(np.round(self.modifier.crange(min(Z_array),
                                                             max(Z_array),
                                                             tick_z / (
                                                                 num_tick_z -
                                                                 1)), 4),
                               fontsize=12)
        else:
            ax.set_xticklabels(np.round(self.modifier.crange(
                min(X), max(X), tick_x / (num_tick_x - 1)), 2), fontsize=12)
            ax.set_yticklabels(np.round(self.modifier.crange(
                min(Z_array), max(Z_array), tick_z / (num_tick_z - 1)), 2),
                fontsize=12)
        # Minor ticks
        ax.set_xticks(np.arange(-.5, Xtotal, 1), minor=True)
        ax.set_yticks(np.arange(-.5, Ztotal, 1), minor=True)
        # Gridlines based on minor ticks
        ax.grid(which='minor', color='k', linestyle='-', linewidth=1)
        cbar = fig.colorbar(cs2, ax=ax, pad=0.3, orientation=pc.HORIZONTAL)
        cbar.ax.set_title(param, fontsize=12)
        cbar.ax.tick_params(labelsize=12)
        cbar.ax.locator_params(nbins=5)
        cbar.ax.ticklabel_format(useOffset=False, style=pc.PLAIN_STYLE)
        plt.xticks(rotation=90)
        plt.xlabel(pc.HORIZONTAL_ADDED.capitalize() + ' '
                   + pc.DISTANCE.capitalize() + ' ' + pc.OPEN_BRACKET
                   + pc.METER + pc.CLOSE_BRACKET, fontsize=12)
        plt.ylabel(pc.VERTICAL_ADDED.capitalize() + ' '
                   + pc.DEPTH.capitalize() + ' ' + pc.OPEN_BRACKET
                   + pc.METER + pc.CLOSE_BRACKET, fontsize=12)
        plt.tight_layout()
        plt.show()
        fig.savefig(grc.GRID_NAME.capitalize() + str(timer) + param
                    + pc.IMAGE_TYPE, bbox_inches=pc.TIGHT_BBOX, dpi=600)
