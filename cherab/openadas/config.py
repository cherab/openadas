# Copyright 2014-2017 United Kingdom Atomic Energy Authority
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.

import os
import urllib.request

from cherab.core.atomic import *
from cherab.core.utility.recursivedict import RecursiveDict
from cherab.openadas.read.adf15 import add_adf15_to_atomic_data


default = RecursiveDict()


# beam emission coefficients:
# config["bme"][beam_species][target_ion][target_ionisation][(initial_level, final_level)] = coefficient
default["bme"][hydrogen][1][hydrogen][(3, 2)] = "adf22/bme10#h/bme10#h_h1.dat"      # H0(n=3) + H+ -> H0(n=2) + H+ + hv (656.28 nm)
default["bme"][hydrogen][2][helium][(3, 2)] = "adf22/bme97#h/bme97#h_he2.dat"     # H0(n=3) + He2+ -> H0(n=2) + He2+ + hv (656.28 nm)
default["bme"][hydrogen][3][lithium][(3, 2)] = "adf22/bme97#h/bme97#h_li3.dat"     # H0(n=3) + Li3+ -> H0(n=2) + Li3+ + hv (656.28 nm)
default["bme"][hydrogen][4][beryllium][(3, 2)] = "adf22/bme97#h/bme97#h_be4.dat"     # H0(n=3) + Be4+ -> H0(n=2) + Be4+ + hv (656.28 nm)
default["bme"][hydrogen][5][boron][(3, 2)] = "adf22/bme97#h/bme97#h_b5.dat"      # H0(n=3) + B5+ -> H0(n=2) + B5+ + hv (656.28 nm)
default["bme"][hydrogen][6][carbon][(3, 2)] = "adf22/bme97#h/bme97#h_c6.dat"      # H0(n=3) + C6+ -> H0(n=2) + C6+ + hv (656.28 nm)
default["bme"][hydrogen][7][nitrogen][(3, 2)] = "adf22/bme97#h/bme97#h_n7.dat"      # H0(n=3) + N7+ -> H0(n=2) + N7+ + hv (656.28 nm)
default["bme"][hydrogen][8][fluorine][(3, 2)] = "adf22/bme97#h/bme97#h_f9.dat"      # H0(n=3) + F9+ -> H0(n=2) + F9+ + hv (656.28 nm)
default["bme"][hydrogen][9][oxygen][(3, 2)] = "adf22/bme97#h/bme97#h_o8.dat"      # H0(n=3) + O8+ -> H0(n=2) + O8+ + hv (656.28 nm)
default["bme"][hydrogen][10][neon][(3, 2)] = "adf22/bme97#h/bme97#h_ne10.dat"  # H0(n=3) + Ne10+ -> H0(n=2) + Ne10+ + hv (656.28 nm)
default["bme"][hydrogen][11][argon][(3, 2)] = "adf22/bme99#h/bme99#h_ar18.dat"  # H0(n=3) + Ar18+ -> H0(n=2) + Ar18+ + hv (656.28 nm)
# default["bme"][hydrogen][12][iron][(3, 2)] = "adf22/bme99#h/bme99#h_fe26.dat"  # H0(n=3) + Fe16+ -> H0(n=2) + Fe26+ + hv (656.28 nm)






default = default.freeze()
