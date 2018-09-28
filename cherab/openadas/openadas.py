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

from cherab.core import AtomicData
from cherab.core.atomic.elements import Isotope
from cherab.openadas.repository import DEFAULT_REPOSITORY_PATH

from .rates import *
from cherab.openadas import repository


class OpenADAS(AtomicData):
    """

    """

    def __init__(self, data_path=None, permit_extrapolation=False):

        super().__init__()
        self._data_path = data_path or DEFAULT_REPOSITORY_PATH

        # if true informs interpolation objects to allow extrapolation beyond the limits of the tabulated data
        self._permit_extrapolation = permit_extrapolation

    @property
    def data_path(self):
        return self._data_path

    def wavelength(self, ion, ionisation, transition):
        """
        :param ion: Element object defining the ion type.
        :param ionisation: Ionisation level of the ion.
        :param transition: Tuple containing (initial level, final level)
        :return: Wavelength in nanometers.
        """

        if isinstance(ion, Isotope):
            ion = ion.element
        return repository.get_wavelength(ion, ionisation, transition)

    def beam_cx_rate(self, donor_ion, receiver_ion, receiver_ionisation, transition):
        """

        :param donor_ion:
        :param receiver_ion:
        :param receiver_ionisation:
        :param transition:
        :return:
        """

        # extract element from isotope
        if isinstance(donor_ion, Isotope):
            donor_ion = donor_ion.element

        if isinstance(receiver_ion, Isotope):
            receiver_ion = receiver_ion.element

        # read data
        wavelength = repository.get_wavelength(receiver_ion, receiver_ionisation - 1, transition)
        data = repository.get_beam_cx_rates(donor_ion, receiver_ion, receiver_ionisation, transition)

        # load and interpolate the relevant transition data from each file
        rates = []
        for donor_metastable, rate_data in data:
            rates.append(BeamCXRate(donor_metastable, wavelength, rate_data, extrapolate=self._permit_extrapolation))
        return rates

    def beam_stopping_rate(self, beam_ion, plasma_ion, ionisation):
        """

        :param beam_ion:
        :param plasma_ion:
        :param ionisation:
        :return:
        """

        # extract element from isotope
        if isinstance(beam_ion, Isotope):
            beam_ion = beam_ion.element

        if isinstance(plasma_ion, Isotope):
            plasma_ion = plasma_ion.element

        # locate data file
        data = repository.get_beam_stopping_rate(beam_ion, plasma_ion, ionisation)

        # load and interpolate data
        return BeamStoppingRate(data, extrapolate=self._permit_extrapolation)

    def beam_population_rate(self, beam_ion, metastable, plasma_ion, ionisation):
        """

        :param beam_ion:
        :param metastable:
        :param plasma_ion:
        :param ionisation:
        :return:
        """

        # extract element from isotope
        if isinstance(beam_ion, Isotope):
            beam_ion = beam_ion.element

        if isinstance(plasma_ion, Isotope):
            plasma_ion = plasma_ion.element

        # locate data file
        data = repository.get_beam_population_rate(beam_ion, metastable, plasma_ion, ionisation)

        # load and interpolate data
        return BeamPopulationRate(data, extrapolate=self._permit_extrapolation)

    def beam_emission_rate(self, beam_ion, plasma_ion, ionisation, transition):
        """

        :param beam_ion:
        :param plasma_ion:
        :param ionisation:
        :param transition:
        :return:
        """

        # extract element from isotope
        if isinstance(beam_ion, Isotope):
            beam_ion = beam_ion.element

        if isinstance(plasma_ion, Isotope):
            plasma_ion = plasma_ion.element

        # locate data file
        data = repository.get_beam_emission_rate(beam_ion, plasma_ion, ionisation, transition)

        # load and interpolate data
        return BeamEmissionRate(data, extrapolate=self._permit_extrapolation)

    def impact_excitation_rate(self, ion, ionisation, transition):
        """

        :param ion:
        :param ionisation:
        :param transition:
        :return:
        """

        if isinstance(ion, Isotope):
            ion = ion.element

        wavelength = repository.get_wavelength(ion, ionisation, transition)
        data = repository.get_pec_excitation_rate(ion, ionisation, transition)
        return ImpactExcitationRate(wavelength, data, extrapolate=self._permit_extrapolation)

    def recombination_rate(self, ion, ionisation, transition):
        """

        :param ion:
        :param ionisation:
        :param transition:
        :return:
        """

        if isinstance(ion, Isotope):
            ion = ion.element

        wavelength = repository.get_wavelength(ion, ionisation, transition)
        data = repository.get_pec_recombination_rate(ion, ionisation, transition)
        return RecombinationRate(wavelength, data, extrapolate=self._permit_extrapolation)

    # def stage_resolved_line_ radiation_rate(self, ion, ionisation):
    #
    #     # extract element from isotope
    #     if isinstance(ion, Isotope):
    #         ion = ion.element
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
    #     name = 'Stage Resolved Continuum Radiation - ({}, {})'.format(ion.symbol, ionisation)
    #
    #     return StageResolvedRadiation(ion, ionisation, densities, temperatures, rate_data,
    #                                   name=name, extrapolate=self._permit_extrapolation)


