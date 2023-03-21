import unittest
from pytoughreact.chemical.kinetic_properties import pHDependenceType2, Dissolution, Precipitation
from pytoughreact.chemical.mineral_description import Mineral
from pytoughreact.chemical.chemical_composition import PrimarySpecies, WaterComp, Water, ReactGas
from pytoughreact.chemical.mineral_composition import MineralComp
from pytoughreact.chemical.mineral_zone import MineralZone
from pytoughreact.chemical.perm_poro_zone import PermPoro, PermPoroZone
from mulgrids import mulgrid
from pytoughreact.writers.react_writing import t2react
from pytoughreact.writers.solute_writing import t2solute
from pytoughreact.writers.chemical_writing import t2chemical
from t2grids import rocktype
from pytoughreact.wrapper.reactzone import t2zone
from pytoughreact.wrapper.reactgrid import t2reactgrid
from pytoughreact.results.result_single import FileReadSingle


class ReactTestCase(unittest.TestCase):
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
        simtime = 1 * year

        # --------------------------------------------FLOW.INP-----------------------------------------------------------------

        length = 9
        xblock = 3
        # yblock = 1
        zblock = 4
        dx = [length / xblock] * xblock
        dy = [0.1]
        dz = [2] * zblock
        geo = mulgrid().rectangular(dx, dy, dz, origin=[0, 0, -100])
        geo.write('geom.dat')

        react = t2react()
        react.title = 'Multiple Rock Type'

        react.multi = {'num_components': 1, 'num_equations': 1, 'num_phases': 2,
                       'num_secondary_parameters': 6}

        react.grid = t2reactgrid().fromgeo(geo)

        react.parameter.update(
            {'print_level': 3,
             'max_timesteps': 9999,
             'tstop': simtime,
             'const_timestep': 8640,
             #    'max_timestep': 8640,
             'print_interval': 2000,
             'gravity': 9.81,
             'relative_error': 1.0000e-06,
             'phase_index': 2,
             'default_incons': [8.06011440362800e+07, 1.70e+02]})

        shale = rocktype('shale', 0, 2600, 0.12, [6.51e-17, 6.51e-17, 6.51e-17], 1.5, 900)

        react.grid.delete_rocktype('dfalt')
        react.grid.add_rocktype(shale)

        for blk in react.grid.blocklist[0:]:
            blk.rocktype = react.grid.rocktype[shale.name]

        shale_zone = t2zone('shale_zone')

        react.grid.add_zone(shale_zone)

        for blk in react.grid.blocklist[0:]:
            blk.zone = react.grid.zone[shale_zone.name]

        react.start = True

        react.write('flow.inp')

        # ---------------------------CHEMICAL.INP------------------------------------------------------------------------------
        h2o = PrimarySpecies('h2o', 0)
        h = PrimarySpecies('h+', 0)
        na = PrimarySpecies('na+', 0)
        cl = PrimarySpecies('cl-', 0)
        hco3 = PrimarySpecies('hco3-', 0)
        ca = PrimarySpecies('ca+2', 0)
        so4 = PrimarySpecies('so4-2', 0)
        mg = PrimarySpecies('mg+2', 0)
        h4sio4 = PrimarySpecies('H4SiO4', 0)
        al = PrimarySpecies('Al+3', 0)
        fe = PrimarySpecies('Fe+2', 0)
        hs = PrimarySpecies('HS-', 0)
        k = PrimarySpecies('K+', 0)

        all_species = [h2o, h, na, cl, hco3, ca, so4, mg, h4sio4, al, fe, hs, k]

        h2o_comp3 = WaterComp(h2o, 1, 1.0000E+00, 1.000000E+00)
        h_comp3 = WaterComp(h, 1, 5.9661E-06, 1.462590E-02)
        na_comp3 = WaterComp(na, 1, 2.2792E+00, 2.279674E+00)
        cl_comp3 = WaterComp(cl, 1, 3.5408E+00, 4.093523E+00)
        hco3_comp3 = WaterComp(hco3, 1, 1.2372E-03, 1.704293E-02)
        ca_comp3 = WaterComp(ca, 1, 4.1945E-01, 5.601284E-01)
        so4_comp3 = WaterComp(so4, 1, 4.8191E-05, 9.094219E-05)
        mg_comp3 = WaterComp(mg, 1, 6.1888E-02, 7.895666E-02)
        h4sio4_comp3 = WaterComp(h4sio4, 1, 2.9275E-03, 2.929168E-03)
        al_comp3 = WaterComp(al, 1, 1.6208E-12, 5.086910E-08)
        fe_comp3 = WaterComp(fe, 1, 9.8531E-03, 1.130685E-02)
        hs_comp3 = WaterComp(hs, 1, 7.8240E-08, 4.566225E-07)
        k_comp3 = WaterComp(k, 1, 1.7547E-01, 5.272968E-01)

        initial_shale_water = Water(
            [h2o_comp3, h_comp3, na_comp3, cl_comp3, hco3_comp3, ca_comp3, so4_comp3, mg_comp3, h4sio4_comp3, al_comp3,
             fe_comp3, hs_comp3, k_comp3], 170, 805.9)

        quartz_zone2 = MineralComp(self.get_specific_mineral('quartz'), 0.369, 1, 0.0E-00, 157.3, 0)
        microcline_zone2 = MineralComp(self.get_specific_mineral('microcline'), 0.0351, 1, 0.0E-00, 12.9, 0)
        albite_zone2 = MineralComp(self.get_specific_mineral('albite'), 0.0815, 1, 0.0E-00, 9.1, 0)
        muscovite_zone2 = MineralComp(self.get_specific_mineral('muscovite'), 0.2388, 1, 0.0E-00, 9.1, 0)
        chlorite_zone2 = MineralComp(self.get_specific_mineral('chlorite'), 0.1236, 1, 0.0E-00, 9.1, 0)
        dolomite_zone2 = MineralComp(self.get_specific_mineral('dolomite'), 0.073, 1, 0.0E-00, 12, 0)
        calcite_zone2 = MineralComp(self.get_specific_mineral('calcite'), 0.054, 1, 0.0E-00, 260, 0)

        initial_co2 = ReactGas('co2(g)', 0, 0)
        # injection_co2 = ReactGas('co2(g)', 0, 0.01)
        # ijgas = [[initial_co2], [injection_co2]]

        permporo = PermPoro(1, 0, 0)
        permporozone = PermPoroZone([permporo])

        shale_zone.water = [[initial_shale_water], []]
        shale_zone.gas = [[initial_co2], []]
        shale_mineral_zone = MineralZone(
            [quartz_zone2, microcline_zone2, albite_zone2, muscovite_zone2, chlorite_zone2, dolomite_zone2, calcite_zone2])
        shale_zone.mineral_zone = shale_mineral_zone
        shale_zone.permporo = permporozone

        mineral_list = ['quartz', 'microcline', 'albite', 'muscovite', 'chlorite', 'dolomite', 'calcite']
        all_minerals = self.get_kinetics_minerals(mineral_list)

        writeChemical = t2chemical(t2reactgrid=react.grid)
        writeChemical.minerals = all_minerals
        writeChemical.title = "An-Gy-Hal-Hal"
        writeChemical.primary_aqueous = all_species
        writeChemical.gases = [initial_co2]
        # masa = writeChemical.perm_poro_index
        writeChemical.write()

        writeSolute = t2solute(writeChemical)
        writeSolute.nodes_to_write = [0]
        writeSolute.options['linear_equation_solver'] = 4
        writeSolute.write()
        return writeSolute

    def set_up_read(self):
        react = t2react()
        react.read('flow.inp')
        writeChemical = t2chemical(t2reactgrid=react.grid)
        writeSolute = t2solute(t2chemical=writeChemical)

        writeChemical.read('chemical.inp')
        writeSolute.read('solute.inp')

        return writeSolute

    def test_write(self):
        write_output = self.set_up_write()
        result = write_output.status
        self.assertEqual(result, 'successful')

    def test_read(self):
        write_output = self.set_up_read()
        result = write_output.status
        self.assertEqual(result, 'successful')

    def test_result_first(self):
        results = FileReadSingle('toughreact', 'kdd_conc.tec')
        time = results.get_times('second')
        parameter_result = results.get_time_series_data('pH', 0)
        time_length = len(time)
        parameter_result_length = len(parameter_result)
        self.assertEqual(time_length, parameter_result_length)

    def test_result_second(self):
        react = t2react()
        react.read('flow.inp')
        results = FileReadSingle('toughreact', 'kdd_conc.tec')
        parameter_result = results.get_grid_data(5000, 'pH')
        parameter_result_length = len(parameter_result)
        self.assertEqual(len(react.grid.blocklist), parameter_result_length)
