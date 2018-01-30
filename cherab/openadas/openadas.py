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
import urllib.request

from cherab.core import AtomicData
from cherab.core.atomic.elements import Isotope
from cherab.core.utility.recursivedict import RecursiveDict

from cherab.openadas.library import *
from cherab.openadas.read import adf11, adf12, adf15, adf21, adf22
from cherab.openadas.read.adf15 import add_adf15_to_atomic_data
from . import config
from .rates import *
from cherab.openadas.rates.radiated_power import StageResolvedRadiation


class OpenADAS(AtomicData):

    def __init__(self, data_path=None, config=config.default, permit_extrapolation=False):

        super().__init__()
        self._data_path = data_path or self._setup_data_path()

        self._config = config

        # if true informs interpolation objects to allow extrapolation beyond the limits of the tabulated data
        self._permit_extrapolation = permit_extrapolation

    @property
    def config(self):
        # configuration is immutable, changes to ADAS state are not tracked
        return self._config.copy()

    @property
    def data_path(self):
        return self._data_path

    def _setup_data_path(self):

        data_path = os.path.expanduser('~/.cherab/openadas')

        if not os.path.isdir(data_path):
            os.makedirs(data_path)
            os.makedirs(os.path.join(data_path, 'adf12'))
            os.makedirs(os.path.join(data_path, 'adf15'))
            os.makedirs(os.path.join(data_path, 'adf21'))
            os.makedirs(os.path.join(data_path, 'adf22'))

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
            if isinstance(ion, Isotope):
                element = ion.element
                try:
                    return self._config["wavelength"][element][ionisation][transition]
                except KeyError:
                    raise RuntimeError("The requested wavelength data for ({}, {}, {}) is not available."
                                       "".format(ion.symbol, ionisation, transition))
            else:
                raise RuntimeError("The requested wavelength data for ({}, {}, {}) is not available."
                                   "".format(ion.symbol, ionisation, transition))

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
            filename, block_number = self._config["excitation"][ion][ionisation][transition]
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
            filename, block_number = self._config["recombination"][ion][ionisation][transition]
        except KeyError:
            raise RuntimeError("The requested recombination rate data does not have an entry in the "
                               "Open-ADAS configuration (ion: {}, ionisation: {}, transition: {})."
                               "".format(ion.symbol, ionisation, transition))

        # load and interpolate data
        data = adf15(os.path.join(self._data_path, filename), block_number)
        return RecombinationRate(wavelength, data, extrapolate=self._permit_extrapolation)

    def stage_resolved_line_radiation_rate(self, ion, ionisation):

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            plt_files = ADF11_PLT_FILES[ion.symbol]
        except KeyError:
            raise ValueError("No ADF11 files set for Ion - {}".format(ion.symbol))

        absolute_file_path = self._check_for_adf_file(plt_files['ADAS_Path'], plt_files['Download_URL'])

        densities, temperatures, rate_data = adf11(absolute_file_path, ion, ionisation)

        name = 'Stage Resolved Line Radiation - ({}, {})'.format(ion.symbol, ionisation)
        return StageResolvedRadiation(ion, ionisation, densities, temperatures, rate_data,
                                      name=name, extrapolate=self._permit_extrapolation)

    def stage_resolved_continuum_radiation_rate(self, ion, ionisation):

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            prb_files = ADF11_PRB_FILES[ion.symbol]
        except KeyError:
            raise ValueError("No ADF11 files set for Ion - {}".format(ion.symbol))

        absolute_file_path = self._check_for_adf_file(prb_files['ADAS_Path'], prb_files['Download_URL'])

        densities, temperatures, rate_data = adf11(absolute_file_path, ion, ionisation)

        name = 'Stage Resolved Continuum Radiation - ({}, {})'.format(ion.symbol, ionisation)

        return StageResolvedRadiation(ion, ionisation, densities, temperatures, rate_data,
                                      name=name, extrapolate=self._permit_extrapolation)

    def _check_for_adf_file(self, relative_adf_file_path, download_path):

        relative_adf_directory, adf_file_name = os.path.split(relative_adf_file_path)
        absolute_adf_directory = os.path.join(self._data_path, relative_adf_directory)
        absolute_file_path = os.path.join(absolute_adf_directory, adf_file_name)

        if not os.path.exists(absolute_adf_directory):
            os.makedirs(absolute_adf_directory)

        if os.path.isfile(absolute_file_path):
            return absolute_file_path
        else:
            urllib.request.urlretrieve(download_path, absolute_file_path)

        return absolute_file_path

    def add_adf15_file(self, element, ionisation, adf_file_path):

        if not os.path.isfile(adf_file_path):
            new_path = os.path.join(os.path.expanduser('~/.cherab/openadas'), adf_file_path)
            if not os.path.isfile(new_path):
                raise ValueError("Could not find ADF15 file - '{}'".format(adf_file_path))
            adf_file_path = new_path

        atomic_data_dict = RecursiveDict.from_dict(self._config)
        atomic_data_dict = add_adf15_to_atomic_data(atomic_data_dict, element, ionisation, adf_file_path)
        self._config = atomic_data_dict.freeze()
