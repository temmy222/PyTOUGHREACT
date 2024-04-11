import unittest
import numpy as np
from mulgrids import mulgrid
from context import pytoughreact
from t2grids import t2grid
from t2data import rocktype


class BioTestCase(unittest.TestCase):

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

        bio = pytoughreact.t2bio()
        bio.title = 'Biodegradation Runs'

        bio.grid = t2grid().fromgeo(geo)
        bio.grid.delete_rocktype('dfalt')
        shale = rocktype('shale', 0, 2600, 0.67, [6.51e-14, 6.51e-14, 6.51e-14], 1.5, 900)
        bio.grid.add_rocktype(shale)

        for blk in bio.grid.blocklist[0:]:
            blk.rocktype = bio.grid.rocktype[shale.name]

        bio.multi = {'num_components': 3, 'num_equations': 3, 'num_phases': 3,
                     'num_secondary_parameters': 8}

        bio.parameter.update(
            {'print_level': 3,
             'max_timesteps': 9999,
             'tstop': simtime,
             'const_timestep': 1.,
             'print_interval': 1,
             'gravity': 9.81,
             'option': np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
             'relative_error': 1e-5,
             'phase_index': 2,
             'default_incons': [9.57e+05, 0, 0, 0, 0, 0, 0, 1e-3, 10.]})

        # ,

        bio.start = True
        toluene = pytoughreact.Component(1).defaultToluene()
        bio.components = [toluene]

        o2_gas = pytoughreact.Gas('O2', 2)
        bio.gas = [o2_gas]

        water = pytoughreact.Water_Bio('H2O')

        biomass = pytoughreact.Biomass(1, 'biom', 0.153, 1.00e-6, 30, 0, 0.e-6)
        oxygen_ks = 0.5e-6
        oxygen_uptake = 1
        water_uptake = -3

        process1 = pytoughreact.Process(biomass, 2, 1.6944e-04, 0.58, 0)
        water.addToProcess(process1, water_uptake)
        o2_gas.addToProcess(process1, oxygen_uptake, oxygen_ks)
        toluene.addToProcess(process1, 1, 7.4625e-06)

        biodegradation = pytoughreact.BIODG(0, 1e-5, 0, 0.2, 0.9, 0.9, [process1], [biomass])
        bio.biodg = [biodegradation]

        bio.diffusion = [
            [2.e-5, 6.e-10, 6.e-10],
            [2.e-5, 6.e-10, 6.e-10],
            [2.e-5, 6.e-10, 6.e-10]
        ]

        bio.write('INFILE')
        return bio

    def set_up_read(self):
        bio_read = pytoughreact.t2bio()
        bio_read.read('INFILE')

        return bio_read

    def test_write(self):
        write_output = self.set_up_write()
        result = write_output.status
        self.assertEqual(result, 'successful')

    def test_read(self):
        write_output = self.set_up_read()
        result = write_output.status
        self.assertEqual(result, 'successful')

    def test_result_first(self):
        results = pytoughreact.FileReadSingle('tmvoc', 'OUTPUT_ELEME.csv', 'test')
        time = results.get_times('second')
        parameter_result = results.get_time_series_data('X_toluen_L', 0)
        time_length = len(time)
        parameter_result_length = len(parameter_result)
        self.assertEqual(time_length, parameter_result_length)


if __name__ == "__main__":
    unittest.main()
