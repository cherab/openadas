
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
from cherab.core.atomic.elements import hydrogen, helium, beryllium, carbon, neon, nitrogen


# Recommended set of ADF15 files for PEC coefficients
ADF15_PEC_FILES = {
    hydrogen: {
        0: {
            "ADAS_Path": "adf15/pec12#h/pec12#h_pju#h0.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec12][h/pec12][h_pju][h0.dat"
        }
    },
    helium: {
        0: {
            "ADAS_Path": "adf15/pec96#he/pec96#he_pju#he0.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][he/pec96][he_pju][he0.dat"
        },
        1: {
            "ADAS_Path": "adf15/pec96#he/pec96#he_pju#he1.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][he/pec96][he_pju][he1.dat"
        }
    },
    beryllium: {
        0: {
            "ADAS_Path": "adf15/pec96#be/pec96#be_pju#be0.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][be/pec96][be_pju][be0.dat"
        },
        1: {
            "ADAS_Path": "adf15/pec96#be/pec96#be_pju#be1.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][be/pec96][be_pju][be1.dat"
        },
        2: {
            "ADAS_Path": "adf15/pec96#be/pec96#be_pju#be2.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][be/pec96][be_pju][be2.dat"
        },
        3: {
            "ADAS_Path": "adf15/pec96#be/pec96#be_pju#be3.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][be/pec96][be_pju][be3.dat"
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
    },
    neon: {
        0: {
            "ADAS_Path": "adf15/pec96#ne/pec96#ne_pju#ne0.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][ne/pec96][ne_pju][ne0.dat"
        },
        1: {
            "ADAS_Path": "adf15/pec96#ne/pec96#ne_pju#ne1.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][ne/pec96][ne_pju][ne1.dat"
        }
    },
    nitrogen: {
        0: {
            "ADAS_Path": "adf15/pec96#n/pec96#n_vsu#n0.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][n/pec96][n_vsu][n0.dat"
        },
        1: {
            "ADAS_Path": "adf15/pec96#n/pec96#n_vsu#n1.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][n/pec96][n_vsu][n1.dat"
        },
        2: {
            "ADAS_Path": "adf15/pec96#n/pec96#n_vsu#n2.dat",
            "Download_URL": "http://open.adas.ac.uk/download/adf15/pec96][n/pec96][n_vsu][n2.dat"
        }
    }
}


# Another version of the library files keyed by filename for quicker lookup
_ADF15_FILES_BY_FILENAME = {}
for element in ADF15_PEC_FILES.keys():
    for ionisation in ADF15_PEC_FILES[element].keys():
        adf15_record = ADF15_PEC_FILES[element][ionisation]
        adf15_filename = os.path.split(adf15_record["ADAS_Path"])[1]
        _ADF15_FILES_BY_FILENAME[adf15_filename] = {
            "File_Type": "ADF15",
            "ADAS_Path": adf15_record["ADAS_Path"],
            "Download_URL": adf15_record["Download_URL"],
            "Element": element,
            "Ionisation": ionisation
        }
