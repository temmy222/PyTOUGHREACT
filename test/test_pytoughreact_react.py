import os
import sys
from mulgrids import mulgrid
from pytoughreact.chemical.kinetic_properties import pHDependenceType2, Dissolution, Precipitation
from pytoughreact.chemical.mineral_description import Mineral
from pytoughreact.chemical.chemical_composition import PrimarySpecies, WaterComp, Water, ReactGas
from pytoughreact.chemical.mineral_composition import MineralComp
from pytoughreact.chemical.mineral_zone import MineralZone
from pytoughreact.chemical.perm_poro_zone import PermPoro, PermPoroZone
from pytoughreact.writers.react_writing import t2react
from pytoughreact.writers.solute_writing import t2solute
from pytoughreact.writers.chemical_writing import t2chemical
from pytoughreact.wrapper.reactzone import t2zone
from pytoughreact.wrapper.reactgrid import t2reactgrid
from pytoughreact.results.t2result import t2result
from t2data import rocktype


class ReactTestCase():
    def get_specific_mineral(self, mineral_name):

        calcite_ph = pHDependenceType2(5.0119e-01, 14.4, 1, 'h+', 1.0)
        dissolution_calcite = Dissolution(1.5488e-06, 2, 1, 1, 23.5, 0, 0, 0)
        dissolution_calcite.pHDependence = [calcite_ph]
        precipitation_calcite = Precipitation(1.5488e-06, 0, 1, 1, 23.5, 0, 0, 0, 1.0E-5, 0, 0, 0, 0)
        calcite = Mineral('Calcite', 1, 3, 0, 0)
        calcite.dissolution = [dissolution_calcite]
        calcite.precipitation = [precipitation_calcite]

        dissolution_portlandite = Dissolution(2.18e-08, 0, 1, 1, 74.9)
        precipitation_portlandite = Precipitation(2.18e-08, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        portlandite = Mineral('Portlandite', 1, 3, 0, 0)
        portlandite.dissolution = [dissolution_portlandite]
        portlandite.precipitation = [precipitation_portlandite]

        dissolution_c3fh6 = Dissolution(1.60e-018, 0, 1, 1, 0.0)
        precipitation_c3fh6 = Precipitation(1.60e-018, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        c3fh6 = Mineral('C3FH6', 1, 3, 0, 0)
        c3fh6.dissolution = [dissolution_c3fh6]
        c3fh6.precipitation = [precipitation_c3fh6]

        dissolution_tobermorite = Dissolution(1.0e-012, 0, 1, 1, 0.0)
        precipitation_tobermorite = Precipitation(1.0e-012, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        tobermorite = Mineral('Tobermorite(11A)', 1, 3, 0, 0)
        tobermorite.dissolution = [dissolution_tobermorite]
        tobermorite.precipitation = [precipitation_tobermorite]

        dissolution_ettringite = Dissolution(1.2589e-012, 0, 1, 1, 0.0)
        precipitation_ettringite = Precipitation(1.2589e-012, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        ettringite = Mineral('Ettringite', 1, 3, 0, 0)
        ettringite.dissolution = [dissolution_ettringite]
        ettringite.precipitation = [precipitation_ettringite]

        dissolution_katoite = Dissolution(1.2589e-012, 0, 1, 1, 0.0)
        precipitation_katoite = Precipitation(1.2589e-012, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        katoite = Mineral('KatoiteSi1', 1, 3, 0, 0)
        katoite.dissolution = [dissolution_katoite]
        katoite.precipitation = [precipitation_katoite]

        dissolution_hydrotalcite = Dissolution(1.2589e-012, 0, 1, 1, 0.0)
        precipitation_hydrotalcite = Precipitation(1.2589e-012, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        hydrotalcite = Mineral('Hydrotalcite', 1, 3, 0, 0)
        hydrotalcite.dissolution = [dissolution_hydrotalcite]
        hydrotalcite.precipitation = [precipitation_hydrotalcite]

        dissolution_friedel_salt = Dissolution(1.2589e-012, 0, 1, 1, 0.0)
        precipitation_friedel_salt = Precipitation(1.2589e-012, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        friedel_salt = Mineral('Friedel_Salt', 1, 3, 0, 0)
        friedel_salt.dissolution = [dissolution_friedel_salt]
        friedel_salt.precipitation = [precipitation_friedel_salt]

        brucite_ph = pHDependenceType2(1.8621e-05, 59, 1, 'h+', 0.5)
        dissolution_brucite = Dissolution(5.7543e-09, 2, 1, 1, 42, 0, 0, 0)
        dissolution_brucite.pHDependence = [brucite_ph]
        precipitation_brucite = Precipitation(5.7543e-09, 0, 1, 1, 42, 0, 0, 0, 1.0E-5, 0, 0, 0, 0)
        brucite = Mineral('Brucite', 1, 3, 0, 0)
        brucite.dissolution = [dissolution_brucite]
        brucite.precipitation = [precipitation_brucite]

        dolomite_ph = pHDependenceType2(6.4565e-04, 36.1, 1, 'h+', 0.5)
        dissolution_dolomite = Dissolution(2.9512e-08, 2, 1, 1, 52.2, 0, 0, 0)
        dissolution_dolomite.pHDependence = [dolomite_ph]
        precipitation_dolomite = Precipitation(2.9512e-08, 0, 1, 1, 52.2, 0, 0, 0, 1.0E-5, 0, 0, 0, 0)
        dolomite = Mineral('Dolomite', 1, 3, 0, 0)
        dolomite.dissolution = [dissolution_dolomite]
        dolomite.precipitation = [precipitation_dolomite]

        dissolution_chalcedony = Dissolution(1.6982e-013, 0, 1, 1, 0.0)
        precipitation_chalcedony = Precipitation(1.6982e-013, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        chalcedony = Mineral('Chalcedony', 1, 3, 0, 0)
        chalcedony.dissolution = [dissolution_chalcedony]
        chalcedony.precipitation = [precipitation_chalcedony]

        dissolution_thaumasite = Dissolution(1.0e-012, 0, 1, 1, 0.0)
        precipitation_thaumasite = Precipitation(1.0e-012, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        thaumasite = Mineral('Thaumasite', 1, 3, 0, 0)
        thaumasite.dissolution = [dissolution_thaumasite]
        thaumasite.precipitation = [precipitation_thaumasite]

        dissolution_gypsum = Dissolution(1.6216e-3, 0, 1, 1, 0.0)
        precipitation_gypsum = Precipitation(1.6216e-3, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        gypsum = Mineral('Gypsum', 1, 3, 0, 0)
        gypsum.dissolution = [dissolution_gypsum]
        gypsum.precipitation = [precipitation_gypsum]

        dissolution_jennite = Dissolution(1.0e-012, 0, 1, 1, 0.0)
        precipitation_jennite = Precipitation(1.0e-012, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        jennite = Mineral('Jennite', 1, 3, 0, 0)
        jennite.dissolution = [dissolution_jennite]
        jennite.precipitation = [precipitation_jennite]

        sepiolite_ph = pHDependenceType2(1.9953e-06, 75.5, 1, 'h+', 0.8)
        dissolution_sepiolite = Dissolution(3.9811e-013, 2, 1, 1, 56.6, 0, 0, 0)
        dissolution_sepiolite.pHDependence = [sepiolite_ph]
        precipitation_sepiolite = Precipitation(3.9811e-013, 0, 1, 1, 56.6, 0, 0, 0, 1.0E-5, 0, 0, 0, 0)
        sepiolite = Mineral('Sepiolite', 1, 3, 0, 0)
        sepiolite.dissolution = [dissolution_sepiolite]
        sepiolite.precipitation = [precipitation_sepiolite]

        dissolution_monosulfoaluminate = Dissolution(5.8880E-12, 0, 1, 1, 0.0)
        precipitation_monosulfoaluminate = Precipitation(5.8880E-12, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        monosulfoaluminate = Mineral('Monosulfoaluminate', 1, 3, 0, 0)
        monosulfoaluminate.dissolution = [dissolution_monosulfoaluminate]
        monosulfoaluminate.precipitation = [precipitation_monosulfoaluminate]

        dissolution_csh = Dissolution(1.0e-012, 0, 1, 1, 0.0)
        precipitation_csh = Precipitation(1.0e-012, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        csh = Mineral('CSH(1.6)', 1, 3, 0, 0)
        csh.dissolution = [dissolution_csh]
        csh.precipitation = [precipitation_csh]

        dissolution_quartz = Dissolution(1.0233e-14, 0, 1, 1, 87.7, 0, 0, 0)
        quartz = Mineral('Quartz(alpha)', 1, 1, 0, 0)
        quartz.dissolution = [dissolution_quartz]

        microcline_ph = pHDependenceType2(8.7096e-11, 51.7, 1, 'h+', 0.5)
        microcline_ph2 = pHDependenceType2(6.3096e-22, 94.1, 1, 'h+', -0.823)
        dissolution_microcline = Dissolution(3.8905e-13, 2, 1, 1, 38, 0, 0, 0)
        dissolution_microcline.pHDependence = [microcline_ph, microcline_ph2]
        precipitation_microcline = Precipitation(3.8905e-13, 0, 1, 1, 38, 0, 0, 0, 1.0E-6, 0, 0, 0, 0)
        microcline = Mineral('Microcline', 1, 3, 0, 0)
        microcline.dissolution = [dissolution_microcline]
        microcline.precipitation = [precipitation_microcline]

        albite_ph = pHDependenceType2(2.1380e-11, 65, 1, 'h+', 0.457)
        dissolution_albite = Dissolution(1.4454e-13, 2, 1, 1, 69.8, 0, 0, 0)
        dissolution_albite.pHDependence = [albite_ph]
        precipitation_albite = Precipitation(1.4454e-13, 0, 1, 1, 69.8, 0, 0, 0, 1.0E-6, 0, 0, 0, 0)
        albite = Mineral('Albite(low)', 1, 3, 0, 0)
        albite.dissolution = [dissolution_albite]
        albite.precipitation = [precipitation_albite]

        muscovite_ph = pHDependenceType2(1.4125e-12, 22, 1, 'h+', 0.37)
        muscovite_ph2 = pHDependenceType2(2.8184e-15, 22, 1, 'h+', -0.22)
        dissolution_muscovite = Dissolution(2.8184e-13, 2, 1, 1, 22, 0, 0, 0)
        dissolution_muscovite.pHDependence = [muscovite_ph, muscovite_ph2]
        precipitation_muscovite = Precipitation(2.8184e-13, 0, 1, 1, 22, 0, 0, 0, 1.0E-6, 0, 0, 0, 0)
        muscovite = Mineral('Muscovite(ordered)', 1, 3, 0, 0)
        muscovite.dissolution = [dissolution_muscovite]
        muscovite.precipitation = [precipitation_muscovite]

        chlorite_ph = pHDependenceType2(7.7624e-12, 88.0, 1, 'h+', 0.5)
        dissolution_chlorite = Dissolution(3.0200e-13, 2, 1, 0.380, 88, 0, 0, 0)
        dissolution_chlorite.pHDependence = [chlorite_ph]
        precipitation_chlorite = Precipitation(3.0200e-13, 0, 1, 0.380, 88, 0, 0, 0, 1.0E-6, 0, 0, 0, 0)
        chlorite = Mineral('Chlorite(Cca-2)', 1, 3, 0, 0)
        chlorite.dissolution = [dissolution_chlorite]
        chlorite.precipitation = [precipitation_chlorite]

        dissolution_anhydrite = Dissolution(6.4565e-04, 0, 1, 1, 14.3, 0, 0, 0)
        precipitation_anhydrite = Precipitation(6.4565e-04, 0, 1, 1, 14.3, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        anhydrite = Mineral('Anhydrite', 1, 3, 0, 0)
        anhydrite.dissolution = [dissolution_anhydrite]
        anhydrite.precipitation = [precipitation_anhydrite]

        dissolution_halite = Dissolution(6.1659e-1, 0, 1, 1, 7.4, 0, 0, 0)
        precipitation_halite = Precipitation(6.1659e-1, 0, 1, 1, 7.4, 0, 0, 0, 1e-6, 0, 0, 0, 0)
        halite = Mineral('Halite', 1, 3, 0, 0)
        halite.dissolution = [dissolution_halite]
        halite.precipitation = [precipitation_halite]
        default_minerals = {
            'csh': csh,
            'quartz': quartz,
            'microcline': microcline,
            'muscovite': muscovite,
            'albite': albite,
            'chlorite': chlorite,
            'anhydrite': anhydrite,
            'calcite': calcite,
            'portlandite': portlandite,
            'c3fh6': c3fh6,
            'tobermorite': tobermorite,
            'ettringite': ettringite,
            'katoite': katoite,
            'hydrotalcite': hydrotalcite,
            'friedel_salt': friedel_salt,
            'brucite': brucite,
            'dolomite': dolomite,
            'chalcedony': chalcedony,
            'thaumasite': thaumasite,
            'gypsum': gypsum,
            'jennite': jennite,
            'sepiolite': sepiolite,
            'monosulfoaluminate': monosulfoaluminate,
            'halite': halite}
        return default_minerals[mineral_name.lower()]

    def get_kinetics_minerals(self, mineral_list):
        output = []
        for mineral in mineral_list:
            output.append(self.get_specific_mineral(mineral.lower()))
        return output

    def set_up_write(self):
        second = 1
        minute = 60 * second
        hour = 60 * minute
        day = 24 * hour
        year = 365. * day
        year = float(year)
        # simtime = 1 * year
        # --------------------------------------------FLOW.INP-----------------------------------------------------------------

        length = 0.1
        nblks = 1
        dx = [length / nblks] * nblks
        dy = [0.5]
        dz = [0.5] * 1
        geo = mulgrid().rectangular(dx, dy, dz)
        geo.write('geom.dat')

        react = t2react()
        react.title = 'Reaction example'

        react.multi = {'num_components': 1, 'num_equations': 1, 'num_phases': 2,
                       'num_secondary_parameters': 6}

        react.grid = t2reactgrid().fromgeo(geo)

        react.parameter.update({'print_level': 4,
                                'max_timesteps': 9999,
                                'tstop': 8640,
                                'const_timestep': 10.,
                                'print_interval': 1,
                                'gravity': 9.81,
                                'relative_error': 1e-5,
                                'phase_index': 2,
                                'default_incons': [1.013e5, 25]})

        sand = rocktype('ROCK1', 0, 2600, 0.1, [6.51e-12, 6.51e-12, 6.51e-12], 0.0, 952.9)

        react.grid.delete_rocktype('dfalt')
        react.grid.add_rocktype(sand)

        for blk in react.grid.blocklist[0:]:
            blk.rocktype = react.grid.rocktype[sand.name]

        zone1 = t2zone('zone1')

        react.grid.add_zone(zone1)

        for blk in react.grid.blocklist[0:]:
            blk.zone = react.grid.zone[zone1.name]

        react.start = True

        react.write('flow.inp')

        # ____________________________________CHEMICAL.INP________________________________________________________________
        h2o = PrimarySpecies('h2o', 0)
        h = PrimarySpecies('h+', 0)
        na = PrimarySpecies('na+', 0)
        cl = PrimarySpecies('cl-', 0)
        hco3 = PrimarySpecies('hco3-', 0)
        ca = PrimarySpecies('ca+2', 0)
        so4 = PrimarySpecies('so4-2', 0)
        mg = PrimarySpecies('mg+2', 0)
        h4sio4 = PrimarySpecies('h4sio4', 0)
        al = PrimarySpecies('al+3', 0)
        fe = PrimarySpecies('fe+2', 0)
        hs = PrimarySpecies('hs-', 0)

        all_species = [h2o, h, na, cl, hco3, ca, so4, mg, h4sio4, al, fe, hs]

        h2o_comp1 = WaterComp(h2o, 1, 1.0000E+00, 1.000000E+00)
        h_comp1 = WaterComp(h, 1, 1E-7, 1E-7)
        na_comp1 = WaterComp(na, 1, 1E-10, 2.93E-2)
        cl_comp1 = WaterComp(cl, 1, 1E-10, 1.08E-3)
        hco3_comp1 = WaterComp(hco3, 1, 1E-10, 2.21E-08)
        ca_comp1 = WaterComp(ca, 1, 1E-10, 5.9E-03)
        so4_comp1 = WaterComp(so4, 1, 1E-10, 6.94E-3)
        mg_comp1 = WaterComp(mg, 1, 1E-10, 2.54E-8)
        h4sio4_comp1 = WaterComp(h4sio4, 1, 1E-10, 1E-10)
        al_comp1 = WaterComp(al, 1, 1E-10, 9.96E-5)
        fe_comp1 = WaterComp(fe, 1, 1E-10, 9.7E-9)
        hs_comp1 = WaterComp(hs, 1, 1E-10, 1E-10)

        initial_water_zone1 = Water([h2o_comp1, h_comp1, na_comp1, cl_comp1, hco3_comp1, ca_comp1, so4_comp1, mg_comp1,
                                     h4sio4_comp1, al_comp1, fe_comp1, hs_comp1], 25, 200)

        mineral_list = ['c3fh6', 'tobermorite', 'calcite', 'csh', 'portlandite', 'ettringite', 'katoite',
                        'hydrotalcite']
        all_minerals = self.get_kinetics_minerals(mineral_list)

        c3fh6_zone1 = MineralComp(self.get_specific_mineral(mineral_list[0]), 0.1, 0, 0.0E-00, 20000.0, 0)
        tobermorite_zone1 = MineralComp(self.get_specific_mineral(mineral_list[1]), 0.05, 0, 0.0E-00, 20000.0, 0)
        calcite_zone1 = MineralComp(self.get_specific_mineral(mineral_list[2]), 0.4, 1, 0.0E-00, 260.0, 0)
        csh_zone1 = MineralComp(self.get_specific_mineral(mineral_list[3]), 0.1, 1, 0.0E-00, 20000.0, 0)
        portlandite_zone1 = MineralComp(self.get_specific_mineral(mineral_list[4]), 0.1, 1, 0.0E-00, 1540.0, 0)
        ettringite_zone1 = MineralComp(self.get_specific_mineral(mineral_list[5]), 0.1, 1, 0.0E-00, 20000.0, 0)
        katoite_zone1 = MineralComp(self.get_specific_mineral(mineral_list[6]), 0.1, 1, 0.0E-00, 570.0, 0)
        hydrotalcite_zone1 = MineralComp(self.get_specific_mineral(mineral_list[7]), 0.05, 1, 0.0E-00, 1000.0, 0)

        initial_co2 = ReactGas('co2(g)', 0, 1.1)
        # ijgas = [[initial_co2], []]

        permporo = PermPoro(1, 0, 0)
        permporozone = PermPoroZone([permporo])

        zone1.water = [[initial_water_zone1], []]
        zone1.gas = [[initial_co2], []]
        mineral_zone1 = MineralZone([c3fh6_zone1, tobermorite_zone1, calcite_zone1, csh_zone1, portlandite_zone1,
                                     ettringite_zone1,
                                     katoite_zone1, hydrotalcite_zone1])
        zone1.mineral_zone = mineral_zone1
        zone1.permporo = permporozone

        writeChemical = t2chemical(t2reactgrid=react.grid)
        writeChemical.minerals = all_minerals
        writeChemical.title = 'Automating Tough react'
        writeChemical.primary_aqueous = all_species
        writeChemical.gases = initial_co2
        writeChemical.write()

        # ____________________________________SOLUTE.INP________________________________________________________________
        writeSolute = t2solute(t2chemical=writeChemical)
        writeSolute.nodes_to_write = [0]
        # masa = writeSolute.getgrid_info()
        writeSolute.write()
        # react.run(writeSolute, simulator='treacteos1.exe')
        return writeSolute

    def set_up_read(self):
        react = t2react()
        react.read('flow.inp')
        writeChemical = t2chemical(t2reactgrid=react.grid)
        writeSolute = t2solute(t2chemical=writeChemical)

        writeChemical.read('chemical.inp')
        writeSolute.read('solute.inp')

        return writeSolute


def test_write_react():
    test_case = ReactTestCase()
    write_output = test_case.set_up_write()
    result = write_output.status
    assert result == 'successful'


def test_read_react():
    test_case = ReactTestCase()
    write_output = test_case.set_up_read()
    result = write_output.status
    assert result == 'successful'


def test_result_first():
    FILE_PATH = os.path.abspath(os.curdir)
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    results = t2result('toughreact', 'kdd_conc.tec', FILE_PATH)
    time = results.get_times()
    parameter_result = results.get_time_series_data('pH', 0)
    time_length = len(time)
    parameter_result_length = len(parameter_result)
    assert time_length == parameter_result_length


def test_result_second():
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    react = t2react()
    react.read('flow.inp')
    results = t2result('toughreact', 'kdd_conc.tec', FILE_PATH)
    parameter_result = results.get_grid_data(5000, 'pH')
    parameter_result_length = len(parameter_result)
    assert len(react.grid.blocklist) == parameter_result_length
