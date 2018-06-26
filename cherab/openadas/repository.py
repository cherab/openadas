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
from cherab.core.atomic import Element

"""
Utilities for managing the local rate repository.
"""

# todo: make this a configuration option in a json file, add options to setup.py to set them during install
DEFAULT_REPOSITORY_PATH = os.path.expanduser('~/.cherab/openadas/repository')


def update_wavelengths(wavelengths, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    for element, ionisations in wavelengths.items():
        for ionisation, transitions in ionisations.items():

            # sanitise and validate
            if not isinstance(element, Element):
                raise TypeError('The element must be an Element object.')

            if not _valid_ionisation(element, ionisation):
                raise ValueError('Ionisation level is larger than the number of protons in the element.')

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
                content[key] = float(wavelengths[element][ionisation][transition])

            # create directory structure if missing
            directory = os.path.dirname(path)
            if not os.path.isdir(directory):
                os.makedirs(directory)

            # write new data
            with open(path, 'w') as f:
                json.dump(content, f, indent=2, sort_keys=True)


def get_wavelength(element, ionisation, transition, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH
    path = os.path.join(repository_path, 'wavelength/{}/{}.json'.format(element.symbol.lower(), ionisation))
    try:
        with open(path, 'r') as f:
            content = json.load(f)
        return content[_encode_transition(transition)]
    except (FileNotFoundError, KeyError):
        raise RuntimeError('Requested wavelength (element={}, ionisation={}, transition={})'
                           ' is not available.'.format(element.symbol, ionisation, transition))


def update_beam_cx_rates(rates, repository_path=None):
    # organisation in repository:
    #   beam/cx/donor_ion/receiver_ion/receiver_ionisation.json
    # inside json file:
    #   transition: [list of donor_metastables with rates]

    def sanitise_and_validate(data, x_key, x_name, y_key, y_name):
        """
        Sanitises and validates pairs of rate data arrays.

        Converts arrays to numpy arrays and check that the dimensions of the
        supplied data are consistent.

        Arrays are converted in place, the supplied dictionary is modified.

        :param data: Rate data dictionary.
        :param x_key: Key of independent variable data.
        :param x_name: Name of data array for error reporting.
        :param y_key: Key of dependent variable data.
        :param y_name: Name of data array for error reporting.
        """

        # convert to numpy arrays
        data[x_key] = np.array(data[x_key], np.float64)
        data[y_key] = np.array(data[y_key], np.float64)

        # check dimensions
        if data[x_key].ndim != 1:
            raise ValueError('The {} array must be a 1D array.'.format(x_name))

        if data[y_key].ndim != 1:
            raise ValueError('The {} array must be a 1D array.'.format(y_name))

        if data[x_key].shape != data[y_key].shape:
            raise ValueError('The {} and {} arrays have inconsistent lengths.'.format(x_name, y_name))

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    for donor, receivers in rates.items():
        for receiver, ionisations in receivers.items():
            for ionisation, transitions in ionisations.items():

                # sanitise and validate
                if not isinstance(donor, Element):
                    raise TypeError('The element must be an Element object.')

                if not isinstance(receiver, Element):
                    raise TypeError('The element must be an Element object.')

                if not _valid_ionisation(receiver, ionisation):
                    raise ValueError('Ionisation level is larger than the number of protons in the element.')

                path = os.path.join(repository_path, 'beam/cx/{}/{}/{}.json'.format(donor.symbol.lower(), receiver.symbol.lower(), ionisation))

                # read in any existing rates
                try:
                    with open(path, 'r') as f:
                        content = RecursiveDict.from_dict(json.load(f))
                except FileNotFoundError:
                    content = RecursiveDict()

                # json keys are strings, must convert metastable key to integer
                for transition, metastables in content.items():
                    content[transition] = RecursiveDict({int(metastable): rate for metastable, rate in metastables.items()})

                # update content
                for transition, metastables in transitions.items():

                    # add/replace data for each metastable
                    transition_key = _encode_transition(transition)
                    for metastable in metastables:

                        if not metastable >= 0:
                            raise ValueError('Donor metastable level cannot be less than zero.')

                        data = rates[donor][receiver][ionisation][transition][metastable]

                        # sanitise/validate data
                        data['qref'] = float(data['qref'])
                        sanitise_and_validate(data, 'eb', 'beam energy', 'qeb', 'beam energy effective rate')
                        sanitise_and_validate(data, 'ti', 'ion temperature', 'qti', 'ion temperature effective rate')
                        sanitise_and_validate(data, 'ni', 'ion density', 'qni', 'ion density effective rate')
                        sanitise_and_validate(data, 'z', 'Zeff', 'qz', 'Zeff effective rate')
                        sanitise_and_validate(data, 'b', 'B-field magnitude', 'qb', 'B-field magnitude effective rate')

                        content[transition_key][metastable] = {
                            'eb': data['eb'].tolist(),
                            'ti': data['ti'].tolist(),
                            'ni': data['ni'].tolist(),
                            'z': data['z'].tolist(),
                            'b': data['b'].tolist(),
                            'qref': data['qref'],
                            'qeb': data['qeb'].tolist(),
                            'qti': data['qti'].tolist(),
                            'qni': data['qni'].tolist(),
                            'qz': data['qz'].tolist(),
                            'qb': data['qb'].tolist(),
                        }

                # create directory structure if missing
                directory = os.path.dirname(path)
                if not os.path.isdir(directory):
                    os.makedirs(directory)

                # write new data
                with open(path, 'w') as f:
                    json.dump(content, f, indent=2, sort_keys=True)


def get_beam_cx_rates(donor_ion, receiver_ion, receiver_ionisation, transition, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH
    path = os.path.join(repository_path, 'beam/cx/{}/{}/{}.json'.format(donor_ion.symbol.lower(), receiver_ion.symbol.lower(), receiver_ionisation))
    try:
        with open(path, 'r') as f:
            content = json.load(f)
        rates = content[_encode_transition(transition)]
    except (FileNotFoundError, KeyError):
        raise RuntimeError('Requested beam CX effective emission rates (donor={}, receiver={}, ionisation={}, transition={})'
                           ' are not available.'.format(donor_ion.symbol, receiver_ion.symbol, receiver_ionisation, transition))

    # sanitise data and convert to (more useful) numpy arrays rather than lists
    for rate in rates.values():
        rate['eb'] = np.array(rate['eb'], np.float64)
        rate['ti'] = np.array(rate['ti'], np.float64)
        rate['ni'] = np.array(rate['ni'], np.float64)
        rate['z'] = np.array(rate['z'], np.float64)
        rate['b'] = np.array(rate['b'], np.float64)
        rate['qref'] = float(rate['qref'])
        rate['qeb'] = np.array(rate['qeb'], np.float64)
        rate['qti'] = np.array(rate['qti'], np.float64)
        rate['qni'] = np.array(rate['qni'], np.float64)
        rate['qz'] = np.array(rate['qz'], np.float64)
        rate['qb'] = np.array(rate['qb'], np.float64)

    return [(int(metastable), rate) for metastable, rate in rates.items()]


def update_pec_rates(rates, repository_path=None):
    """
    PEC rate file structure

    /pec/CLASS/ELEMENT/IONISATION.json
    """

    valid_classes = [
        'excitation',
        'recombination',
        'thermalcx'
    ]

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    for cls, elements in rates.items():
        for element, ionisations in elements.items():
            for ionisation, transitions in ionisations.items():

                # sanitise and validate
                cls = cls.lower()
                if cls not in valid_classes:
                    raise ValueError('Unrecognised pec rate class \'{}\'.'.format(cls))

                if not isinstance(element, Element):
                    raise TypeError('The element must be an Element object.')

                if not _valid_ionisation(element, ionisation):
                    raise ValueError('Ionisation level is larger than the number of protons in the element.')

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

                    # sanitise/validate data
                    data['ne'] = np.array(data['ne'], np.float64)
                    data['te'] = np.array(data['te'], np.float64)
                    data['rate'] = np.array(data['rate'], np.float64)

                    if data['ne'].ndim != 1:
                        raise ValueError('Density array must be a 1D array.')

                    if data['te'].ndim != 1:
                        raise ValueError('Temperature array must be a 1D array.')

                    if (data['ne'].shape[0], data['te'].shape[0]) != data['rate'].shape:
                        raise ValueError('Density, temperature and rate data arrays have inconsistent sizes.')

                    content[key] = {
                        'ne': data['ne'].tolist(),
                        'te': data['te'].tolist(),
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


def get_pec_thermalcx_rate(element, ionisation, transition, repository_path=None):
    return _get_pec_rate('thermalcx', element, ionisation, transition, repository_path)


def _get_pec_rate(cls, element, ionisation, transition, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH
    path = os.path.join(repository_path, 'pec/{}/{}/{}.json'.format(cls, element.symbol.lower(), ionisation))
    try:
        with open(path, 'r') as f:
            content = json.load(f)
        d = content[_encode_transition(transition)]
    except (FileNotFoundError, KeyError):
        raise RuntimeError('Requested PEC rate (class={}, element={}, ionisation={}, transition={})'
                           ' is not available.'.format(cls, element.symbol, ionisation, transition))

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


def _valid_ionisation(element, ionisation):
    """
    Returns true if the element can be ionised to the specified level.

    :param ionisation: Integer ionisation level.
    :return: True/False.
    """
    return ionisation <= element.atomic_number



