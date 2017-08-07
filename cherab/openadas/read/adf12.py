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

import logging
from .utility import readvalues


def adf12(file_path, transition):
    """
    Read the given adf12 file data concerning the given transition. The output
    is a dictionary containing all the information about this transition. The
    keys and values are the following:
    - CODE: processing code (string)
    - DATE: date of calculation (string)
    - DONOR: donor element and state (string)
    - RECEIVER: receiver element (string)
    - TRANSITION: transition (2-tuple of integers)
    - FILE: file name (string)
    - M: ? (string)
    - ISEL: index of the read block in the file (int)
    - QEFREF: qeff at reference conditions (float)
    - EBREF: reference collision energy (float)
    - TIREF: reference ion temperature (float)
    - NIREF: reference ion density (float)
    - ZEREF: reference zeff (float)
    - BREF: reference magnetic field (float)
    - ENER: collision energy coordinates (1D array)
    - QENER: qeff at collision energy coordinates (1D array)
    - TIEV: ion temperature coordinates (1D array)
    - QTIEV: qeff at ion temperature coordinates (1D array)
    - DENSI: ion density coordinates (1D array)
    - QDENSI: qeff at ion density coordinates (1D array)
    - ZEFF: zeff coordinates (1D array)
    - QZEFF: qeff at zeff coordinates (1D array)
    - BMAG: magnetic field coordinates (1D array)
    - QBMAG: qeff at magnetic field coordinates (1D array)

    :param file_path: path of the adf12 file to read
    :param transition: 2-tuple of integers representing an electronic transition
    :return: a dictionary
    """

    logging.info('Reading ADAS12 file {}, transition {}'.format(file_path, transition))

    output = {}

    with open(file_path, 'r') as file:
        n_sel = int(file.readline()[3:5])
        i_sel = 1

        line = file.readline()
        transition_sel = (int(line[38:40]), int(line[41:43]))

        while transition_sel != transition:

            for _ in range(31):  # jump the entire block
                file.readline()

            i_sel += 1
            if i_sel > n_sel:
                raise ValueError("The transition asked does not exist in this file")

            line = file.readline()
            transition_sel = (int(line[38:40]), int(line[41:43]))

        output['CODE'] = line[0:7]
        output['DATE'] = line[8:16]
        output['DONOR'] = line[19:27]
        output['RECEIVER'] = line[30:35]
        output['TRANSITION'] = transition_sel
        output['FILE'] = line[46:53]
        output['M'] = line[56:62]
        output['ISEL'] = int(line[68:70])

        output['QEFREF'] = readvalues(file, 1, 6)[0]
        ebref, tiref, niref, zeref, bref = readvalues(file, 5, 6)
        output['EBREF'] = ebref
        output['TIREF'] = tiref
        output['NIREF'] = niref
        output['ZEREF'] = zeref
        output['BREF'] = bref

        nbeam, nti, ndi, nze, nb = readvalues(file, 5, 6, type=int)
        output['ENER'] = readvalues(file, 24, 6)[0:nbeam]
        output['QENER'] = readvalues(file, 24, 6)[0:nbeam]
        output['TIEV'] = readvalues(file, 12, 6)[0:nti]
        output['QTIEV'] = readvalues(file, 12, 6)[0:nti]
        output['DENSI'] = readvalues(file, 24, 6)[0:ndi]
        output['QDENSI'] = readvalues(file, 24, 6)[0:ndi]
        output['ZEFF'] = readvalues(file, 12, 6)[0:nze]
        output['QZEFF'] = readvalues(file, 12, 6)[0:nze]
        output['BMAG'] = readvalues(file, 12, 6)[0:nb]
        output['QBMAG'] = readvalues(file, 12, 6)[0:nb]

    return output
