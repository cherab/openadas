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


import re
import numpy as np
from cherab.core.atomic import hydrogen


PEC_INDEX_HEADER_MATCH = '^C\s*ISEL\s*WAVELENGTH\s*TRANSITION\s*TYPE'
CONFIGURATION_HEADER_MATCH = '^C\s*Configuration\s*\(2S\+1\)L\(w-1/2\)\s*Energy \(cm\*\*-1\)$'

CONFIGURATION_STRING_MATCH = "^C\s*([0-9]*)\s*((?:[0-9][SPDFG][0-9]\s)*)\s*\(([0-9]*\.?[0-9]*)\)([0-9]*)\(\s*([0-9]*\.?[0-9]*)\)"

PEC_N_TRANSITION_MATCH = '^C\s*([0-9]*)\.\s*([0-9]*\.[0-9])\s*N=\s*([0-9]*).*N=\s*([0-9]*)\s*([A-Z]*)$'
PEC_HYDROGEN_TRANSITION_MATCH = '^C\s*([0-9]*)\.\s*([0-9]*\.[0-9]*)\s*N=\s*([0-9]*) - N=\s*([0-9]*)\s*([A-Z]*)'
PEC_FULL_TRANSITION_MATCH = '^C\s*([0-9]*)\.\s*([0-9]*\.[0-9])\s*([0-9]*)[\(\)\.0-9\s]*-\s*([0-9]*)[\(\)\.0-9\s]*([A-Z]*)'
WAVELENGTH_MATCH = '^\s*[0-9]*\.[0-9] ?A .*$'
BLOCK_ID_MATCH = '^\s*[0-9]*\.[0-9] ?A\s*([0-9]*)\s*([0-9]*).*/TYPE = ([a-zA-Z]*).*/ISEL *= * ([0-9]*)$'

_L_LOOKUP = {
    0: 'S',
    1: 'P',
    2: 'D',
    3: 'F',
    4: 'G',
    5: 'H',
    6: 'I',
    7: 'K',
    8: 'L',
    9: 'M',
    10: 'N',
    11: 'O',
    12: 'Q',
    13: 'R',
}


def add_adf15_to_atomic_data(atomic_data_dictionary, element, ionisation, adf_file_path):

    adf15_file = open(adf_file_path, "r")
    lines = adf15_file.readlines()

    # Use simple electron configuration structure for hydrogen
    if element == hydrogen:

        while not re.match(PEC_INDEX_HEADER_MATCH, lines[0]):
            lines.pop(0)
        index_lines = lines

        for i in range(len(index_lines)):

            match = re.match(PEC_HYDROGEN_TRANSITION_MATCH, index_lines[i])
            if not match:
                continue

            block_num = int(match.groups()[0])
            wavelength = float(match.groups()[1])/10
            upper_level = int(match.groups()[2])
            lower_level = int(match.groups()[3])
            rate_type_adas = match.groups()[4]
            if rate_type_adas == 'EXCIT':
                rate_type = 'excitation'
            elif rate_type_adas == 'RECOM':
                rate_type = 'recombination'
            elif rate_type_adas == 'CHEXC':
                rate_type = 'cx_thermal'
            else:
                raise ValueError("Unrecognised rate type - {}".format(rate_type_adas))

            atomic_data_dictionary[rate_type][element][ionisation][(upper_level, lower_level)] = (adf_file_path, block_num)
            atomic_data_dictionary["wavelength"][element][ionisation][(upper_level, lower_level)] = wavelength

    # Use full electron configuration structure for anything else
    else:

        configuration_lines = []
        configuration_dict = {}

        while not re.match(CONFIGURATION_HEADER_MATCH, lines[0]):
            lines.pop(0)
        while not re.match(PEC_INDEX_HEADER_MATCH, lines[0]):
            configuration_lines.append(lines[0])
            lines.pop(0)
        index_lines = lines

        for i in range(len(configuration_lines)):

            match = re.match(CONFIGURATION_STRING_MATCH, configuration_lines[i])
            if not match:
                continue

            config_id = int(match.groups()[0])
            electron_configuration = match.groups()[1].rstrip().lower()
            spin_multiplicity = match.groups()[2]  # (2S+1)
            total_orbital_quantum_number = _L_LOOKUP[int(match.groups()[3])]  # L
            total_angular_momentum_quantum_number = match.groups()[4]  # J

            configuration_dict[config_id] = (electron_configuration + " " + spin_multiplicity +
                                             total_orbital_quantum_number + total_angular_momentum_quantum_number)

        for i in range(len(index_lines)):

            match = re.match(PEC_FULL_TRANSITION_MATCH, index_lines[i])
            if not match:
                continue

            block_num = int(match.groups()[0])
            wavelength = float(match.groups()[1])/10
            upper_level_id = int(match.groups()[2])
            upper_level = configuration_dict[upper_level_id]
            lower_level_id = int(match.groups()[3])
            lower_level = configuration_dict[lower_level_id]
            rate_type_adas = match.groups()[4]
            if rate_type_adas == 'EXCIT':
                rate_type = 'excitation'
            elif rate_type_adas == 'RECOM':
                rate_type = 'recombination'
            elif rate_type_adas == 'CHEXC':
                rate_type = 'cx_thermal'
            else:
                raise ValueError("Unrecognised rate type - {}".format(rate_type_adas))

            atomic_data_dictionary[rate_type][element][ionisation][(upper_level, lower_level)] = (adf_file_path, block_num)
            atomic_data_dictionary["wavelength"][element][ionisation][(upper_level, lower_level)] = wavelength

    return atomic_data_dictionary


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
