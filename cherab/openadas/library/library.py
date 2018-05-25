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


from cherab.core.utility.recursivedict import RecursiveDict

from .adf11 import ADF11_PLT_FILES, ADF11_PRB_FILES
from .adf12 import ADF12_CXS_FILES
from .adf15 import ADF15_PEC_FILES
from .adf21 import ADF21_BMS_FILES
from .adf22 import ADF22_BMP_FILES, ADF22_BME_FILES


DEFAULT_ADAS_CONFIG = RecursiveDict()

DEFAULT_ADAS_CONFIG["ADF11_PLT_FILES"] = ADF11_PLT_FILES
DEFAULT_ADAS_CONFIG["ADF11_PRB_FILES"] = ADF11_PRB_FILES
DEFAULT_ADAS_CONFIG["ADF12_CXS_FILES"] = ADF12_CXS_FILES
DEFAULT_ADAS_CONFIG["ADF15_PEC_FILES"] = ADF15_PEC_FILES
DEFAULT_ADAS_CONFIG["ADF21_BMS_FILES"] = ADF21_BMS_FILES
DEFAULT_ADAS_CONFIG["ADF22_BMP_FILES"] = ADF22_BMP_FILES
DEFAULT_ADAS_CONFIG["ADF22_BME_FILES"] = ADF22_BME_FILES
