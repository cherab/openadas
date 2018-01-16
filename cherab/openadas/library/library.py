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
import json


LIBRARY_PATH = os.path.split(__file__)[0]

ADF11_FILES = json.load(open(os.path.join(LIBRARY_PATH, 'adf11.json')))
ADF11_PLT_FILES = ADF11_FILES['adf11_plt_files']
ADF11_PRB_FILES = ADF11_FILES['adf11_prb_files']



