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

import numpy as np
from cherab.core.utility import RecursiveDict
from cherab.core.utility.conversion import Cm3ToM3, PerCm3ToPerM3
from .utility import readvalues


def parse_adf21(beam_species, target_ion, target_ionisation, adf_file_path):

    rate = RecursiveDict()
    with open(adf_file_path, 'r') as file:
        raw = _parse_rate(file)

    # add to repository update dictionary, converting density from cm^-3 to m^-3
    rate[beam_species][target_ion][target_ionisation] = {
        'e': np.array(raw['EB'], np.float64),
        'n': PerCm3ToPerM3.to(np.array(raw['DT'], np.float64)),
        't': np.array(raw['TT'], np.float64),

        'sen': Cm3ToM3.to(np.array(raw['SV'], np.float64)),
        'st': np.array(raw['SVT'], np.float64),

        'eref': raw['EREF'],
        'nref': PerCm3ToPerM3.to(raw['NREF']),
        'tref': raw['TREF'],
        'sref': raw['SREF']
    }

    return rate


def _parse_rate(file):
    """
    Read from the given adf21/22 file stream.

    The output is a dictionary containing all the information in this file.
    The keys and values are the following:

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

    :param file: A file stream.
    :return: a dictionary
    """

    output = {}

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
