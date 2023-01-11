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

from chemical.mineral_description import Mineral
from chemical.kinetic_properties import Precipitation, Dissolution, pHDependenceType2, Equilibrium

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

equilibrium_c3fh6 = Equilibrium(0, 0, 0)
c3fh6_equil = Mineral('C3FH6', 0, 0, 0, 0)
c3fh6_equil.equilibrium = [equilibrium_c3fh6]


dissolution_tobermorite = Dissolution(1.0e-012, 0, 1, 1, 0.0)
precipitation_tobermorite = Precipitation(1.0e-012, 0, 1, 1, 0, 0, 0, 0, 1e-6, 0, 0, 0, 0)
tobermorite = Mineral('Tobermorite(11A)', 1, 3, 0, 0)
tobermorite.dissolution = [dissolution_tobermorite]
tobermorite.precipitation = [precipitation_tobermorite]

equilibrium_tobermorite = Equilibrium(0, 0, 0)
tobermorite_equil = Mineral('Tobermorite(11A)', 0, 0, 0, 0)
tobermorite_equil.equilibrium = [equilibrium_tobermorite]

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
    'c3fh6_equil': c3fh6_equil,
    'tobermorite': tobermorite,
    'tobermorite_equil': tobermorite_equil,
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


def get_kinetics_minerals(mineral_list):
    output = []
    for mineral in mineral_list:
        output.append(default_minerals[mineral.lower()])
    return output


def get_specific_mineral(mineral_name):
    return default_minerals[mineral_name.lower()]
