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
import json
import numpy as np

from cherab.core.atomic import Element
from cherab.core.utility import RecursiveDict
from .utility import DEFAULT_REPOSITORY_PATH, valid_charge


def add_ionisation_rate(species, charge, rate, repository_path=None):
    """
    Adds a single ionisation rate to the repository.

    If adding multiple rates, consider using the update_ionisation_rates()
    function instead. The update function avoids repeatedly opening and closing
    the rate files.

    :param repository_path:
    :return:
    """

    update_ionisation_rates({
        species: {
            charge: rate
        }
    }, repository_path)


def update_ionisation_rates(rates, repository_path=None):
    """
    Ionisation rate file structure

    /ionisation/<species>.json

    File contains multiple rates, indexed by the ion charge state.
    """

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    for species, rate_data in rates.items():

        # sanitise and validate arguments
        if not isinstance(species, Element):
            raise TypeError('The species must be an Element object.')

        path = os.path.join(repository_path, 'ionisation/{}.json'.format(species.symbol.lower()))

        _update_and_write_adf11(species, rate_data, path)


def add_recombination_rate(species, charge, rate, repository_path=None):
    """
    Adds a single recombination rate to the repository.

    If adding multiple rates, consider using the update_recombination_rates()
    function instead. The update function avoids repeatedly opening and closing
    the rate files.

    :param repository_path:
    :return:
    """

    update_recombination_rates({
        species: {
            charge: rate
        }
    }, repository_path)


def update_recombination_rates(rates, repository_path=None):
    """
    Ionisation rate file structure

    /recombination/<species>.json

    File contains multiple rates, indexed by the ion charge state.
    """

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    for species, rate_data in rates.items():

        # sanitise and validate arguments
        if not isinstance(species, Element):
            raise TypeError('The species must be an Element object.')

        path = os.path.join(repository_path, 'recombination/{}.json'.format(species.symbol.lower()))

        _update_and_write_adf11(species, rate_data, path)


def add_thermalchargeexchange_rate(species, charge, rate, repository_path=None):
    """
    Adds a single thermal charge exchange rate to the repository.

    If adding multiple rates, consider using the update_recombination_rates()
    function instead. The update function avoids repeatedly opening and closing
    the rate files.

    :param repository_path:
    :return:
    """

    update_thermalchargeexchange_rates({
        species: {
            charge: rate
        }
    }, repository_path)


def update_thermalchargeexchange_rates(rates, repository_path=None):
    """
    Thermal charge exchange rate file structure

    /recombination/<species>.json

    File contains multiple rates, indexed by the ion charge state.
    """

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    for species, rate_data in rates.items():

        # sanitise and validate arguments
        if not isinstance(species, Element):
            raise TypeError('The species must be an Element object.')

        path = os.path.join(repository_path, 'thermalchargeexchange/{}.json'.format(species.symbol.lower()))

        _update_and_write_adf11(species, rate_data, path)


def _update_and_write_adf11(species, rate_data, path):

        # read in any existing rates
        try:
            with open(path, 'r') as f:
                content = RecursiveDict.from_dict(json.load(f))
        except FileNotFoundError:
            content = RecursiveDict()

        for charge, rates in rate_data.items():

            if not valid_charge(species, charge):
                raise ValueError('Charge state is larger than the number of protons in the specified species.')

            # sanitise and validate rate data
            te = np.array(rates['te'], np.float64)
            ne = np.array(rates['ne'], np.float64)
            rate_table = np.array(rates['rates'], np.float64)

            if ne.ndim != 1:
                raise ValueError('Density array must be a 1D array.')

            if te.ndim != 1:
                raise ValueError('Temperature array must be a 1D array.')

            if (ne.shape[0], te.shape[0]) != rate_table.shape:
                raise ValueError('Electron temperature, density and rate data arrays have inconsistent sizes.')

            # update file content with new rate
            content[charge] = {
                'te': te.tolist(),
                'ne': ne.tolist(),
                'rate': rate_table.tolist(),
            }

            # create directory structure if missing
            directory = os.path.dirname(path)
            if not os.path.isdir(directory):
                os.makedirs(directory)

            # write new data
            with open(path, 'w') as f:
                json.dump(content, f, indent=2, sort_keys=True)


def get_ionisation_rate(element, charge, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    path = os.path.join(repository_path, 'ionisation/{}.json'.format(element.symbol.lower()))
    try:
        with open(path, 'r') as f:
            content = json.load(f)
        d = content[str(charge)]
    except (FileNotFoundError, KeyError):
        print()
        print(path)
        raise RuntimeError('Requested ionisation rate (element={}, charge={})'
                           ' is not available.'.format(element.symbol, charge))

    # convert to numpy arrays
    d['ne'] = np.array(d['ne'], np.float64)
    d['te'] = np.array(d['te'], np.float64)
    d['rate'] = np.array(d['rate'], np.float64)

    return d


def get_recombination_rate(element, charge, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    path = os.path.join(repository_path, 'recombination/{}.json'.format(element.symbol.lower()))
    try:
        with open(path, 'r') as f:
            content = json.load(f)
        d = content[str(charge)]
    except (FileNotFoundError, KeyError):
        raise RuntimeError('Requested recombination rate (element={}, charge={})'
                           ' is not available.'.format(element.symbol, charge))

    # convert to numpy arrays
    d['ne'] = np.array(d['ne'], np.float64)
    d['te'] = np.array(d['te'], np.float64)
    d['rate'] = np.array(d['rate'], np.float64)

    return d


def get_thermalchargeexchange_rate(element, charge, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH

    path = os.path.join(repository_path, 'thermalchargeexchange/{}.json'.format(element.symbol.lower()))
    try:
        with open(path, 'r') as f:
            content = json.load(f)
        d = content[str(charge)]
    except (FileNotFoundError, KeyError):
        raise RuntimeError('Requested recombination rate (element={}, charge={})'
                           ' is not available.'.format(element.symbol, charge))

    # convert to numpy arrays
    d['ne'] = np.array(d['ne'], np.float64)
    d['te'] = np.array(d['te'], np.float64)
    d['rate'] = np.array(d['rate'], np.float64)

    return d
