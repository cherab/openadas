# Copyright 2014-2018 United Kingdom Atomic Energy Authority
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
import urllib
import json
from cherab.core.utility import RecursiveDict
from cherab.openadas.read import *

"""
Utilities for managing the local rate repository.
"""

# todo: make this a configuration option in a json file, add options to setup.py to set them during install
DEFAULT_REPOSITORY_PATH = os.path.expanduser('~/.cherab/openadas/repository')
ADAS_FILE_CACHE = os.path.expanduser('~/.cherab/openadas/download_cache')    # todo: if pointed to ADAS home.... no downloading!
OPENADAS_FILE_URL = 'http://open.adas.ac.uk/download/'


# cherab rate repository will store rates as they are addressed by the interface
# adf files will be "installed" into the repository
# open adas will use a default location if not specified

# e.g. /pec/he/he0.json

# inside file: definition for each line: 1s1 4d1 1D2.0 1s1 2p1 1P1.0

# data will be a json format version of adf structure, but nicer names etc...

# units:
#   temperature: eV
#   density - m^-3
#   rates: photons / m^3 (converts to W/m^3 in rate object)


def install_files(configuration, download=False, repository_path=None, adas_path=None):

    for adf in configuration:
        if adf.lower() == 'adf15':
            for args in configuration[adf]:
                install_adf15(*args, download=download, repository_path=repository_path, adas_path=adas_path)


def install_adf15(element, ionisation, file_path, download=False, repository_path=None, adas_path=None):
    """
    Adds the rates in the ADF15 file to the repository.

    :param element: The element described by the rate file.
    :param ionisation: The ionisation level described by the rate file.
    :param file: Path relative to ADAS root.
    :param download: Attempt to download file if not present (Default=True).
    :return:
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, download, adas_path)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # decode file and write out rates
    rates, wavelengths = read_adf15(element, ionisation, path)
    update_pec_rates(rates, repository_path)
    # todo: update_wavelengths(wavelengths, repository_path)

    print(' - installed!')


def _locate_adas_file(file_path, download=False, adas_path=None):

    path = None

    # is file in adas path?
    if adas_path:
        target = os.path.join(adas_path, file_path)
        if os.path.isfile(target):
            path = target

    # download file?
    if not path and download:
        target = os.path.join(ADAS_FILE_CACHE, file_path)

        # is file in cache? if not download...
        if os.path.isfile(target):
            path = target
        else:

            # create directory structure if missing
            directory = os.path.dirname(target)
            if not os.path.isdir(directory):
                os.makedirs(directory)

            # TODO: move to logging?
            print(" - downloading ADF file '{}' to '{}'".format(file_path, target))

            url = urllib.parse.urljoin(OPENADAS_FILE_URL, file_path.replace('#', '][').lstrip('/'))
            urllib.request.urlretrieve(url, target)
            path = target

    return path


def add_pec_rate(cls, element, ionisation, te, ne, rate):
    pass


def update_pec_rates(rates, repository_path=None):
    """
    PEC rate file structure

    /pec/CLASS/ELEMENT/IONISATION.json
    """

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    for cls, elements in rates.items():
        for element, ionisations in elements.items():
            for ionisation, transitions in ionisations.items():

                # todo: validate class, element, ionisation and rate data

                path = os.path.join(repository_path, 'pec/{}/{}/{}.json'.format(cls, element.symbol.lower(), ionisation))

                # read in any existing rates
                try:
                    with open(path, 'r') as f:
                        content = RecursiveDict.from_dict(json.load(f))
                except FileNotFoundError:
                    content = RecursiveDict()

                # add/replace data for a transition
                for transition in transitions:
                    key = _encode_transition(transition)
                    data = rates[cls][element][ionisation][transition]
                    content[key] = {
                        'te': data['te'].tolist(),
                        'ne': data['ne'].tolist(),
                        'rate': data['rate'].tolist()
                    }

                # create directory structure if missing
                directory = os.path.dirname(path)
                if not os.path.isdir(directory):
                    os.makedirs(directory)

                # read in any existing rates
                with open(path, 'w') as f:
                    json.dump(content, f, indent=2, sort_keys=True)


def _encode_transition(transition):
    """
    Generate a key string from a transition.

    Both integer and string transition descriptions are handled.
    """

    upper, lower = transition

    upper = str(upper).lower()
    lower = str(lower).lower()

    return '{} -> {}'.format(upper, lower)






