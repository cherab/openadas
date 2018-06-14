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

from cherab.core import AtomicData
from cherab.core.atomic.elements import Isotope
from cherab.core.utility.recursivedict import RecursiveDict
from cherab.openadas.repository import DEFAULT_REPOSITORY_PATH

from cherab.openadas.library import wavelength_database, default_adas_config
# from cherab.openadas.read import adf11, adf12, adf15, adf21, adf22
# from cherab.openadas.read.adf15 import add_adf15_to_atomic_data
from .rates import *
from cherab.openadas.rates.radiated_power import StageResolvedRadiation
from cherab.openadas.utilities import check_for_adf_file




"""
TODO:
 * move auto-download to init (downloads everything the first time it finds the files)
 * add an option to enable/disable auto download - default=disabled
 * remove auto-download code from individual rate routines
 * add utility functions to help build/scrape configuration e.g. add_wavelength(transition, wavelength)
 * tidy up interfaces, so all are consistent
"""
"""
options:
* store cache on disk, user required to build database before first run (can be added to setup.py)
    - user can specify rate overrides files/data in code, use in preference to searching for data
* 
"""




class OpenADAS(AtomicData):

    def __init__(self, data_path=None, permit_extrapolation=False):

        super().__init__()
        self._data_path = data_path or DEFAULT_REPOSITORY_PATH
        # self._adas_config = adas_config.freeze()

        # adas config specifies files in which to find the rates for species etc... but not transisions
        # to discover the transitions the adf file must be parsed, this is done dynamically
        # self._adf12_config = {}
        # self._adf15_config = {}
        # self._adf21_config = {}
        # self._adf22_bmp_config = {}
        # self._adf22_bme_config = {}
        # self._wavelengths = wavelength_database

        # if true informs interpolation objects to allow extrapolation beyond the limits of the tabulated data
        self._permit_extrapolation = permit_extrapolation

    # @property
    # def config(self):
    #     # configuration is immutable, changes to ADAS state are not tracked
    #     return self._adas_config.copy()

    @property
    def data_path(self):
        return self._data_path

    def wavelength(self, ion, ionisation, transition):
        """
        :param ion: Element object defining the ion type.
        :param transition: Tuple containing (initial level, final level)
        :return: Wavelength in nanometers.
        """

        # try:
        #     return self._wavelength_list[ion][ionisation][transition]
        # except KeyError:
        #     if isinstance(ion, Isotope):
        #         element = ion.element
        #         try:
        #             return self._wavelength_list[element][ionisation][transition]
        #         except KeyError:
        #             raise RuntimeError("The requested wavelength data for ({}, {}, {}) is not available."
        #                                "".format(ion.symbol, ionisation, transition))
        #     else:
        #         raise RuntimeError("The requested wavelength data for ({}, {}, {}) is not available."
        #                            "".format(ion.symbol, ionisation, transition))

    # def beam_cx_rate(self, donor_ion, receiver_ion, receiver_ionisation, transition):
    #
    #     # extract element from isotope
    #     if isinstance(donor_ion, Isotope):
    #         donor_ion = donor_ion.element
    #
    #     if isinstance(receiver_ion, Isotope):
    #         receiver_ion = receiver_ion.element
    #
    #     # locate data files
    #     try:
    #         data = self._adf12_config[donor_ion][receiver_ion][receiver_ionisation]
    #     except KeyError:
    #
    #         # If not found in current configuration try the Open-ADAS library files.
    #         try:
    #             library_files = self._adas_config['ADF12_CXS_FILES'][donor_ion][receiver_ion][receiver_ionisation]
    #
    #             for file in library_files:
    #                 donor_metastable, adas_path, download_path = file
    #                 adf_file_path = check_for_adf_file(adas_path, download_path)
    #                 self._add_adf12_file(donor_ion, receiver_ion, receiver_ionisation, donor_metastable, adf_file_path)
    #             data = self._adf12_config[donor_ion][receiver_ion][receiver_ionisation]
    #         except KeyError:
    #             raise RuntimeError("The requested beam cx rate data does not have an entry in the Open-ADAS configuration"
    #                                "(donor ion: {}, receiver ion: {}, ionisation: {}, transition: {})."
    #                                "".format(donor_ion.symbol, receiver_ion.symbol, receiver_ionisation, transition))
    #
    #     wavelength = self.wavelength(receiver_ion, receiver_ionisation - 1, transition)
    #
    #     # load and interpolate the relevant transition data from each file
    #     rates = []
    #     for donor_metastable, filename in data:
    #         file_path = os.path.join(self._data_path, filename)
    #         rates.append(BeamCXRate(donor_metastable, wavelength, adf12(file_path, transition), extrapolate=self._permit_extrapolation))
    #     return rates

    # def beam_stopping_rate(self, beam_ion, plasma_ion, ionisation):
    #
    #     # extract element from isotope
    #     if isinstance(beam_ion, Isotope):
    #         beam_ion = beam_ion.element
    #
    #     if isinstance(plasma_ion, Isotope):
    #         plasma_ion = plasma_ion.element
    #
    #     # locate data file
    #     try:
    #         filename = self._adf21_config[beam_ion][plasma_ion][ionisation]
    #     except KeyError:
    #
    #         # If not found in current configuration try the Open-ADAS library files.
    #         try:
    #             adas_path, download_path = self._adas_config["ADF21_BMS_FILES"][beam_ion][plasma_ion][ionisation]
    #             adf_file_path = check_for_adf_file(adas_path, download_path)
    #             self._add_adf21_file(beam_ion, plasma_ion, ionisation, adf_file_path)
    #             filename = self._adf21_config[beam_ion][plasma_ion][ionisation]
    #         except KeyError:
    #             raise RuntimeError("The requested beam stopping rate data does not have an entry in the Open-ADAS "
    #                                "configuration (beam ion: {}, plasma ion: {}, ionisation: {})."
    #                                "".format(beam_ion.symbol, plasma_ion.symbol, ionisation))
    #
    #     # load and interpolate data
    #     return BeamStoppingRate(adf21(os.path.join(self._data_path, filename)), extrapolate=self._permit_extrapolation)

    # def beam_population_rate(self, beam_ion, metastable, plasma_ion, ionisation):
    #
    #     # extract element from isotope
    #     if isinstance(beam_ion, Isotope):
    #         beam_ion = beam_ion.element
    #
    #     if isinstance(plasma_ion, Isotope):
    #         plasma_ion = plasma_ion.element
    #
    #     # locate data file
    #     try:
    #         filename = self._adf22_bmp_config[beam_ion][metastable][plasma_ion][ionisation]
    #     except KeyError:
    #
    #         # If not found in current configuration try the Open-ADAS library files.
    #         try:
    #             adas_path, download_path = self._adas_config["ADF22_BMP_FILES"][beam_ion][metastable][plasma_ion][ionisation]
    #             adf_file_path = check_for_adf_file(adas_path, download_path)
    #             self._add_adf22_bmp_file(beam_ion, metastable, plasma_ion, ionisation, adf_file_path)
    #             filename = self._adf22_bmp_config[beam_ion][metastable][plasma_ion][ionisation]
    #         except KeyError:
    #             raise RuntimeError("The requested beam population rate data does not have an entry in the "
    #                                "Open-ADAS configuration (beam ion: {}, metastable: {}, plasma ion: {}, ionisation: {})."
    #                                "".format(beam_ion.symbol, metastable, plasma_ion.symbol, ionisation))
    #
    #     # load and interpolate data
    #     return BeamPopulationRate(adf22(os.path.join(self._data_path, filename)), extrapolate=self._permit_extrapolation)

    # def beam_emission_rate(self, beam_ion, plasma_ion, ionisation, transition):
    #
    #     wavelength = self.wavelength(beam_ion, 0, transition)
    #
    #     # extract element from isotope
    #     if isinstance(beam_ion, Isotope):
    #         beam_ion = beam_ion.element
    #
    #     if isinstance(plasma_ion, Isotope):
    #         plasma_ion = plasma_ion.element
    #
    #     try:
    #         filename = self._adf22_bme_config[beam_ion][plasma_ion][ionisation][transition]
    #     except KeyError:
    #
    #         # If not found in current configuration try the Open-ADAS library files.
    #         try:
    #             adas_path, download_path = self._adas_config["ADF22_BME_FILES"][beam_ion][plasma_ion][ionisation][transition]
    #             adf_file_path = check_for_adf_file(adas_path, download_path)
    #             self._add_adf22_bme_file(beam_ion, plasma_ion, ionisation, transition, adf_file_path)
    #             filename = self._adf22_bmp_config[beam_ion][plasma_ion][ionisation][transition]
    #         except KeyError:
    #             raise RuntimeError("The requested beam emission rate data does not have an entry in the "
    #                                "Open-ADAS configuration (beam ion: {}, plasma ion: {}, ionisation: {}, transition: {})."
    #                                "".format(beam_ion.symbol, plasma_ion.symbol, ionisation, transition))
    #
    #     # load and interpolate data
    #     return BeamEmissionRate(adf22(os.path.join(self._data_path, filename)), wavelength, extrapolate=self._permit_extrapolation)

    def impact_excitation_rate(self, ion, ionisation, transition):

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        # try: locate and read rate file for ion
            # read json file
            # unpack data
        # if rate missing inform user

        # setup rate object

        try:
            filename, block_number = self._adf15_config["excitation"][ion][ionisation][transition]
            wavelength = self._adf15_config["wavelength"][ion][ionisation][transition]
            self._wavelength_list[ion][ionisation][transition] = wavelength
        except KeyError:

            # If not found in current configuration try the Open-ADAS library files.
            try:
                library_file = self._adas_config["ADF15_PEC_FILES"][ion][ionisation]
                adf_file_path = check_for_adf_file(library_file['ADAS_Path'], library_file['Download_URL'])
                self._add_adf15_file(ion, ionisation, adf_file_path)
                filename, block_number = self._adf15_config["excitation"][ion][ionisation][transition]
                wavelength = self._adf15_config["wavelength"][ion][ionisation][transition]
                wavelength_config = RecursiveDict.from_dict(self._wavelength_list)
                wavelength_config[ion][ionisation][transition] = wavelength
                self._wavelength_list = wavelength_config.freeze()
            except KeyError:
                raise RuntimeError("The requested impact excitation rate data does not have an entry in the "
                                   "Open-ADAS configuration (ion: {}, ionisation: {}, transition: {})."
                                   "".format(ion.symbol, ionisation, transition))

        # load and interpolate data
        data = adf15(os.path.join(self._data_path, filename), block_number)
        return ImpactExcitationRate(wavelength, data, extrapolate=self._permit_extrapolation)

    def recombination_rate(self, ion, ionisation, transition):

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            filename, block_number = self._adf15_config["recombination"][ion][ionisation][transition]
            wavelength = self._adf15_config["wavelength"][ion][ionisation][transition]
            self._wavelength_list[ion][ionisation][transition] = wavelength
        except KeyError:

            # If not found in current configuration try the Open-ADAS library files.
            try:
                library_file = self._adas_config["ADF15_PEC_FILES"][ion][ionisation]
                adf_file_path = check_for_adf_file(library_file['ADAS_Path'], library_file['Download_URL'])
                self._add_adf15_file(ion, ionisation, adf_file_path)
                filename, block_number = self._adf15_config["recombination"][ion][ionisation][transition]
                wavelength = self._adf15_config["wavelength"][ion][ionisation][transition]
                wavelength_config = RecursiveDict.from_dict(self._wavelength_list)
                wavelength_config[ion][ionisation][transition] = wavelength
                self._wavelength_list = wavelength_config.freeze()
            except KeyError:
                raise RuntimeError("The requested recombination rate data does not have an entry in the "
                                   "Open-ADAS configuration (ion: {}, ionisation: {}, transition: {})."
                                   "".format(ion.symbol, ionisation, transition))

        # load and interpolate data
        data = adf15(os.path.join(self._data_path, filename), block_number)
        return RecombinationRate(wavelength, data, extrapolate=self._permit_extrapolation)

    # def stage_resolved_line_radiation_rate(self, ion, ionisation):
    #
    #     # extract element from isotope
    #     if isinstance(ion, Isotope):
    #         ion = ion.element
    #
    #     try:
    #         plt_files = self._adas_config["ADF11_PLT_FILES"][ion.symbol]
    #     except KeyError:
    #         raise ValueError("No ADF11 files set for Ion - {}".format(ion.symbol))
    #
    #     absolute_file_path = check_for_adf_file(plt_files['ADAS_Path'], plt_files['Download_URL'])
    #
    #     densities, temperatures, rate_data = adf11(absolute_file_path, ion, ionisation)
    #
    #     name = 'Stage Resolved Line Radiation - ({}, {})'.format(ion.symbol, ionisation)
    #     return StageResolvedRadiation(ion, ionisation, densities, temperatures, rate_data,
    #                                   name=name, extrapolate=self._permit_extrapolation)

    # def stage_resolved_continuum_radiation_rate(self, ion, ionisation):
    #
    #     # extract element from isotope
    #     if isinstance(ion, Isotope):
    #         ion = ion.element
    #
    #     try:
    #         prb_files = self._adas_config["ADF11_PRB_FILES"][ion.symbol]
    #     except KeyError:
    #         raise ValueError("No ADF11 files set for Ion - {}".format(ion.symbol))
    #
    #     absolute_file_path = check_for_adf_file(prb_files['ADAS_Path'], prb_files['Download_URL'])
    #
    #     densities, temperatures, rate_data = adf11(absolute_file_path, ion, ionisation)
    #
    #     name = 'Stage Resolved Continuum Radiation - ({}, {})'.format(ion.symbol, ionisation)
    #
    #     return StageResolvedRadiation(ion, ionisation, densities, temperatures, rate_data,
    #                                   name=name, extrapolate=self._permit_extrapolation)

    # def _add_adf12_file(self, donor_ion, receiver_ion, receiver_ionisation, donor_metastable, adf_file_path):
    #
    #     if not os.path.isfile(adf_file_path):
    #         new_path = os.path.join(os.path.expanduser('~/.cherab/openadas'), adf_file_path)
    #         if not os.path.isfile(new_path):
    #             raise ValueError("Could not find ADF15 file - '{}'".format(adf_file_path))
    #         adf_file_path = new_path
    #
    #     adf12_config = RecursiveDict.from_dict(self._adf12_config)
    #     if type(adf12_config[donor_ion][receiver_ion][receiver_ionisation]) == RecursiveDict:
    #         adf12_config[donor_ion][receiver_ion][receiver_ionisation] = [(donor_metastable, adf_file_path)]
    #     else:
    #         adf12_config[donor_ion][receiver_ion][receiver_ionisation].append((donor_metastable, adf_file_path))
    #     self._adf12_config = adf12_config.freeze()

    # def _add_adf15_file(self, element, ionisation, adf_file_path):
    #
    #     if not os.path.isfile(adf_file_path):
    #         new_path = os.path.join(os.path.expanduser('~/.cherab/openadas'), adf_file_path)
    #         if not os.path.isfile(new_path):
    #             raise ValueError("Could not find ADF15 file - '{}'".format(adf_file_path))
    #         adf_file_path = new_path
    #
    #     adf15_config = RecursiveDict.from_dict(self._adf15_config)
    #     adf15_config = add_adf15_to_atomic_data(adf15_config, element, ionisation, adf_file_path)
    #     self._adf15_config = adf15_config.freeze()

    # def _add_adf21_file(self, beam_ion, plasma_ion, ionisation, adf_file_path):
    #
    #     if not os.path.isfile(adf_file_path):
    #         new_path = os.path.join(os.path.expanduser('~/.cherab/openadas'), adf_file_path)
    #         if not os.path.isfile(new_path):
    #             raise ValueError("Could not find ADF15 file - '{}'".format(adf_file_path))
    #         adf_file_path = new_path
    #
    #     adf21_config = RecursiveDict.from_dict(self._adf21_config)
    #     adf21_config[beam_ion][plasma_ion][ionisation] = adf_file_path
    #     self._adf21_config = adf21_config.freeze()

    # def _add_adf22_bmp_file(self, beam_ion, metastable, plasma_ion, ionisation, adf_file_path):
    #
    #     if not os.path.isfile(adf_file_path):
    #         new_path = os.path.join(os.path.expanduser('~/.cherab/openadas'), adf_file_path)
    #         if not os.path.isfile(new_path):
    #             raise ValueError("Could not find ADF15 file - '{}'".format(adf_file_path))
    #         adf_file_path = new_path
    #
    #     adf22_config = RecursiveDict.from_dict(self._adf22_bmp_config)
    #     adf22_config[beam_ion][metastable][plasma_ion][ionisation] = adf_file_path
    #     self._adf22_bmp_config = adf22_config.freeze()

    # def _add_adf22_bme_file(self, beam_ion, plasma_ion, ionisation, transition, adf_file_path):
    #
    #     if not os.path.isfile(adf_file_path):
    #         new_path = os.path.join(os.path.expanduser('~/.cherab/openadas'), adf_file_path)
    #         if not os.path.isfile(new_path):
    #             raise ValueError("Could not find ADF15 file - '{}'".format(adf_file_path))
    #         adf_file_path = new_path
    #
    #     adf22_config = RecursiveDict.from_dict(self._adf22_bme_config)
    #     adf22_config[beam_ion][plasma_ion][ionisation][transition] = adf_file_path
    #     self._adf22_bme_config = adf22_config.freeze()
