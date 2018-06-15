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
import json
import numpy as np
from cherab.core.utility import RecursiveDict

"""
Utilities for managing the local rate repository.
"""

# todo: make this a configuration option in a json file, add options to setup.py to set them during install
DEFAULT_REPOSITORY_PATH = os.path.expanduser('~/.cherab/openadas/repository')

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


# def add_pec_rate(cls, element, ionisation, te, ne, rate):
#     pass


# todo: add error handling
def update_wavelengths(wavelengths, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    for element, ionisations in wavelengths.items():
        for ionisation, transitions in ionisations.items():

            # todo: validate element, ionisation and wavelength data

            path = os.path.join(repository_path, 'wavelength/{}/{}.json'.format(element.symbol.lower(), ionisation))

            # read in any existing wavelengths
            try:
                with open(path, 'r') as f:
                    content = RecursiveDict.from_dict(json.load(f))
            except FileNotFoundError:
                content = RecursiveDict()

            # add/replace data for a transition
            for transition in transitions:
                key = _encode_transition(transition)
                content[key] = wavelengths[element][ionisation][transition]

            # create directory structure if missing
            directory = os.path.dirname(path)
            if not os.path.isdir(directory):
                os.makedirs(directory)

            # write new data
            with open(path, 'w') as f:
                json.dump(content, f, indent=2, sort_keys=True)


# todo: add error handling
def get_wavelength(element, ionisation, transition, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH
    path = os.path.join(repository_path, 'wavelength/{}/{}.json'.format(element.symbol.lower(), ionisation))
    with open(path, 'r') as f:
        content = json.load(f)
    return content[_encode_transition(transition)]


# todo: add error handling
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

                # write new data
                with open(path, 'w') as f:
                    json.dump(content, f, indent=2, sort_keys=True)


def get_pec_excitation_rate(element, ionisation, transition, repository_path=None):
    return _get_pec_rate('excitation', element, ionisation, transition, repository_path)


def get_pec_recombination_rate(element, ionisation, transition, repository_path=None):
    return _get_pec_rate('recombination', element, ionisation, transition, repository_path)


# todo: add error handling
def _get_pec_rate(cls, element, ionisation, transition, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH
    path = os.path.join(repository_path, 'pec/{}/{}/{}.json'.format(cls, element.symbol.lower(), ionisation))
    with open(path, 'r') as f:
        content = json.load(f)

    # extract raw rate data
    d = content[_encode_transition(transition)]

    # convert to numpy arrays
    d['ne'] = np.array(d['ne'], np.float64)
    d['te'] = np.array(d['te'], np.float64)
    d['rate'] = np.array(d['rate'], np.float64)

    return d


def _encode_transition(transition):
    """
    Generate a key string from a transition.

    Both integer and string transition descriptions are handled.
    """

    upper, lower = transition

    upper = str(upper).lower()
    lower = str(lower).lower()

    return '{} -> {}'.format(upper, lower)






