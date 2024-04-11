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

import math
import os


from pytoughreact.results.multi_result_tough_3 import MultiResultTough3
from pytoughreact.results.multi_result_tough_react import MultiResultReact
import matplotlib.pyplot as plt
import pytoughreact.constants.generalconstants as gc
import pytoughreact.constants.plotconstants as pc
import pytoughreact.constants.reactionconstants as rc

from pytoughreact.utilities.t2_utilities import T2Utilities


class PlotMultiFiles(object):
    def __init__(self, simulator_type, file_locations, file_titles, props,
                 **kwargs):
        """
        Class for processing multiple file results

        Parameters
        -----------
        file_locations :  list[str]
            specifies the location of the files on the syste
        file_titles : list[str]
            gives the title of the file e.g 'kdd.conc' or 'OUTPUT.csv'.
        simulator_type: str
            can either be toughreact, tmvoc or tough3
        prop : list[str]
            properties to be plotted

        **kwargs

        x_slice value : int
            value at which the plot should be sliced at the  x axis
        per_file : boolean
            if the plot should be made per file and not per property
        tile : str
            title of each of the plots


        Returns
        --------

        """
        assert isinstance(file_locations, list)
        assert isinstance(file_titles, list)
        assert isinstance(props, list)
        self.file_locations = file_locations
        self.file_titles = file_titles
        self.simulator_type = simulator_type
        self.props = props
        self.modifier = T2Utilities
        self.x_slice_value = kwargs.get(gc.X_SLICE_VALUE)
        self.per_file = kwargs.get(gc.PER_FILE)
        self.title = kwargs.get(gc.TITLE)

    def _validate_input(self):
        """ Validate Inputs
        """
        if self.simulator_type.lower() == gc.TOUGHREACT:
            multi_tough = MultiResultReact(self.simulator_type,
                                           self.file_locations,
                                           self.file_titles,
                                           self.props,
                                           x_slice_value=self.x_slice_value)
        elif self.simulator_type.lower() == gc.TMVOC:
            multi_tough = MultiResultTough3(self.simulator_type,
                                            self.file_locations,
                                            self.file_titles,
                                            self.props)
        else:
            print("Code only has capability for TOUGHREACT or TOUGH3 \
                  (by extension TMVOC)")
        return multi_tough

    def _plot_raw_single(self, data, legend):
        """ Plot of Single File

        Parameters
        -----------
        data :  pd.DataFrame
            data for plot
        legend :  list[str]
            List of legend values

        Returns
        --------
        """
        prop_index = 0
        fig, axs = plt.subplots(1, 1)
        for i in range(0, len(data.columns), 2):
            x_data = data.iloc[:, i]
            y_data = data.iloc[:, i + 1]
            axs.plot(x_data, y_data, marker=pc.CARET_SYMBOL)
            axs.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=14)
            axs.set_ylabel(self.props[prop_index], fontsize=14)
            axs.legend(legend, loc=pc.LOC_BEST)
            axs.ticklabel_format(useOffset=False)
        plt.setp(axs.get_xticklabels(), fontsize=14)
        plt.setp(axs.get_yticklabels(), fontsize=14)
        os.chdir(self.file_locations[0])
        plt.tight_layout()
        plt.show()
        fig.savefig(self.props[0] + ' ' + pc.DIFFERENT_FILES_TAG + ' ' +
                    pc.IMAGE_TYPE, bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def _plot_raw_multi(self, data, legend):
        """ Plot of Multi File

        Parameters
        -----------
        data :  pd.DataFrame
            data for plot
        legend :  list[str]
            List of legend values

        Returns
        --------
        """

        fig = plt.figure()
        plot_counter = 1
        start_point = 0
        prop_index = 0
        initial_length = len(self.props) * 2
        for number in range(1, len(self.props)):
            axs = plt.subplot(3, 2, plot_counter)
            legend_index = 0
            for i in range(start_point, initial_length, 2):
                x_data = data.iloc[:, i]
                y_data = data.iloc[:, i + 1]
                axs.plot(x_data, y_data, marker=pc.CARET_SYMBOL,
                         label=legend[legend_index])
                axs.set_xlabel(pc.X_LABEL_TIME_YEAR)
                axs.set_ylabel(self.props[prop_index])
                legend_index = legend_index + 1
            plot_counter = plot_counter + 1
            start_point = start_point + (len(self.props) * 2)
            initial_length = initial_length + (len(self.props) * 2)
            prop_index = prop_index + 1
        handles, labels = axs.get_legend_handles_labels()
        plt.setp(axs.get_xticklabels(), fontsize=14)
        plt.setp(axs.get_yticklabels(), fontsize=14)
        plt.figlegend(handles, labels, loc=pc.LOC_LOWER_CENTER, ncol=5,
                      labelspacing=0.)
        plt.show()
        fig.savefig(self.props[0] + ' ' + pc.DIFFERENT_FILES_TAG + ' ' +
                    pc.IMAGE_TYPE, bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def _set_tough_y_label(self, value):
        """ Convert the value in tough results to understandable values

        Parameters
        -----------
        value :  str
            value to be converted (must be present in TOUGH data output)

        Returns
        --------
        value :  str
            converted value

        """
        if rc.TOBERMORITE_TOUGHREACT in value:
            value = rc.TOBERMORITE_CONVERSION
        elif rc.MONOSULFOALUMINATE_TOUGHREACT in value:
            value = rc.MONOSULFOALUMINATE_CONVERSION
        elif rc.KATOITE_TOUGHREACT in value:
            value = rc.KATOITE_CONVERSION
        if rc.PH_TOUGHREACT not in value:
            value = value.capitalize()
        if rc.C3FH6_TOUGHREACT in value:
            value = rc.C3FH6_CONVERSION
        if self.simulator_type == gc.TMVOC:
            value = value.upper()
        return value

    def _plot_raw_multi_file(self, data, legend, format_of_date):
        """ Plot of Multi File

        Parameters
        -----------
        data :  pd.DataFrame
            data for plot
        legend :  list[str]
            List of legend values
        format_of_date: str
            The format of the date; could be minute, hour, day or year

        Returns
        --------

        """
        fig = plt.figure(figsize=(10, 10))
        plot_counter = 1
        start_point = 0
        prop_index = 0
        markers = pc.ALL_MARKERS
        for number in range(1, len(self.props) + 1):
            if number == 4:
                pass
            axs = plt.subplot(math.ceil(len(self.props) / 2) + 1, 2,
                              plot_counter)
            legend_index = 0
            for i in range(start_point, len(data.columns),
                           (len(self.props) * 2)):
                x_data = data.iloc[:, i]
                y_data = data.iloc[:, i + 1]
                axs.plot(x_data, y_data, marker=markers[legend_index],
                         label=legend[legend_index])
                axs.set_xlabel('Time ' + '(' + format_of_date + ')',
                               fontsize=14)
                axs.set_ylabel(self._set_tough_y_label(self.props[prop_index]),
                               fontsize=14)
                axs.ticklabel_format(useOffset=False)
                legend_index = legend_index + 1
            plot_counter = plot_counter + 1
            start_point = start_point + 2
            prop_index = prop_index + 1
            plt.setp(axs.get_xticklabels(), fontsize=14)
            plt.setp(axs.get_yticklabels(), fontsize=14)
        handles, labels = axs.get_legend_handles_labels()
        fig.tight_layout()
        if len(self.props) > 3:
            plt.figlegend(handles, labels, loc=pc.LOC_LOWER_CENTER, ncol=4,
                          labelspacing=0.)
        else:
            plt.figlegend(handles, labels, loc=pc.LOC_LOWER_CENTER, ncol=4,
                          labelspacing=0.)
        plt.show()
        os.chdir(self.file_locations[0])
        fig.savefig(self.props[0] + ' ' + pc.DIFFERENT_FILES_TAG + ' ' +
                    pc.IMAGE_TYPE, bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def _plot_raw_multi_file_panel(self, data, panels, format_of_date):
        """ Plot of Multi File Per Panel

        Parameters
        -----------
        data :  pd.DataFrame
            data for plot
        panels :  int
            Number of panels
        format_of_date: str
            The format of the date; could be minute, hour, day or year

        Returns
        --------

        """
        fig = plt.figure(figsize=(10, 8))
        start_point = 0
        # markers = pc.ALL_MARKERS
        fig, axs = plt.subplots(2, 2)
        number = 0
        length_of_prop = len(list(panels[number].values())[0][0])
        for i in range(0, len(panels)):
            x_data = data.iloc[:, start_point]
            y_data = data.iloc[:, start_point + 1:start_point + length_of_prop
                               + 1]
            number += 1
            start_point = start_point + length_of_prop + 1
            try:
                length_of_prop = len(list(panels[number].values())[0][0])
            except IndexError:
                pass
            if i == 0:
                # marker = itertools.cycle((',', '+', '.', 'o', '*'))
                axsa = axs[0, 0]
                axsa.plot(x_data, y_data)
                y_label = list(panels[0].values())[0][2][0]
                axsa.set_xlabel('Time ' + format_of_date, fontsize=12)
                axsa.set_ylabel(y_label, fontsize=12)
                axsa.ticklabel_format(useOffset=False)
                axsa.legend(list(panels[0].values())[0][1], fontsize=12,
                            loc=pc.LOC_BEST, shadow=True, fancybox=True)
            elif i == 1:
                axsa = axs[0, 1]
                axsa.plot(x_data, y_data)
                y_label = list(panels[1].values())[0][2][0]
                axsa.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
                axsa.set_ylabel(y_label, fontsize=12)
                axsa.ticklabel_format(useOffset=False)
                axsa.legend(list(panels[1].values())[0][1], fontsize=12,
                            loc=pc.LOC_BEST, shadow=True, fancybox=True)
            elif i == 2:
                axsa = axs[1, 0]
                axsa.plot(x_data, y_data)
                y_label = list(panels[2].values())[0][2][0]
                axsa.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
                axsa.set_ylabel(y_label, fontsize=12)
                axsa.ticklabel_format(useOffset=False)
                axsa.legend(list(panels[2].values())[0][1], fontsize=12,
                            loc=pc.LOC_BEST, shadow=True, fancybox=True)
            elif i == 3:
                axsa = axs[1, 1]
                axsa.plot(x_data, y_data)
                y_label = list(panels[3].values())[0][2][0]
                axsa.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=12)
                axsa.set_ylabel(y_label, fontsize=12)
                axsa.ticklabel_format(useOffset=False)
                axsa.legend(list(panels[3].values())[0][1], fontsize=10,
                            loc=pc.LOC_BEST, shadow=True, fancybox=True)
        fig.tight_layout()
        plt.show()
        fig.savefig(list(panels[0].values())[0][0][0] +
                    pc.MULTI_PLOTS_PER_PANEL + pc.IMAGE_TYPE,
                    bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def _plot_raw_multi_file_per_file(self, data, legend):
        """ Plot of Multi File Per File

        Parameters
        -----------
        data :  pd.DataFrame
            data for plot
        legend :  list[str]
            List of legend values

        Returns
        --------

        """
        fig = plt.figure(figsize=(10, 8))
        plot_counter = 1
        start_point = 0
        prop_index = 0
        markers = pc.ALL_MARKERS
        for number in range(1, len(self.props) + 1):
            axs = plt.subplot(3, 2, plot_counter)
            legend_index = 0
            for i in range(start_point, len(data.columns), (len(self.props)
                                                            * 2)):
                x_data = data.iloc[:, i]
                y_data = data.iloc[:, i + 1]
                if gc.POROSITY in data.columns[i]:
                    axs.plot(x_data, y_data, marker=markers[legend_index],
                             label=self._set_tough_y_label(legend[legend_index]))
                    axs.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=14)
                    if self.simulator_type.lower() == gc.TMVOC:
                        axs.set_ylabel(
                            self.modifier.param_label_full(
                                self.props[prop_index]), fontsize=14)
                    else:
                        axs.set_ylabel(rc.CHANGE_IN_VOLUME_FRACTION,
                                       fontsize=14)
                else:
                    axs.plot(x_data, y_data, marker=markers[legend_index],
                             label=self._set_tough_y_label(legend[legend_index]))
                    axs.set_xlabel(pc.X_LABEL_TIME_YEAR, fontsize=14)
                    if self.simulator_type.lower() == gc.TMVOC:
                        param_value = self.modifier.param_label_full(
                            self.props[prop_index].upper())
                        axs.set_ylabel(param_value, fontsize=14)
                    else:
                        axs.set_ylabel(rc.CHANGE_IN_VOLUME_FRACTION,
                                       fontsize=14)
                axs.ticklabel_format(useOffset=False)
                plt.setp(axs.get_xticklabels(), fontsize=14)
                plt.setp(axs.get_yticklabels(), fontsize=14)
                legend_index = legend_index + 1
            # axs.set_title(self.title[prop_index], fontsize='14')
            axs.set_title(self.props[prop_index], fontsize='14')
            plot_counter = plot_counter + 1
            start_point = start_point + 2
            prop_index = prop_index + 1
        handles, labels = axs.get_legend_handles_labels()
        # handles2, labels2 = ax2s.get_legend_handles_labels()
        # handles.append(handles2[0])
        # labels.append(labels2[0])
        plt.figlegend(handles, labels, loc=pc.LOC_LOWER_CENTER, ncol=4,
                      labelspacing=0.)
        fig.tight_layout()
        plt.show()
        os.chdir(self.file_locations[0])
        fig.savefig(self.props[0] + ' ' + pc.DIFFERENT_FILES_TAG + ' '
                    + pc.IMAGE_TYPE, bbox_inches=pc.TIGHT_BBOX, dpi=600)

    def multi_file_single_plot(self, grid_block_number, legend):
        """ Plot of  Multiple Files with a single plot

        Parameters
        -----------
        grid_block_number :  int
            The grid block number to be plotted
        legend :  list[str]
            List of legend values

        Returns
        --------

        """
        multi_tough = self._validate_input()
        data = multi_tough.retrieve_data_multi_timeseries(grid_block_number)
        try:
            with plt.style.context(pc.MY_STYLE):
                self._plot_raw_single(data, legend)
        except Exception:
            with plt.style.context(pc.CLASSIC):
                self._plot_raw_single(data, legend)

    def _plot_multi_element_multi_file_per_file(self, grid_block_number, legend,
                                                format_of_date):
        """ Plot of Multi Elements and Multiple Files for File only

        Parameters
        -----------
        grid_block_number :  int
            The grid block number to be plotted
        legend :  list[str]
            List of legend values
        format_of_date: str
            The format of the date; could be minute, hour, day or year

        Returns
        --------

        """
        multi_tough = self._validate_input()
        data = multi_tough.get_multi_element_data(grid_block_number,
                                                  format_of_date)
        try:
            with plt.style.context(pc.MY_STYLE):
                self._plot_raw_multi_file_per_file(data, legend)
        except Exception:
            with plt.style.context(pc.CLASSIC):
                self._plot_raw_multi_file_per_file(data, legend)

    def _plot_multi_element_multi_file_per_prop(self, grid_block_number, legend,
                                                format_of_date):
        """ Plot of Multi Elements and Multiple Files for Property only

        Parameters
        -----------
        grid_block_number :  int
            The grid block number to be plotted
        legend :  list[str]
            List of legend values
        format_of_date: str
            The format of the date; could be minute, hour, day or year

        Returns
        --------

        """
        multi_tough = self._validate_input()
        data = multi_tough.get_multi_element_data(grid_block_number,
                                                  format_of_date)
        try:
            with plt.style.context(pc.MY_STYLE):
                self._plot_raw_multi_file(data, legend, format_of_date)
        except Exception:
            with plt.style.context(pc.CLASSIC):
                self._plot_raw_multi_file(data, legend, format_of_date)

    def plot_multi_element_multi_file(self, grid_block_number, legend,
                                      format_of_date, plot_kind=pc.PROPERTY):
        """ Plot of Multi Elements and Multiple Files

        Parameters
        -----------
        grid_block_number :  int
            The grid block number to be plotted
        legend :  list[str]
            List of legend values
        format_of_date: str
            The format of the date; could be minute, hour, day or year
        plot_kind: str
            The kind of plot to be used; could be 'property' or 'file'

        Returns
        --------

        """
        if plot_kind.lower() == pc.PROPERTY:
            self._plot_multi_element_multi_file_per_prop(grid_block_number, legend,
                                                         format_of_date)
        elif plot_kind.lower() == pc.FILE:
            self._plot_multi_element_multi_file_per_file(grid_block_number, legend,
                                                         format_of_date)
        else:
            print('Plot kind can either be property or file')

    def plot_multi_per_panel(self, grid_block_number, panels,
                             format_of_date=pc.DAY):
        """ Plot of Multi Properties Per Panel

        Parameters
        -----------
        grid_block_number :  int
            The grid block number to be plotted
        panels :  int
            Number of panels
        format_of_date: str
            The format of the date; could be minute, hour, day or year

        Returns
        --------

        """
        multi_tough = self._validate_input()
        data = multi_tough.get_multi_element_data_per_panel(grid_block_number,
                                                            panels, format_of_date)
        if self.x_slice_value is not None:
            stringo = panels[0]['panel1'][0][0] + 'time00'
            data = data[data[stringo] <= self.x_slice_value]
        try:
            with plt.style.context(pc.MY_STYLE):
                self._plot_raw_multi_file_panel(data, panels, format_of_date)
        except Exception:
            with plt.style.context(pc.CLASSIC):
                self._plot_raw_multi_file_panel(data, panels, format_of_date)

    def plot_multi_file_distance(self, direction_x, direction_y, time, layer_num,
                                 legend):
        """ Plot of Parameter with Distance for Multiple Files

        Parameters
        -----------
        direction_x :  str
            The direction to be plotted on the x axis
        direction_y :  str
            The direction to be plotted on the y axis
        legend :  list[str]
            List of legend values
        layer_num :  int
            The layer in the model to be plotted
        time : int
            the time at which the plot is to be made

        Returns
        --------

        """
        multi_tough = self._validate_input()
        data = multi_tough.get_multi_file_distance(direction_x, direction_y, time,
                                                   layer_num)
        if self.per_file is True:
            try:
                with plt.style.context(pc.MY_STYLE):
                    self._plot_raw_multi_file_per_file(data, legend)
            except Exception:
                with plt.style.context(pc.CLASSIC):
                    self._plot_raw_multi_file_per_file(data, legend)
        else:
            try:
                with plt.style.context(pc.MY_STYLE):
                    self._plot_raw_multi_file(data, legend)
            except Exception:
                with plt.style.context(pc.CLASSIC):
                    self._plot_raw_multi_file(data, legend)
