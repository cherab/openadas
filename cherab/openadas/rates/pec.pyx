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

import numpy as np
import matplotlib.pyplot as plt

from cherab.core.utility.conversion import Cm3ToM3, PerCm3ToPerM3, PhotonToJ

from libc.math cimport log10


# todo: evaluate it the interpolation can be done without the log10 operations? or if this should be ported to the cx rates.
cdef class ImpactExcitationRate(CoreImpactExcitationRate):

    def __init__(self, double wavelength, dict rate_data, extrapolate=False):

        self.raw_data = rate_data

        # pre-convert data to W m^3 from Photons s^-1 cm^3 prior to interpolation
        te = rate_data["TE"]                                            # eV
        ne = PerCm3ToPerM3.to(rate_data["DENS"])                        # m^-3
        pec = PhotonToJ.to(Cm3ToM3.to(rate_data["PEC"]), wavelength)    # W.m^3

        self.density_range = ne.min(), ne.max()
        self.temperature_range = te.min(), te.max()

        self._pec = Interpolate2DCubic(
            np.log10(ne), np.log10(te), np.log10(pec), extrapolate=extrapolate, extrapolation_type="quadratic"
        )

    cpdef double evaluate(self, double density, double temperature):
        return 10 ** self._pec.evaluate(log10(density), log10(temperature))


# todo: evaluate it the interpolation can be done without the log10 operations? or if this should be ported to the cx rates.
cdef class RecombinationRate(CoreRecombinationRate):

    def __init__(self, double wavelength, dict rate_data, extrapolate=False):

        self.raw_data = rate_data

        # pre-convert data to W m^3 from Photons s^-1 cm^3 prior to interpolation
        te = rate_data["TE"]                                            # eV
        ne = PerCm3ToPerM3.to(rate_data["DENS"])                        # m^-3
        pec = PhotonToJ.to(Cm3ToM3.to(rate_data["PEC"]), wavelength)    # W.m^3

        self.density_range = ne.min(), ne.max()
        self.temperature_range = te.min(), te.max()

        self._pec = Interpolate2DCubic(
            np.log10(ne), np.log10(te), np.log10(pec), extrapolate=extrapolate, extrapolation_type="quadratic"
        )

    cpdef double evaluate(self, double density, double temperature):
        return 10 ** self._pec.evaluate(log10(density), log10(temperature))


# cdef class ThermalCXRate(CoreThermalCXRate):
#
#     def __init__(self, double wavelength ,dict rate_data, extrapolate=False):
#         pass
#     cpdef double evaluate(self, double density, double temperature):
#         pass
#
#     def plot(self, density_list=None, x_limit=None, y_limit=None):
#
#         plt.figure()
#         for dens in density_list:
#             rates = [self.__call__(dens, temp) for temp in self._temperature]
#             plt.loglog(self._temperature, rates, label='{:.4G} m$^{{-3}}$'.format(dens))
#
#         if x_limit:
#             plt.xlim(x_limit)
#         if y_limit:
#             plt.ylim(y_limit)
#
#         plt.legend(loc=4)
#         plt.xlabel('Electron Temperature (eV)')
#         plt.ylabel('$PEC$ (m$^3$ s$^{-1}$)')
#         plt.title('Photon emissivity coefficient')