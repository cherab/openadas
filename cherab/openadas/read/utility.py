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


import numpy as np


def readvalues(file, nb_values, values_per_line, type=float):
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