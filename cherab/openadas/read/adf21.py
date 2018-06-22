# Copyright 2016-2018 Euratom
# Copyright 2016-2018 United Kingdom Atomic Energy Authority
# Copyright 2016-2018 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
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
import numpy as np
from .utility import readvalues


def adf21(file_path):
    """
    Read the given adf21 file data. The output is a dictionary containing all
    the information in this file. The keys and values are the following:
    - DATE: date of calculation (string)
    - CODE: processing code (string)
    - ZT: target ion charge (int)
    - SPEC: target element (string)
    - SVREF: coefficient at reference conditions (float)
    - TREF: reference target temperature (float)
    - EREF: reference beam energy (float)
    - DREF: reference target density (float)
    - TT: target temperature coordinates (1D array)
    - SVT: coefficients at target temperature coordinates (1D array)
    - EB: beam energy coordinates (1D array)
    - DT: target density coordinates (1D array)
    - SV: coefficients at beam energy coordinates (first index) and target
    density coordinates (second index) (2D array)

    :param file_path: path of the adf21 file to read
    :return: a dictionary
    """

    logging.info('Reading ADAS21 or 22 file {}'.format(file_path))

    output = {}

    with open(file_path, 'r') as file:

        line = file.readline()
        output['ZT'] = int(line[3:5])
        output['SVREF'] = float(line[13:22])
        output['SPEC'] = line[29:31]
        output['DATE'] = line[38:46]
        output['CODE'] = line[53:-1]

        file.readline()  # jump the hyphen line

        line = file.readline()
        neb = int(line[1:5])
        ndt = int(line[6:10])
        output['TREF'] = float(line[17:26])

        file.readline()  # jump the hyphen line

        output['EB'] = readvalues(file, neb, 8)
        output['DT'] = readvalues(file, ndt, 8)

        file.readline()  # jump the hyphen line

        sv = np.zeros((neb, ndt))
        for index in range(ndt):
            sv[:, index] = readvalues(file, neb, 8)
        output['SV'] = sv

        file.readline()  # jump the hyphen line

        line = file.readline()
        ntt = int(line[1:5])
        output['EREF'] = float(line[12:21])
        output['DREF'] = float(line[28:37])

        file.readline()  # jump the hyphen line

        output['TT'] = readvalues(file, ntt, 8)

        file.readline()  # jump the hyphen line

        output['SVT'] = readvalues(file, ntt, 8)

    return output
