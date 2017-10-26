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

from cherab.core import AtomicData, Isotope
from pkg_resources import resource_filename

from cherab.openadas.read import adf12, adf15, adf21, adf22
from . import config
from .rates import *


class OpenADAS(AtomicData):

    def __init__(self, data_path=None, config=config.default, permit_extrapolation=False):

        super().__init__()
        self._data_path = self._locate_data(data_path)

        # configuration is immutable, changes to ADAS state are not tracked
        self._config = config.copy()

        # if true informs interpolation objects to allow extrapolation beyond the limits of the tabulated data
        self._permit_extrapolation = permit_extrapolation

    @property
    def config(self):
        # configuration is immutable, changes to ADAS state are not tracked
        return self._config.copy()

    @property
    def data_path(self):
        return self._data_path

    def _locate_data(self, data_path):

        if data_path is None:

            # todo: rework this handling to provide an order of precedence / more sensible options
            #       user home directory ~/.cherab/openadas/data/ ?
            #       add a config.rc to the package to configure default search paths / autodownload
            #       change this code so all data readers try each  location in turn?
            #       add an auto-download option to auto-download adas files from openadas

            # local copy of adas data
            # search_paths = [resource_filename("cherab", "/openadas/data")]
            search_paths = []

            # adas home directory
            try:
                search_paths.append(os.path.join(os.environ["ADASHOME"], "adas"))
            except KeyError:
                search_paths.append("/home/adas/adas")

            search_paths.append(os.path.expanduser('~/.cherab/openadas'))

            for path in search_paths:
                if os.path.isdir(path):
                    data_path = path
                    break
            else:
                raise IOError("Could not find the Open-ADAS data directory.")

        return data_path

    def wavelength(self, ion, ionisation, transition):
        """
        :param ion: Element object defining the ion type.
        :param transition: Tuple containing (initial level, final level)
        :return: Wavelength in nanometers.
        """

        try:
            return self._config["wavelength"][ion][ionisation][transition]
        except KeyError:
            raise RuntimeError("The requested wavelength data for ({}, {}, {}) is not available.".format(ion.symbol, ionisation, transition))

    def beam_cx_rate(self, donor_ion, receiver_ion, receiver_ionisation, transition):

        wavelength = self.wavelength(receiver_ion, receiver_ionisation - 1, transition)

        # extract element from isotope
        if isinstance(donor_ion, Isotope):
            donor_ion = donor_ion.element

        if isinstance(receiver_ion, Isotope):
            receiver_ion = receiver_ion.element

        # locate data files
        try:
            data = self._config["cxs"][donor_ion][receiver_ion][receiver_ionisation]
        except KeyError:
            raise RuntimeError("The requested beam cx rate data does not have an entry in the Open-ADAS configuration"
                               "(donor ion: {}, receiver ion: {}, ionisation: {}, transition: {})."
                               "".format(donor_ion.symbol, receiver_ion.symbol, receiver_ionisation, transition))

        # load and interpolate the relevant transition data from each file
        rates = []
        for donor_metastable, filename in data:
            file_path = os.path.join(self._data_path, filename)
            rates.append(BeamCXRate(donor_metastable, wavelength, adf12(file_path, transition), extrapolate=self._permit_extrapolation))
        return rates

    def beam_stopping_rate(self, beam_ion, plasma_ion, ionisation):

        # extract element from isotope
        if isinstance(beam_ion, Isotope):
            beam_ion = beam_ion.element

        if isinstance(plasma_ion, Isotope):
            plasma_ion = plasma_ion.element

        # locate data file
        try:
            filename = self._config["bms"][beam_ion][plasma_ion][ionisation]
        except KeyError:
            raise RuntimeError("The requested beam stopping rate data does not have an entry in the Open-ADAS "
                               "configuration (beam ion: {}, plasma ion: {}, ionisation: {})."
                               "".format(beam_ion.symbol, plasma_ion.symbol, ionisation))

        # load and interpolate data
        return BeamStoppingRate(adf21(os.path.join(self._data_path, filename)), extrapolate=self._permit_extrapolation)

    def beam_population_rate(self, beam_ion, metastable, plasma_ion, ionisation):

        # extract element from isotope
        if isinstance(beam_ion, Isotope):
            beam_ion = beam_ion.element

        if isinstance(plasma_ion, Isotope):
            plasma_ion = plasma_ion.element

        # locate data file
        try:
            filename = self._config["bmp"][beam_ion][metastable][plasma_ion][ionisation]
        except KeyError:
            raise RuntimeError("The requested beam population rate data does not have an entry in the "
                               "Open-ADAS configuration (beam ion: {}, metastable: {}, plasma ion: {}, ionisation: {})."
                               "".format(beam_ion.symbol, metastable, plasma_ion.symbol, ionisation))

        # load and interpolate data
        return BeamPopulationRate(adf22(os.path.join(self._data_path, filename)), extrapolate=self._permit_extrapolation)

    def beam_emission_rate(self, beam_ion, plasma_ion, ionisation, transition):
        # transition: Tuple containing (initial level, final level)
        # locate data file

        wavelength = self.wavelength(beam_ion, 0, transition)

        # extract element from isotope
        if isinstance(beam_ion, Isotope):
            beam_ion = beam_ion.element

        if isinstance(plasma_ion, Isotope):
            plasma_ion = plasma_ion.element

        try:
            filename = self._config["bme"][beam_ion][plasma_ion][ionisation][transition]
        except KeyError:
            raise RuntimeError("The requested beam emission rate data does not have an entry in the "
                               "Open-ADAS configuration (beam ion: {}, plasma ion: {}, ionisation: {}, transition: {})."
                               "".format(beam_ion.symbol, plasma_ion.symbol, ionisation, transition))

        # load and interpolate data
        return BeamEmissionRate(adf22(os.path.join(self._data_path, filename)), wavelength, extrapolate=self._permit_extrapolation)

    def impact_excitation_rate(self, ion, ionisation, transition):

        wavelength = self.wavelength(ion, ionisation, transition)

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            filename, block_number = self._config["eim"][ion][ionisation][transition]
        except KeyError:
            raise RuntimeError("The requested impact excitation rate data does not have an entry in the "
                               "Open-ADAS configuration (ion: {}, ionisation: {}, transition: {})."
                               "".format(ion.symbol, ionisation, transition))

        # load and interpolate data
        data = adf15(os.path.join(self._data_path, filename), block_number)
        return ImpactExcitationRate(wavelength, data, extrapolate=self._permit_extrapolation)

    def recombination_rate(self, ion, ionisation, transition):

        wavelength = self.wavelength(ion, ionisation, transition)

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            filename, block_number = self._config["rec"][ion][ionisation][transition]
        except KeyError:
            raise RuntimeError("The requested recombination rate data does not have an entry in the "
                               "Open-ADAS configuration (ion: {}, ionisation: {}, transition: {})."
                               "".format(ion.symbol, ionisation, transition))

        # load and interpolate data
        data = adf15(os.path.join(self._data_path, filename), block_number)
        return RecombinationRate(wavelength, data, extrapolate=self._permit_extrapolation)

