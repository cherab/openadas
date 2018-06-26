
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
from cherab.core.atomic.elements import *
from cherab.openadas.install import install_files

install_files(
    {
        'adf12': (
            # (donor, receiver, ionisation, ((donor_metastable, rate file), ...))
            (hydrogen, hydrogen, 1, (
                (1, 'adf12/qef93#h/qef93#h_h1.dat')
            )),
            (hydrogen, helium, 2, (
                (1, "adf12/qef93#h/qef93#h_he2.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#he2.dat")
            )),
            (hydrogen, beryllium, 4, (
                (1, "adf12/qef93#h/qef93#h_be4.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#be4.dat")
            )),
            (hydrogen, boron, 5, (
                (1, "adf12/qef93#h/qef93#h_b5.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#b5.dat")
            )),
            (hydrogen, carbon, 6, (
                (1, "adf12/qef93#h/qef93#h_c6.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#c6.dat")
            )),
            (hydrogen, neon, 10, (
                (1, "adf12/qef93#h/qef93#h_ne10.dat"),
                (2, "adf12/qef97#h/qef97#h_en2_kvi#ne10.dat"),
            )),
        ),
        'adf15': (
            (hydrogen, 0, 'adf15/pec12#h/pec12#h_pju#h0.dat'),
            (helium, 0, 'adf15/pec96#he/pec96#he_pju#he0.dat'),
            (helium, 1, 'adf15/pec96#he/pec96#he_pju#he1.dat'),
            (beryllium, 0, 'adf15/pec96#be/pec96#be_pju#be0.dat'),
            (beryllium, 1, 'adf15/pec96#be/pec96#be_pju#be1.dat'),
            (beryllium, 2, 'adf15/pec96#be/pec96#be_pju#be2.dat'),
            (beryllium, 3, 'adf15/pec96#be/pec96#be_pju#be3.dat'),
            (carbon, 0, 'adf15/pec96#c/pec96#c_vsu#c0.dat'),
            (carbon, 1, 'adf15/pec96#c/pec96#c_vsu#c1.dat'),
            (carbon, 2, 'adf15/pec96#c/pec96#c_vsu#c2.dat'),
            # (neon, 0, 'adf15/pec96#ne/pec96#ne_pju#ne0.dat'),     #TODO: OPENADAS DATA CORRUPT
            # (neon, 1, 'adf15/pec96#ne/pec96#ne_pju#ne1.dat'),     #TODO: OPENADAS DATA CORRUPT
            (nitrogen, 0, 'adf15/pec96#n/pec96#n_vsu#n0.dat'),
            (nitrogen, 1, 'adf15/pec96#n/pec96#n_vsu#n1.dat'),
            # (nitrogen, 2, 'adf15/pec96#n/pec96#n_vsu#n2.dat'),    #TODO: OPENADAS DATA CORRUPT
        )

    },
    download=True,
    # adas_path='/home/adas/adas/'
)



# install_adf15(hydrogen, 0, 'adf15/pec12#h/pec12#h_pju#h0.dat')
# install_adf15(carbon, 0, 'adf15/pec96#c/pec96#c_vsu#c0.dat')
# install_adf15(carbon, 1, 'adf15/pec96#c/pec96#c_vsu#c1.dat')
# install_adf15(carbon, 2, 'adf15/pec96#c/pec96#c_vsu#c2.dat')


