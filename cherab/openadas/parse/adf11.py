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

import numpy as np
import re

# todo: to be implemented in a future release


# def parse_adf11acd(ion, ionisation, adf_file_path):
#     pass


# def parse_adf11scd(ion, ionisation, adf_file_path):
#     pass


# def parse_adf11qcd(ion, ionisation, adf_file_path):
#     pass


# def parse_adf11xcd(ion, ionisation, adf_file_path):
#     pass


# def parse_adf11ccd(ion, ionisation, adf_file_path):
#     pass


# def parse_adf11plt(ion, ionisation, adf_file_path):
#     pass


# def parse_adf11prb(ion, ionisation, adf_file_path):
#     pass


# def parse_adf11pls(ion, ionisation, adf_file_path):
#     pass


# def parse_adf11prc(ion, ionisation, adf_file_path):
#     pass


# def parse_adf11xxx(file_path, ion, ionisation):
#
#     adf11_fh = open(file_path, 'r')
#     lines = adf11_fh.readlines()
#     adf11_fh.close()
#
#     file_header = lines.pop(0).split()
#     if int(file_header[0]) != ion.atomic_number:
#         raise ValueError("ADF file does not match required atomic number.")
#
#     num_densities = int(file_header[1])
#     num_temperatures = int(file_header[2])
#
#     lines.pop(0)
#     parameter_lines = []
#     while True:
#         next_line = lines.pop(0)
#         if next_line[0:2] == '--':
#             break
#         components = next_line.split()
#         for c in components:
#             parameter_lines.append(float(c))
#
#     if len(parameter_lines) != num_densities + num_temperatures:
#         raise ValueError("ADF11 file could not be parsed correctly.")

#     # todo: remove log10 remapping, interpolate directly! Note also needs to be fixed in rate.
#     densities = np.array([10**x * 1E4 for x in parameter_lines[0:num_densities]])
#     temperatures = np.array([10**x for x in parameter_lines[num_densities:]])
#
#     found = False
#     while True:
#         if next_line[0:2] == '--':
#             match = re.match('.*Z1= ([0-9]*).*', next_line)
#             if match and int(match.group(1)) == ionisation+1:
#                 found = True
#                 break
#         if next_line[0] == 'C':
#             break
#         next_line = lines.pop(0)
#
#     if found:
#         rate_data = []
#         while True:
#             next_line = lines.pop(0)
#             if next_line[0:2] == '--' or next_line[0] == 'C':
#                 break
#             for c in next_line.split():
#                 rate_data.append(10**float(c) * 1E-8)
#
#         rate_data = np.array(rate_data)
#         rate_data = rate_data.reshape((num_densities, num_temperatures))
#
#     else:
#         raise ValueError('Requested ADF11 data could not be found in this file.')
#
#     return densities, temperatures, rate_data
