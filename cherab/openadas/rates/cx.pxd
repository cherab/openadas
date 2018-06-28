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

from cherab.core cimport BeamCXRate as CoreBeamCXRate
from cherab.core.math cimport Function1D, Function2D


cdef class BeamCXRate(CoreBeamCXRate):

    cdef readonly:
        dict raw_data
        double wavelength
        int donor_metastable
        Function1D _eb, _ti, _ni, _zeff, _b
        readonly tuple beam_energy_range,
        readonly tuple density_range
        readonly tuple temperature_range
        readonly tuple zeff_range
        readonly tuple b_field_range
