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
import re

import numpy as np

# from cherab.openadas.rates import PEC

PEC_INDEX_HEADER_MATCH = '^C\s*[A-Z]*\s*[A-Z]*\s*[A-Z]*\s*[A-Z]*$'
PEC_TRANSITION_MATCH = '^C\s*([0-9]*)\.\s*([0-9]*\.[0-9])\s*N=\s*([0-9]*).*N=\s*([0-9]*)\s*([A-Z]*)$'
WAVELENGTH_MATCH = '^\s*[0-9]*\.[0-9] ?A .*$'
BLOCK_ID_MATCH = '^\s*[0-9]*\.[0-9] ?A\s*([0-9]*)\s*([0-9]*).*/TYPE = ([a-zA-Z]*).*/ISEL *= * ([0-9]*)$'


# Group lines of file into blocks based on precursor '  6561.9A   24...'
def _group_by_block(source_file, match_string):
    buffer = []
    for line in source_file:
        if re.match(match_string, line):
            if buffer:
                yield buffer
            buffer = [line]
        else:
            buffer.append(line)
    yield buffer


# TODO - re-add optional validation
def adf15(file_name, block_num):

    with open(file_name, "r") as adf15_file:
        for block in _group_by_block(adf15_file, WAVELENGTH_MATCH):
            match = re.match(BLOCK_ID_MATCH, block[0])

            if not match:
                continue

            if int(match.groups()[3]) == block_num:
                # get number of n and T data points:
                num_n = int(match.groups()[0])
                num_t = int(match.groups()[1])

                block.pop(0)

                # Load density values
                nn = 0
                density = []
                while nn != num_n:
                    next_line = block.pop(0)
                    components = next_line.split()
                    for value in components:
                        nn += 1
                        density.append(float(value))

                # Load temperature values
                nt = 0
                temperature = []
                while nt != num_t:
                    next_line = block.pop(0)
                    components = next_line.split()
                    for value in components:
                        nt += 1
                        temperature.append(float(value))

                # Loop over the remaining lines in the block
                rates = []
                while block:
                    next_line = block.pop(0)
                    components = next_line.split()
                    for value in components:
                        rates.append(float(value))

                if len(rates) != num_n * num_t:
                    raise RuntimeError('The input file {} is invalid. Number of rate values must equal num_density * '
                                       'num_temperature values.'.format(file_name))

                density = np.array(density)
                temperature = np.array(temperature)
                rates = np.array(rates)
                rates = rates.reshape((num_n, num_t))

                return {'DENS': density, 'TE': temperature, 'PEC': rates}

        # If code gets to here, block wasn't found.
        raise RuntimeError('Block number {} was not found in ADF15 file {}.'.format(block_num, file_name))


