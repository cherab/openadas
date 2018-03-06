
from cherab.core.atomic.elements import hydrogen, carbon


ADF15_PEC_FILES = {
    "description": "Recommended set of ADF15 files for PEC coefficients",
    hydrogen: {
        0: {
            "ADAS_Path": "adf15/pec12#h/pec12#h_pju#h0.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec12][h/pec12][h_pju][h0.dat"
        }
    },
    carbon: {
        0: {
            "ADAS_Path": "adf15/pec96#c/pec96#c_vsu#c0.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][c/pec96][c_vsu][c0.dat"
        },
        1: {
            "ADAS_Path": "adf15/pec96#c/pec96#c_vsu#c1.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][c/pec96][c_vsu][c1.dat"
        },
        2: {
            "ADAS_Path": "adf15/pec96#c/pec96#c_vsu#c2.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][c/pec96][c_vsu][c2.dat"
        }
    }
}