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


def read_adf12(donor_ion, receiver_ion, receiver_ionisation, donor_metastable, adf_file_path):
    """
    Opens and parses ADAS ADF12 data files.

    :param donor_ion: The donor ion element described by the rate file.
    :param receiver_ion: The receiver ion element described by the rate file.
    :param receiver_ionisation: The receiver ion ionisation level described by the rate file.
    :param adf_file_path: Path to ADF15 file from ADAS root.
    :return: Dictionary containing rates.
    """

    rates = RecursiveDict()

    with open(adf_file_path, 'r') as file:

        rate_count = int(file.readline()[3:5])
        for i in range(rate_count):

            # parse block
            transition, rate = _parse_block(file)

            # add to repository update dictionary, converting density from cm^-3 to m^-3
            rates[donor_ion][receiver_ion][receiver_ionisation][transition][donor_metastable] = {
                'eb': np.array(rate['ENER'], np.float64),
                'ti': np.array(rate['TIEV'], np.float64),
                'ni': PerCm3ToPerM3.to(np.array(rate['DENSI'], np.float64)),
                'z': np.array(rate['ZEFF'], np.float64),
                'b': np.array(rate['BMAG'], np.float64),

                'qeb': np.array(rate['QENER'], np.float64),
                'qti': np.array(rate['QTIEV'], np.float64),
                'qni': Cm3ToM3.to(np.array(rate['QDENSI'], np.float64)),
                'qz': np.array(rate['QZEFF'], np.float64),
                'qb': np.array(rate['QBMAG'], np.float64),

                'ebref': float(rate['EBREF']),
                'tiref': float(rate['TIREF']),
                'niref': PerCm3ToPerM3.to(float(rate['NIREF'])),
                'zref': float(rate['ZEREF']),
                'bref': float(rate['BREF']),
                'qref': Cm3ToM3.to(float(rate['QEFREF']))
            }

    return rates



def _parse_block(file):
    """
    Reads and parses an ADF12 rate block from an IO stream.

    :param file: Text stream seeked to the start of the block.
    :return: Tuple containing (transition tuple, rate data dictionary).
    """

    # header
    line = file.readline()
    transition = (int(line[38:40]), int(line[41:43]))

    rate = {}

    # reference value section
    rate['QEFREF'] = _readvalues(file, 1, 6)[0]
    ebref, tiref, niref, zeref, bref = _readvalues(file, 5, 6)
    rate['EBREF'] = ebref
    rate['TIREF'] = tiref
    rate['NIREF'] = niref
    rate['ZEREF'] = zeref
    rate['BREF'] = bref

    # rate data section
    nbeam, nti, ndi, nze, nb = _readvalues(file, 5, 6, type=int)
    rate['ENER'] = _readvalues(file, 24, 6)[0:nbeam]
    rate['QENER'] = _readvalues(file, 24, 6)[0:nbeam]
    rate['TIEV'] = _readvalues(file, 12, 6)[0:nti]
    rate['QTIEV'] = _readvalues(file, 12, 6)[0:nti]
    rate['DENSI'] = _readvalues(file, 24, 6)[0:ndi]
    rate['QDENSI'] = _readvalues(file, 24, 6)[0:ndi]
    rate['ZEFF'] = _readvalues(file, 12, 6)[0:nze]
    rate['QZEFF'] = _readvalues(file, 12, 6)[0:nze]
    rate['BMAG'] = _readvalues(file, 12, 6)[0:nb]
    rate['QBMAG'] = _readvalues(file, 12, 6)[0:nb]

    return transition, rate


def _readvalues(file, nb_values, values_per_line, type=float):
    """
    Read and return a given number of values in a file, taking into account
    end of lines. The reading begins at the current read line of the file (which
    must be open to use this function). The read lines of the file are assumed
    to be shaped as following:
    a first useless character, then a given number of 10 characters values, and
    any other characters after (not read).

    :param file: file in which values have to be read
    :param nb_values: number of values to be read
    :param values_per_line: number of values per line on the file
    :param type: python type of the values to be returned
    :return: a numpy 1D array with the read values in the reading order.
    """
    nb_read = 0
    output = []

    while nb_read < nb_values:
        nb_read_line = nb_read % values_per_line
        if nb_read_line == 0:
            line = file.readline()

        output.append(type(line[1+nb_read_line*10:(nb_read_line+1)*10].replace('D', 'E')))
        nb_read += 1

    return np.array(output)