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

from cherab.core cimport ImpactExcitationRate as CoreImpactExcitationRate
from cherab.core cimport RecombinationRate as CoreRecombinationRate
from cherab.core cimport ThermalCXRate as CoreThermalCXRate
from cherab.core.math cimport Interpolate2DCubic


cdef class ImpactExcitationRate(CoreImpactExcitationRate):

    cdef:
        readonly dict raw_data
        readonly double wavelength
        readonly tuple density_range, temperature_range
        Interpolate2DCubic _rate


cdef class NullImpactExcitationRate(CoreImpactExcitationRate):
    pass


cdef class RecombinationRate(CoreRecombinationRate):

    cdef:
        readonly dict raw_data
        readonly double wavelength
        readonly tuple density_range, temperature_range
        Interpolate2DCubic _rate


cdef class NullRecombinationRate(CoreRecombinationRate):
    pass


# cdef class CXThermalRate(CoreCXThermalRate):
#     pass
#
# cdef class ThermalCXRate(CoreThermalCXRate):
#     pass
