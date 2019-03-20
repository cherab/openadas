from cherab.openadas.parse.adf11 import parse_adf11
from cherab.openadas import repository
from cherab.core.atomic import neon
from cherab.openadas import OpenADAS
from cherab.openadas.parse import parse_adf11
from cherab.core.utility import RecursiveDict, Cm3ToM3, PerCm3ToPerM3
import numpy as np
from cherab.core.math import Interpolate2DCubic
import matplotlib.pyplot as plt


def solve_ion_balance(ne, te, ion_interpol, recom_interpol, log = False):
    if log:
        ne = np.log10(ne)
        te = np.log10(ne)

    matbal = np.zeros((numstates, numstates))

    matbal[0, 0] -= ion_interpol[0](ne, te)
    matbal[0, 1] += recom_interpol[1](ne, te)
    matbal[-1, -1] -= recom_interpol[10](ne, te)
    matbal[-1, -2] += ion_interpol[9](ne, te)

    for i in range(1, numstates - 1):
        matbal[i, i - 1] += ion_interpol[i - 1](ne, te)
        matbal[i, i] -= (ion_interpol[i](ne, te) + recom_interpol[i](ne, te))
        matbal[i, i + 1] += recom_interpol[i + 1](ne, te)

    if log:
        tmp = np.where(~(matbal == 0))
        matbal[tmp] = 10 ** matbal[tmp]

    matbal = np.concatenate((matbal, np.ones((1, matbal.shape[1]))), axis=0)
    matbal = np.concatenate((matbal, np.zeros((matbal.shape[0], 1))), axis=1)
    solution = np.zeros((matbal.shape[0]))
    solution[-1] = 1

    fracabun = np.linalg.lstsq(matbal, solution, rcond=-1)[0][0:-1]

    return fracabun



adas = OpenADAS(permit_extrapolation=False)



charge = 1
numstates = neon.atomic_number + 1

electron_density = 1e19
electron_temperatures = [10**x for x in np.linspace(np.log10(1), np.log10(10000), num=100)]

ion_adas = parse_adf11(neon, "/compass/home/tomes/.cherab/openadas/download_cache/adf11/scd96/scd96_ne.dat")
recom_adas = parse_adf11(neon, "/compass/home/tomes/.cherab/openadas/download_cache/adf11/acd96/acd96_ne.dat")


############Create interpolators on adas data in log10 number format
ion_interp_adas_origin = {}
recom_interp_adas_origin = {}
for i in range(neon.atomic_number):
    ac = i+1
    ion_interp_adas_origin[i] = Interpolate2DCubic(ion_adas[neon][ac]["ne"], ion_adas[neon][ac]["te"], ion_adas[neon][ac]["rates"])
    recom_interp_adas_origin[i + 1] = Interpolate2DCubic(recom_adas[neon][ac]["ne"], recom_adas[neon][ac]["te"], recom_adas[neon][ac]["rates"])

#############Create interpolators on adas data in normal number format
ion_interp_adas_pow = {}
recom_interp_adas_pow = {}
for i in range(neon.atomic_number):
    ac = i+1
    ion_interp_adas_pow[i] = Interpolate2DCubic(10**ion_adas[neon][ac]["ne"], 10**ion_adas[neon][ac]["te"], 10**ion_adas[neon][ac]["rates"])
    recom_interp_adas_pow[i + 1] = Interpolate2DCubic(10**recom_adas[neon][ac]["ne"], 10**recom_adas[neon][ac]["te"], 10**recom_adas[neon][ac]["rates"])

###################
ion_interp_cherab = {}
recom_interp_cherab = {}
for i in np.linspace(1, 10, 10):
    try:
        ion_interp_cherab[i-1] = adas.ionisation_rate(neon, int(i-1))
    except ValueError:
        pass
    try:
        recom_interp_cherab[i] = adas.recombination_rate(neon, int(i))
    except ValueError:
        pass



ion_balance_adas_origin = np.zeros((neon.atomic_number+1, 100))
ion_balance_adas_pow = np.zeros((neon.atomic_number+1, 100))
ion_balance_cherab = np.zeros((neon.atomic_number+1, 100))
for j, te in enumerate(electron_temperatures):
    ion_balance_adas_origin[:, j] = solve_ion_balance(electron_density*1e-6, te, ion_interp_adas_origin, recom_interp_adas_origin, True)
    ion_balance_adas_pow[:, j] = solve_ion_balance(electron_density*1e-6, te, ion_interp_adas_pow, recom_interp_adas_pow, False)
    ion_balance_cherab[:, j] = solve_ion_balance(electron_density, te, ion_interp_cherab, recom_interp_cherab, False)


if False:
    for i in range(neon.atomic_number+1):
        try:
            ionisation_rates_adas_origin = [10 ** ion_interp_adas_origin[i](np.log10(electron_density), np.log10(x)) * 1e-6 for x in electron_temperatures]
            ionisation_rates_adas_pow = [ion_interp_adas_pow[i](np.log10(electron_density), np.log10(x)) * 1e-6 for x in electron_temperatures]
            ionisation_rates_cherab = [ion_interp_cherab[i](electron_density, np.log10(x)) for x in electron_temperatures]
            plt.loglog(electron_temperatures, ionisation_rates, '.-', label='Ne{}'.format(i))
        except KeyError:
            continue
    plt.ylim(1E-21, 1E-10)
    plt.legend()
    plt.xlabel("Electron Temperature (eV)")
    plt.title("Ionisation Rates")


    plt.figure()
    for i in range(neon.atomic_number+1):
        try:
            recombination_rates = [10 ** recom_interp_adas_origin[i](np.log10(electron_density), np.log10(x)) * 1e-6 for x in electron_temperatures]
            plt.loglog(electron_temperatures, recombination_rates, '.-', label='Ne{}'.format(i))
        except KeyError:
            continue
    plt.ylim(1E-21, 1E-10)
    plt.legend()
    plt.xlabel("Electron Temperature (eV)")
    plt.title("Recombination Rates")


    plt.figure()
    for i in range(neon.atomic_number+1):
        plt.semilogx(electron_temperatures, ion_balance_adas_origin[i, :], '.-', label='Ne{} adas origin'.format(i))
        plt.semilogx(electron_temperatures, ion_balance_adas_pow[i, :], '.--', label='Ne{} adas 10^x'.format(i))
        plt.semilogx(electron_temperatures, ion_balance_cherab[i, :], '.:', label='Ne{} cherab'.format(i))

    plt.xlabel("Electron Temperature (eV)")
    plt.title('Fractional Abundance')
    plt.show()