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

import os
import urllib.request

from .library.adf15 import _ADF15_FILES_BY_FILENAME
from .read.adf15 import add_adf15_to_atomic_data
from cherab.core.utility.recursivedict import RecursiveDict


_RATE_TYPE_CONVERTER = {'excitation': 'Excitation', 'recombination': 'Recombination', 'cx_thermal': 'Thermal Charge Exchange (CX)'}


def print_available_adf15_rates(adf_file):
    """
    Prints a list of available transitions for which rate data are available, sorted by wavelength.

    :param str adf_file: The ADF file name or ADAS library path of interest.
    """

    adf_file_record = identify_adf_file(adf_file)

    absolute_file_path = check_for_adf_file(adf_file_record["ADAS_Path"], adf_file_record["Download_URL"])

    element = adf_file_record['Element']
    ionisation = adf_file_record['Ionisation']
    atomic_data_dictionary = add_adf15_to_atomic_data(RecursiveDict(), element, ionisation, absolute_file_path).freeze()

    for rate_type in ('excitation', 'recombination', 'cx_thermal'):

        try:
            atomic_data_dictionary[rate_type]
        except KeyError:
            print()
            print("No '{}' rate data available in adf file '{}'.".format(rate_type, os.path.split(adf_file)[1]))
            continue

        print()
        print("Rate type: {}".format(_RATE_TYPE_CONVERTER[rate_type]))
        transitions = atomic_data_dictionary[rate_type][element][ionisation].keys()
        pairs = [(atomic_data_dictionary['wavelength'][element][ionisation][transition], transition) for transition in transitions]
        pairs.sort(key=lambda x: x[0])
        for wavelength, transition in pairs:
            print("  {:.6g}nm -> {}".format(wavelength, transition))


def identify_adf_file(adf_file):
    """
    Returns the record dictionary for a known ADF file in the CHERAB OpenADAS preferred library.

    :param str adf_file: The ADF file name or ADAS library path of interest.
    :return: A dictionary with the ADF file's meta data.
    """

    adf_file_name = os.path.split(adf_file)[1]

    try:
        return _ADF15_FILES_BY_FILENAME[adf_file_name]
    except KeyError:
        raise ValueError("The specified ADAS file '{}' is not in the standard CHERAB OpenADAS ADF file library."
                         "".format(adf_file))


def check_for_adf_file(adf_file_path, download_path):
    """
    Checks the specified ADF file is available on local disk, otherwise it tries to download the ADF file.

    :param str adf_file_path: The path to the ADF file
    :param str download_path: The url to use for downloading the ADF file if it isn't found locally.
    :return:
    """

    data_path=os.path.expanduser('~/.cherab/openadas')

    # check to see if this is already a absolute path to an ADF file
    if os.path.exists(adf_file_path):
        return adf_file_path

    relative_adf_directory, adf_file_name = os.path.split(adf_file_path)
    absolute_adf_directory = os.path.join(data_path, relative_adf_directory)
    absolute_file_path = os.path.join(absolute_adf_directory, adf_file_name)

    if not os.path.exists(absolute_adf_directory):
        os.makedirs(absolute_adf_directory)

    if os.path.isfile(absolute_file_path):
        return absolute_file_path
    else:
        # TODO - catch urllib exceptions and return nicer error to user
        print("Downloading ADF file - '{}' to '~/.cherab/openadas'".format(adf_file_path))
        urllib.request.urlretrieve(download_path, absolute_file_path)

    return absolute_file_path

