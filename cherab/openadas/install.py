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
from cherab.openadas.repository import update_pec_rates, update_wavelengths
from cherab.openadas.read import *

ADAS_DOWNLOAD_CACHE = os.path.expanduser('~/.cherab/openadas/download_cache')
OPENADAS_FILE_URL = 'http://open.adas.ac.uk/download/'


def install_files(configuration, download=False, repository_path=None, adas_path=None):

    for adf in configuration:
        if adf.lower() == 'adf12':
            for args in configuration[adf]:
                install_adf12(*args, download=download, repository_path=repository_path, adas_path=adas_path)
        if adf.lower() == 'adf15':
            for args in configuration[adf]:
                install_adf15(*args, download=download, repository_path=repository_path, adas_path=adas_path)


def install_adf12(donor_ion, receiver_ion, receiver_ionisation, rate_files, download=False, repository_path=None, adas_path=None):
    pass


# todo: move print calls to logging
def install_adf15(element, ionisation, file_path, download=False, repository_path=None, adas_path=None):
    """
    Adds the rates in the ADF15 file to the repository.

    :param element: The element described by the rate file.
    :param ionisation: The ionisation level described by the rate file.
    :param file_path: Path relative to ADAS root.
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
    update_wavelengths(wavelengths, repository_path)

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
        target = os.path.join(ADAS_DOWNLOAD_CACHE, file_path)

        # is file in cache? if not download...
        if os.path.isfile(target):
            path = target
        else:

            # create directory structure if missing
            directory = os.path.dirname(target)
            if not os.path.isdir(directory):
                os.makedirs(directory)

            # TODO: move print to logging
            print(" - downloading ADF file '{}' to '{}'".format(file_path, target))

            url = urllib.parse.urljoin(OPENADAS_FILE_URL, file_path.replace('#', '][').lstrip('/'))
            urllib.request.urlretrieve(url, target)
            path = target

    return path
