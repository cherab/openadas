
from cherab.core.atomic.elements import hydrogen, helium, beryllium, boron, carbon, neon


ADF12_CXS_FILES = {

    "description": "Recommended set of ADF12 files for Beam-CX emission rate coefficients. "
                   "config[donor_species][receiver_ion][receiver_ionisation] = "
                   "[([donor_metastable], rate_file, download_path), ...]",
    # donor_species
    hydrogen: {

        # receiver_ion
        hydrogen: {
            # receiver_ionisation
            1: [
                (1, "adf12/qef93#h/qef93#h_h1.dat", "http://open.adas.ac.uk/download/adf12/qef93][h/qef93][h_h1.dat")
            ]
        },

        # receiver_ion
        helium: {
            # receiver_ionisation
            2: [
                (1, "adf12/qef93#h/qef93#h_he2.dat", "http://open.adas.ac.uk/download/adf12/qef93][h/qef93][h_he2.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#he2.dat", "http://open.adas.ac.uk/download/adf12/qef97][h/qef97][h_en2_kvi][he2.dat"),
            ],
        },

        # receiver_ion
        beryllium: {
            # receiver_ionisation
            4: [
                (1, "adf12/qef93#h/qef93#h_be4.dat", "http://open.adas.ac.uk/download/adf12/qef93][h/qef93][h_be4.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#be4.dat", "http://open.adas.ac.uk/download/adf12/qef97][h/qef97][h_en2_kvi][be4.dat"),
            ],
        },

        # receiver_ion
        boron: {
            # receiver_ionisation
            5: [
                (1, "adf12/qef93#h/qef93#h_b5.dat", "http://open.adas.ac.uk/download/adf12/qef93][h/qef93][h_b5.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#b5.dat", "http://open.adas.ac.uk/download/adf12/qef97][h/qef97][h_en2_kvi][b5.dat"),
            ]
        },

        # receiver_ion
        carbon: {
            # receiver_ionisation
            6: [
                (1, "adf12/qef93#h/qef93#h_c6.dat", "http://open.adas.ac.uk/download/adf12/qef93][h/qef93][h_c6.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#c6.dat", "http://open.adas.ac.uk/download/adf12/qef97][h/qef97][h_en2_kvi][c6.dat"),
            ]
        },

        # receiver_ion
        neon: {
            # receiver_ionisation
            10: [
                (1, "adf12/qef93#h/qef93#h_ne10.dat", "http://open.adas.ac.uk/download/adf12/qef93][h/qef93][h_ne10.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#ne10.dat", "http://open.adas.ac.uk/download/adf12/qef97][h/qef97][h_en2_kvi][ne10.dat"),
            ],
        },
    }
}
