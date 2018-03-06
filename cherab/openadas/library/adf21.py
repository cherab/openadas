
from cherab.core.atomic.elements import hydrogen, helium, lithium, beryllium, boron, carbon,\
    nitrogen, oxygen, fluorine, neon


ADF21_BMS_FILES = {

    "description": "Recommended set of ADF21 files for beam stopping coefficients. "
                   "config[beam_species][target_ion][target_ionisation] = coefficient",
    # beam_species
    hydrogen: {
        hydrogen: {  # H -> H1+
            1: ("adf21/bms97#h/bms97#h_h1.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_h1.dat")
        },
        helium: {  # H -> He2+
            2: ("adf21/bms97#h/bms97#h_he2.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_he2.dat")
        },
        lithium: {  # H -> Li3+
            3: ("adf21/bms97#h/bms97#h_li3.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_li3.dat")
        },
        beryllium: {  # H -> Be4+
            4: ("adf21/bms97#h/bms97#h_be4.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_be4.dat")
        },
        boron: {  # H -> B5+
            5: ("adf21/bms97#h/bms97#h_b5.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_b5.dat")
        },
        carbon: {  # H -> C6+
            6: ("adf21/bms97#h/bms97#h_c6.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_c6.dat")
        },
        nitrogen: {  # H -> N7+
            7: ("adf21/bms97#h/bms97#h_n7.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_n7.dat")
        },
        oxygen: {  # H -> O8+
            8: ("adf21/bms97#h/bms97#h_o8.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_o8.dat")
        },
        fluorine: {  # H -> F9+
            9: ("adf21/bms97#h/bms97#h_f9.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_f9.dat")
        },
        neon: {  # H -> Ne10+
            10: ("adf21/bms97#h/bms97#h_ne10.dat", "http://open.adas.ac.uk/download/adf21/bms97][h/bms97][h_ne10.dat")
        }
    }
}
