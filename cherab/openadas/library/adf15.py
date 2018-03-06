
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
