
from cherab.core.utility.recursivedict import RecursiveDict
from cherab.core.atomic.elements import hydrogen, helium, lithium, beryllium, boron, carbon,\
    nitrogen, oxygen, fluorine, neon


# beam population coefficients:
# config["bmp"][beam_species][beam_metastable][target_ion][target_ionisation] = coefficient

ADF22_BMP_FILES = RecursiveDict()

ADF22_BMP_FILES["description"] = "Recommended set of ADF22 files for beam population coefficients. " \
                                 "config[beam_species][beam_metastable][target_ion][target_ionisation] = coefficient"

# H(m=2) -> H1+
ADF22_BMP_FILES[hydrogen][2][hydrogen][1] = ("adf22/bmp97#h/bmp97#h_2_h1.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_h1.dat")
# H(m=3) -> H1+
ADF22_BMP_FILES[hydrogen][3][hydrogen][1] = ("adf22/bmp97#h/bmp97#h_3_h1.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_h1.dat")
# H(m=4) -> H1+
ADF22_BMP_FILES[hydrogen][4][hydrogen][1] = ("adf22/bmp97#h/bmp97#h_4_h1.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_h1.dat")


# H(m=2) -> He2+
ADF22_BMP_FILES[hydrogen][2][helium][2] = ("adf22/bmp97#h/bmp97#h_2_he2.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_he2.dat")
# H(m=3) -> He2+
ADF22_BMP_FILES[hydrogen][3][helium][2] = ("adf22/bmp97#h/bmp97#h_3_he2.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_he2.dat")
# H(m=4) -> He2+
ADF22_BMP_FILES[hydrogen][4][helium][2] = ("adf22/bmp97#h/bmp97#h_4_he2.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_he2.dat")


# H(m=2) -> Li3+
ADF22_BMP_FILES[hydrogen][2][lithium][3] = ("adf22/bmp97#h/bmp97#h_2_li3.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_li3.dat")
# H(m=3) -> Li3+
ADF22_BMP_FILES[hydrogen][3][lithium][3] = ("adf22/bmp97#h/bmp97#h_3_li3.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_li3.dat")
# H(m=4) -> Li3+
ADF22_BMP_FILES[hydrogen][4][lithium][3] = ("adf22/bmp97#h/bmp97#h_4_li3.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_li3.dat")

# H(m=2) -> Be4+
ADF22_BMP_FILES[hydrogen][2][beryllium][4] = ("adf22/bmp97#h/bmp97#h_2_be4.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_be4.dat")
# H(m=3) -> Be4+
ADF22_BMP_FILES[hydrogen][3][beryllium][4] = ("adf22/bmp97#h/bmp97#h_3_be4.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_be4.dat")
# H(m=4) -> Be4+
ADF22_BMP_FILES[hydrogen][4][beryllium][4] = ("adf22/bmp97#h/bmp97#h_4_be4.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_be4.dat")


# H(m=2) -> B5+
ADF22_BMP_FILES[hydrogen][2][boron][5] = ("adf22/bmp97#h/bmp97#h_2_b5.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_b5.dat")
# H(m=3) -> B5+
ADF22_BMP_FILES[hydrogen][3][boron][5] = ("adf22/bmp97#h/bmp97#h_3_b5.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_b5.dat")
# H(m=4) -> B5+
ADF22_BMP_FILES[hydrogen][4][boron][5] = ("adf22/bmp97#h/bmp97#h_4_b5.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_b5.dat")


# H(m=2) -> C6+
ADF22_BMP_FILES[hydrogen][2][carbon][6] = ("adf22/bmp97#h/bmp97#h_2_c6.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_c6.dat")
# H(m=3) -> C6+
ADF22_BMP_FILES[hydrogen][3][carbon][6] = ("adf22/bmp97#h/bmp97#h_3_c6.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_c6.dat")
# H(m=4) -> C6+
ADF22_BMP_FILES[hydrogen][4][carbon][6] = ("adf22/bmp97#h/bmp97#h_4_c6.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_c6.dat")


# H(m=2) -> N7+
ADF22_BMP_FILES[hydrogen][2][nitrogen][7] = ("adf22/bmp97#h/bmp97#h_2_n7.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_n7.dat")
# H(m=3) -> N7+
ADF22_BMP_FILES[hydrogen][3][nitrogen][7] = ("adf22/bmp97#h/bmp97#h_3_n7.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_n7.dat")
# H(m=4) -> N7+
ADF22_BMP_FILES[hydrogen][4][nitrogen][7] = ("adf22/bmp97#h/bmp97#h_4_n7.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_n7.dat")


# H(m=2) -> O8+
ADF22_BMP_FILES[hydrogen][2][oxygen][8] = ("adf22/bmp97#h/bmp97#h_2_o8.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_o8.dat")
# H(m=3) -> O8+
ADF22_BMP_FILES[hydrogen][3][oxygen][8] = ("adf22/bmp97#h/bmp97#h_3_o8.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_o8.dat")
# H(m=4) -> O8+
ADF22_BMP_FILES[hydrogen][4][oxygen][8] = ("adf22/bmp97#h/bmp97#h_4_o8.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_o8.dat")


# H(m=2) -> F9+
ADF22_BMP_FILES[hydrogen][2][fluorine][9] = ("adf22/bmp97#h/bmp97#h_2_f9.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_f9.dat")
# H(m=3) -> F9+
ADF22_BMP_FILES[hydrogen][3][fluorine][9] = ("adf22/bmp97#h/bmp97#h_3_f9.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_f9.dat")
# H(m=4) -> F9+
ADF22_BMP_FILES[hydrogen][4][fluorine][9] = ("adf22/bmp97#h/bmp97#h_4_f9.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_f9.dat")


# H(m=2) -> Ne10+
ADF22_BMP_FILES[hydrogen][2][neon][10] = ("adf22/bmp97#h/bmp97#h_2_ne10.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_2_ne10.dat")
# H(m=3) -> Ne10+
ADF22_BMP_FILES[hydrogen][3][neon][10] = ("adf22/bmp97#h/bmp97#h_3_ne10.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_3_ne10.dat")
# H(m=4) -> Ne10+
ADF22_BMP_FILES[hydrogen][4][neon][10] = ("adf22/bmp97#h/bmp97#h_4_ne10.dat", "http://open.adas.ac.uk/download/adf22/bmp97][h/bmp97][h_4_ne10.dat")

