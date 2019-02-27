
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

# todo: to be implemented in a future release

# import numpy as np
# from numpy cimport ndarray
# from cherab.core.math.interpolators.interpolators2d cimport Interpolate2DCubic
# from cherab.core.atomic.rates cimport StageResolvedLineRadiation as CoreStageResolvedLineRadiation
#
#
# # todo remove log10 of data
# cdef class StageResolvedRadiation(CoreStageResolvedLineRadiation):
#
#     cdef:
#         readonly bint extrapolate
#         readonly tuple density_range, temperature_range
#         readonly ndarray _electron_density, _electron_temperature, _radiated_power
#         readonly Interpolate2DCubic _power_func
#
#     def __init__(self, element, ionisation, electron_density, electron_temperature, radiated_power, name='', extrapolate=False):
#
#         super().__init__(element, ionisation, name=name)
#
#         self._electron_density = np.array(electron_density, dtype=np.float64)
#         self._electron_temperature = np.array(electron_temperature, dtype=np.float64)
#         self._radiated_power = np.array(radiated_power, dtype=np.float64)
#
#         if not all(j >= 0 for i in self._radiated_power for j in i):
#             raise ValueError("Can't have negative power values!")
#
#         self.density_range = (self._electron_density.min(), self._electron_density.max())
#         self.temperature_range = (self._electron_temperature.min(), self._electron_temperature.max())
#
#         self.extrapolate = extrapolate
#         self._power_func = Interpolate2DCubic(self._electron_density, self._electron_temperature, self._radiated_power,
#                                               extrapolate=extrapolate, extrapolation_type="nearest")
#
#     cdef double evaluate(self, double electron_density, double electron_temperature) except? -1e999:
#         cdef double rate = self._power_func.evaluate(electron_density, electron_temperature)
#         return max(0, rate)
#
#
# cdef class NullStageResolvedLineRadiation(CoreStageResolvedLineRadiation):
#     """
#     A stage resolved line radiation rate that always returns zero.
#     Needed for use cases where the required atomic data is missing.
#     """
#
#     cdef double evaluate(self, double electron_density, double electron_temperature) except? -1e999:
#         return 0.0
