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

from cherab.core.atomic.elements import *
from cherab.core.utility.recursivedict import RecursiveDict

# TODO: future expansion, need to consider how to handle isotopes - include atomic weight with a "catch all" for ion species with a natural isotope abundance
default = RecursiveDict()

# effective charge exchange rates:
# config["cxs"][donor_species][receiver_ion][receiver_ionisation] = [(donor_metastable, rate), ...]
default["cxs"][hydrogen][hydrogen][1] = [(1, "adf12/qef93#h/qef93#h_h1.dat")]
default["cxs"][hydrogen][helium][2] = [(1, "adf12/qef93#h/qef93#h_he2.dat"), (2, "adf12/qef97#h/qef97#h_en2_kvi#he2.dat")]
default["cxs"][hydrogen][beryllium][4] = [(1, "adf12/qef93#h/qef93#h_be4.dat"), (2, "adf12/qef97#h/qef97#h_en2_kvi#be4.dat")]
default["cxs"][hydrogen][boron][5] = [(1, "adf12/qef93#h/qef93#h_b5.dat"), (2, "adf12/qef97#h/qef97#h_en2_kvi#b5.dat")]
default["cxs"][hydrogen][carbon][6] = [(1, "adf12/qef93#h/qef93#h_c6.dat"), (2, "adf12/qef97#h/qef97#h_en2_kvi#c6.dat")]
default["cxs"][hydrogen][neon][10] = [(1, "adf12/qef93#h/qef93#h_ne10.dat"), (2, "adf12/qef97#h/qef97#h_en2_kvi#ne10.dat")]


# beam population coefficients:
# config["bmp"][beam_species][beam_metastable][target_ion][target_ionisation] = coefficient
default["bmp"][hydrogen][2][hydrogen][1] = "adf22/bmp97#h/bmp97#h_2_h1.dat"       # H(m=2) -> H1+
default["bmp"][hydrogen][3][hydrogen][1] = "adf22/bmp97#h/bmp97#h_3_h1.dat"       # H(m=3) -> H1+
default["bmp"][hydrogen][4][hydrogen][1] = "adf22/bmp97#h/bmp97#h_4_h1.dat"       # H(m=4) -> H1+

default["bmp"][hydrogen][2][helium][2] = "adf22/bmp97#h/bmp97#h_2_he2.dat"      # H(m=2) -> He2+
default["bmp"][hydrogen][3][helium][2] = "adf22/bmp97#h/bmp97#h_3_he2.dat"      # H(m=3) -> He2+
default["bmp"][hydrogen][4][helium][2] = "adf22/bmp97#h/bmp97#h_4_he2.dat"      # H(m=4) -> He2+

default["bmp"][hydrogen][2][lithium][3] = "adf22/bmp97#h/bmp97#h_2_li3.dat"      # H(m=2) -> Li3+
default["bmp"][hydrogen][3][lithium][3] = "adf22/bmp97#h/bmp97#h_3_li3.dat"      # H(m=3) -> Li3+
default["bmp"][hydrogen][4][lithium][3] = "adf22/bmp97#h/bmp97#h_4_li3.dat"      # H(m=4) -> Li3+

default["bmp"][hydrogen][2][beryllium][4] = "adf22/bmp97#h/bmp97#h_2_be4.dat"      # H(m=2) -> Be4+
default["bmp"][hydrogen][3][beryllium][4] = "adf22/bmp97#h/bmp97#h_3_be4.dat"      # H(m=3) -> Be4+
default["bmp"][hydrogen][4][beryllium][4] = "adf22/bmp97#h/bmp97#h_4_be4.dat"      # H(m=4) -> Be4+

default["bmp"][hydrogen][2][boron][5] = "adf22/bmp97#h/bmp97#h_2_b5.dat"       # H(m=2) -> B5+
default["bmp"][hydrogen][3][boron][5] = "adf22/bmp97#h/bmp97#h_3_b5.dat"       # H(m=3) -> B5+
default["bmp"][hydrogen][4][boron][5] = "adf22/bmp97#h/bmp97#h_4_b5.dat"       # H(m=4) -> B5+

default["bmp"][hydrogen][2][carbon][6] = "adf22/bmp97#h/bmp97#h_2_c6.dat"       # H(m=2) -> C6+
default["bmp"][hydrogen][3][carbon][6] = "adf22/bmp97#h/bmp97#h_3_c6.dat"       # H(m=3) -> C6+
default["bmp"][hydrogen][4][carbon][6] = "adf22/bmp97#h/bmp97#h_4_c6.dat"       # H(m=4) -> C6+

default["bmp"][hydrogen][2][nitrogen][7] = "adf22/bmp97#h/bmp97#h_2_n7.dat"       # H(m=2) -> N7+
default["bmp"][hydrogen][3][nitrogen][7] = "adf22/bmp97#h/bmp97#h_3_n7.dat"       # H(m=3) -> N7+
default["bmp"][hydrogen][4][nitrogen][7] = "adf22/bmp97#h/bmp97#h_4_n7.dat"       # H(m=4) -> N7+

default["bmp"][hydrogen][2][oxygen][8] = "adf22/bmp97#h/bmp97#h_2_o8.dat"       # H(m=2) -> O8+
default["bmp"][hydrogen][3][oxygen][8] = "adf22/bmp97#h/bmp97#h_3_o8.dat"       # H(m=3) -> O8+
default["bmp"][hydrogen][4][oxygen][8] = "adf22/bmp97#h/bmp97#h_4_o8.dat"       # H(m=4) -> O8+

default["bmp"][hydrogen][2][fluorine][9] = "adf22/bmp97#h/bmp97#h_2_f9.dat"       # H(m=2) -> F9+
default["bmp"][hydrogen][3][fluorine][9] = "adf22/bmp97#h/bmp97#h_3_f9.dat"       # H(m=3) -> F9+
default["bmp"][hydrogen][4][fluorine][9] = "adf22/bmp97#h/bmp97#h_4_f9.dat"       # H(m=4) -> F9+

default["bmp"][hydrogen][2][neon][10] = "adf22/bmp97#h/bmp97#h_2_ne10.dat"   # H(m=2) -> Ne10+
default["bmp"][hydrogen][3][neon][10] = "adf22/bmp97#h/bmp97#h_3_ne10.dat"   # H(m=3) -> Ne10+
default["bmp"][hydrogen][4][neon][10] = "adf22/bmp97#h/bmp97#h_4_ne10.dat"   # H(m=4) -> Ne10+


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


# beam stopping coefficients:
# config["bms"][beam_species][target_ion][target_ionisation] = coefficient
default["bms"][hydrogen][hydrogen][1] = "adf21/bms97#h/bms97#h_h1.dat"        # H -> H1+
default["bms"][hydrogen][helium][2] = "adf21/bms97#h/bms97#h_he2.dat"       # H -> He2+
default["bms"][hydrogen][lithium][3] = "adf21/bms97#h/bms97#h_li3.dat"       # H -> Li3+
default["bms"][hydrogen][beryllium][4] = "adf21/bms97#h/bms97#h_be4.dat"       # H -> Be4+
default["bms"][hydrogen][boron][5] = "adf21/bms97#h/bms97#h_b5.dat"        # H -> B5+
default["bms"][hydrogen][carbon][6] = "adf21/bms97#h/bms97#h_c6.dat"        # H -> C6+
default["bms"][hydrogen][nitrogen][7] = "adf21/bms97#h/bms97#h_n7.dat"        # H -> N7+
default["bms"][hydrogen][oxygen][8] = "adf21/bms97#h/bms97#h_o8.dat"        # H -> O8+
default["bms"][hydrogen][fluorine][9] = "adf21/bms97#h/bms97#h_f9.dat"        # H -> F9+
default["bms"][hydrogen][neon][10] = "adf21/bms97#h/bms97#h_ne10.dat"    # H -> Ne10+


# Electron Impact Excitation rate coefficients (PECs)
# config["eim"][species][ionisation][(initial_level, final_level)] = coefficient
default["eim"][hydrogen][0][(2, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 1)
default["eim"][hydrogen][0][(3, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 2)
default["eim"][hydrogen][0][(3, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 3)
default["eim"][hydrogen][0][(4, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 4)
default["eim"][hydrogen][0][(4, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 5)
default["eim"][hydrogen][0][(4, 3)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 6)
default["eim"][hydrogen][0][(5, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 7)
default["eim"][hydrogen][0][(5, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 8)
default["eim"][hydrogen][0][(5, 3)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 9)
default["eim"][hydrogen][0][(5, 4)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 10)
default["eim"][hydrogen][0][(6, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 11)
default["eim"][hydrogen][0][(6, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 12)
default["eim"][hydrogen][0][(6, 3)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 13)
default["eim"][hydrogen][0][(6, 4)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 14)
default["eim"][hydrogen][0][(6, 5)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 15)
default["eim"][hydrogen][0][(7, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 16)
default["eim"][hydrogen][0][(7, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 17)
default["eim"][hydrogen][0][(7, 3)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 18)
default["eim"][hydrogen][0][(7, 4)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 19)

# Recombination rate coefficients (PECs)
# config["rec"][species][ionisation][(initial_level, final_level)] = coefficient
default["rec"][hydrogen][0][(2, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 67)
default["rec"][hydrogen][0][(3, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 68)
default["rec"][hydrogen][0][(3, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 69)
default["rec"][hydrogen][0][(4, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 70)
default["rec"][hydrogen][0][(4, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 71)
default["rec"][hydrogen][0][(4, 3)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 72)
default["rec"][hydrogen][0][(5, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 73)
default["rec"][hydrogen][0][(5, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 74)
default["rec"][hydrogen][0][(5, 3)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 75)
default["rec"][hydrogen][0][(5, 4)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 76)
default["rec"][hydrogen][0][(6, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 77)
default["rec"][hydrogen][0][(6, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 78)
default["rec"][hydrogen][0][(6, 3)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 79)
default["rec"][hydrogen][0][(6, 4)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 80)
default["rec"][hydrogen][0][(6, 5)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 81)
default["rec"][hydrogen][0][(7, 1)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 82)
default["rec"][hydrogen][0][(7, 2)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 83)
default["rec"][hydrogen][0][(7, 3)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 84)
default["rec"][hydrogen][0][(7, 4)] = ('adf15/pec96#h/pec96#h_pju#h0.dat', 85)


# TODO: there are concerns about the accuracy of this data
# Data from NIST Atomic Spectra Database - http://www.nist.gov/pml/data/asd.cfm
# line emission natural wavelength (in nanometers):
# config["wavelength"][ion][ionisation][(initial_level, final_level)] = wavelength



# H0
default["wavelength"][hydrogen][0] = {
    (2, 1): 121.57,
    (3, 1): 102.53,
    (3, 2): 656.28,
    (4, 1): 97.21,
    (4, 2): 486.06,
    (4, 3): 1875.13,
    (5, 1): 94.93,
    (5, 2): 433.99,
    (5, 3): 1281.61,
    (5, 4): 4052.28,
    (6, 1): 93.74,
    (6, 2): 410.12,
    (6, 3): 1093.64,
    (6, 4): 2625.87,
    (6, 5): 7459.90,
    (7, 1): 93.04,
    (7, 2): 396.95,
    (7, 3): 1004.79,
    (7, 4): 2165.19
}

default["wavelength"][protium][0] = {
    (2, 1): 121.57,
    (3, 1): 102.53,
    (3, 2): 656.28,
    (4, 1): 97.21,
    (4, 2): 486.06,
    (4, 3): 1875.13,
    (5, 1): 94.93,
    (5, 2): 433.99,
    (5, 3): 1281.61,
    (5, 4): 4052.28,
    (6, 1): 93.74,
    (6, 2): 410.12,
    (6, 3): 1093.64,
    (6, 4): 2625.87,
    (6, 5): 7459.90,
    (7, 1): 93.04,
    (7, 2): 396.95,
    (7, 3): 1004.79,
    (7, 4): 2165.19
}

# TODO - fix these with correct wavelengths
default["wavelength"][deuterium][0] = {
    (2, 1): 121.57,
    (3, 1): 102.53,
    (3, 2): 656.28,
    (4, 1): 97.21,
    (4, 2): 486.06,
    (4, 3): 1875.13,
    (5, 1): 94.93,
    (5, 2): 433.99,
    (5, 3): 1281.61,
    (5, 4): 4052.28,
    (6, 1): 93.74,
    (6, 2): 410.12,
    (6, 3): 1093.64,
    (6, 4): 2625.87,
    (6, 5): 7459.90,
    (7, 1): 93.04,
    (7, 2): 396.95,
    (7, 3): 1004.79,
    (7, 4): 2165.19
}
# TODO - fix these with correct wavelengths
default["wavelength"][tritium][0] = {
    (2, 1): 121.57,
    (3, 1): 102.53,
    (3, 2): 656.28,
    (4, 1): 97.21,
    (4, 2): 486.06,
    (4, 3): 1875.13,
    (5, 1): 94.93,
    (5, 2): 433.99,
    (5, 3): 1281.61,
    (5, 4): 4052.28,
    (6, 1): 93.74,
    (6, 2): 410.12,
    (6, 3): 1093.64,
    (6, 4): 2625.87,
    (6, 5): 7459.90,
    (7, 1): 93.04,
    (7, 2): 396.95,
    (7, 3): 1004.79,
    (7, 4): 2165.19
}


# He1+
default["wavelength"][helium][1] = {
    (2, 1): 30.378,     # 2p -> 1s
    (3, 1): 25.632,     # 3p -> 1s
    (3, 2): 164.04,     # 3d -> 2p
    (4, 2): 121.51,     # 4d -> 2p
    (4, 3): 468.71,     # 4f -> 3d
    (5, 3): 320.28,     # 5f -> 3d
    (5, 4): 1012.65,    # 5g -> 4f
    (6, 4): 656.20,     # 6g -> 4f
    (6, 5): 1864.20,    # 6h -> 5g
    (7, 5): 1162.53,    # from ADAS comment, unknown source
    (7, 6): 3090.55     # from ADAS comment, unknown source
}


# Be3+
default["wavelength"][beryllium][3] = {
    (3, 1): 6.4065,     # 3p -> 1s
    (3, 2): 41.002,     # 3d -> 2p
    (4, 2): 30.373,     # 4d -> 2p
    (4, 3): 117.16,     # 4f -> 3d
    (5, 3): 80.092,     # 5f -> 3d
    (5, 4): 253.14,     # 5g -> 4f
    (6, 4): 164.03,     # 6g -> 4f
    (6, 5): 466.01,     # 6h -> 5g
    (7, 5): 290.62,     # from ADAS comment, unknown source
    (7, 6): 772.62,     # from ADAS comment, unknown source
    (8, 6): 468.53,     # from ADAS comment, unknown source
    (8, 7): 1190.42     # from ADAS comment, unknown source
}

# B4+
default["wavelength"][boron][4] = {
    (3, 1): 4.0996,     # 3p -> 1s
    (3, 2): 26.238,     # 3d -> 2p
    (4, 2): 19.437,     # 4d -> 2p
    (4, 3): 74.980,     # 4f -> 3d
    (5, 3): 51.257,     # 5f -> 3d
    (5, 4): 162.00,     # 5g -> 4f
    (6, 4): 104.98,     # 6g -> 4f
    (6, 5): 298.24,     # 6h -> 5g
    (7, 5): 186.05,     # 7h -> 5g
    (7, 6): 494.48,     # 7i -> 6h
    (8, 6): 299.86,     # 8i -> 6h
    (8, 7): 761.87,     # 8k -> 7i
    (9, 7): 451.99,     # 9k -> 7i
    (9, 8): 1111.25     # from ADAS comment, unknown source
}

# C5+
default["wavelength"][carbon][5] = {
    (4, 2): 13.496,     # 4d -> 2p
    (4, 3): 52.067,     # 4f -> 3d
    (5, 3): 35.594,     # 5f -> 3d
    (5, 4): 112.50,     # 5g -> 4f
    (6, 4): 72.900,     # 6g -> 4f
    (6, 5): 207.11,     # 6h -> 5g
    (7, 5): 129.20,     # from ADAS comment, unknown source
    (7, 6): 343.38,     # from ADAS comment, unknown source
    (8, 6): 208.23,     # from ADAS comment, unknown source
    (8, 7): 529.07,     # from ADAS comment, unknown source
    (9, 7): 313.87,     # from ADAS comment, unknown source
    (9, 8): 771.69,     # from ADAS comment, unknown source
    (10, 8): 449.89,    # from ADAS comment, unknown source
    (10, 9): 1078.86    # from ADAS comment, unknown source
}

# Ne9+
default["wavelength"][neon][9] = {
    (6, 5): 74.54,      # from ADAS comment, unknown source
    (7, 6): 123.64,     # from ADAS comment, unknown source
    (8, 7): 190.50,     # from ADAS comment, unknown source
    (9, 8): 277.79,     # from ADAS comment, unknown source
    (10, 9): 388.37,    # from ADAS comment, unknown source
    (11, 10): 524.92,   # from ADAS comment, unknown source
    (12, 11): 690.16,   # from ADAS comment, unknown source
    (13, 12): 886.83,   # from ADAS comment, unknown source
    (6, 4): 26.24,      # from ADAS comment, unknown source
    (7, 5): 46.51,      # from ADAS comment, unknown source
    (8, 6): 74.98,      # from ADAS comment, unknown source
    (9, 7): 113.02,     # from ADAS comment, unknown source
    (10, 8): 162.00,    # from ADAS comment, unknown source
    (11, 9): 223.22,    # from ADAS comment, unknown source
    (12, 10): 298.15,   # from ADAS comment, unknown source
    (13, 11): 388.12    # from ADAS comment, unknown source
}

default = default.freeze()
