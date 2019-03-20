from cherab.openadas.parse.adf11 import parse_adf11
from cherab.openadas import repository
from cherab.core.atomic import neon
from cherab.openadas import OpenADAS
from cherab.openadas.parse import parse_adf11
from cherab.core.utility import RecursiveDict, Cm3ToM3, PerCm3ToPerM3
import numpy as np
from cherab.core.math import Interpolate2DCubic
import matplotlib.pyplot as plt


def solve_ion_balance(ne_b, te_b, ion_interpol, recom_interpol, log = False):
    """
    solves ionisation balance
    """
    matbal = np.zeros((numstates, numstates))

    if log:
        ne_b = np.log10(ne_b)
        te_b = np.log10(te_b)

        matbal[0, 0] -= 10 ** ion_interpol[0](ne_b, te_b)
        matbal[0, 1] += 10 ** recom_interpol[1](ne_b, te_b)
        matbal[-1, -1] -= 10 ** recom_interpol[10](ne_b, te_b)
        matbal[-1, -2] += 10 ** ion_interpol[9](ne_b, te_b)

        for i in range(1, numstates - 1):
            matbal[i, i - 1] += 10 ** ion_interpol[i - 1](ne_b, te_b)
            matbal[i, i] -= (10 ** ion_interpol[i](ne_b, te_b) + 10 ** recom_interpol[i](ne_b, te_b))
            matbal[i, i + 1] += 10 ** recom_interpol[i + 1](ne_b, te_b)
    else:
        matbal[0, 0] -= ion_interpol[0](ne_b, te_b)
        matbal[0, 1] += recom_interpol[1](ne_b, te_b)
        matbal[-1, -1] -= recom_interpol[10](ne_b, te_b)
        matbal[-1, -2] += ion_interpol[9](ne_b, te_b)

        for i in range(1, numstates - 1):
            matbal[i, i - 1] += ion_interpol[i - 1](ne_b, te_b)
            matbal[i, i] -= (ion_interpol[i](ne_b, te_b) + recom_interpol[i](ne_b, te_b))
            matbal[i, i + 1] += recom_interpol[i + 1](ne_b, te_b)


    matbal = np.concatenate((matbal, np.ones((1, matbal.shape[1]))), axis=0)
    matbal = np.concatenate((matbal, np.zeros((matbal.shape[0], 1))), axis=1)
    solution = np.zeros((matbal.shape[0]))
    solution[-1] = 1

    fracabun = np.linalg.lstsq(matbal, solution, rcond=1e-60)[0][0:-1]

    return fracabun



adas = OpenADAS(permit_extrapolation=False)



numstates = neon.atomic_number + 1

electron_density = 1e19
electron_temperatures = np.power(10, np.linspace(-0.69877, 4.1, num=500))

ion_adas = parse_adf11(neon, "/compass/home/tomes/.cherab/openadas/download_cache/adf11/scd96/scd96_ne.dat")
recom_adas = parse_adf11(neon, "/compass/home/tomes/.cherab/openadas/download_cache/adf11/acd96/acd96_ne.dat")


############Create interpolators on adas data in log10 number format
ion_interp_adas_origin = {}
recom_interp_adas_origin = {}
for i in range(neon.atomic_number):
    ac = i+1
    ion_interp_adas_origin[i] = Interpolate2DCubic(ion_adas[neon][ac]["ne"], ion_adas[neon][ac]["te"], ion_adas[neon][ac]["rates"])
    recom_interp_adas_origin[ac] = Interpolate2DCubic(recom_adas[neon][ac]["ne"], recom_adas[neon][ac]["te"], recom_adas[neon][ac]["rates"])

#############Create interpolators on adas data in normal number format
ion_interp_adas_pow = {}
recom_interp_adas_pow = {}
for i in range(neon.atomic_number):
    ac = i+1
    ion_interp_adas_pow[i] = Interpolate2DCubic(10**ion_adas[neon][ac]["ne"], 10**ion_adas[neon][ac]["te"], 10**ion_adas[neon][ac]["rates"])
    recom_interp_adas_pow[ac] = Interpolate2DCubic(10**recom_adas[neon][ac]["ne"], 10**recom_adas[neon][ac]["te"], 10**recom_adas[neon][ac]["rates"])

################### CHerab interpolators from the cherab-openadas database
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


#solve ionisation balance for given temperatures and density
ion_balance_adas_origin = np.zeros((neon.atomic_number+1, electron_temperatures.shape[0]))
ion_balance_adas_pow = np.zeros((neon.atomic_number+1, electron_temperatures.shape[0]))
ion_balance_cherab = np.zeros((neon.atomic_number+1, electron_temperatures.shape[0]))
for j, te in enumerate(electron_temperatures):
    ion_balance_adas_origin[:, j] = solve_ion_balance(PerCm3ToPerM3.inv(electron_density), te, ion_interp_adas_origin, recom_interp_adas_origin, True)
    ion_balance_adas_pow[:, j] = solve_ion_balance(PerCm3ToPerM3.inv(electron_density), te, ion_interp_adas_pow, recom_interp_adas_pow, False)
    ion_balance_cherab[:, j] = solve_ion_balance(electron_density, te, ion_interp_cherab, recom_interp_cherab, False)

#just some plots
if False:
    fig_ionisation = plt.subplots(figsize=(12, 7))
    ax = fig_ionisation[1]
    fig_ionisation[0].subplots_adjust(right=0.7)
    for i in range(neon.atomic_number+1):
        try:
            ionisation_rates_adas_origin = [Cm3ToM3.to(10 ** ion_interp_adas_origin[i](np.log10(PerCm3ToPerM3.inv(electron_density)), np.log10(x))) for x in electron_temperatures]
            ionisation_rates_adas_pow = [Cm3ToM3.to(ion_interp_adas_pow[i](PerCm3ToPerM3.inv(electron_density), x)) for x in electron_temperatures]
            ionisation_rates_cherab = [ion_interp_cherab[i](electron_density, x) for x in electron_temperatures]
            tmp = ax.loglog(electron_temperatures, ionisation_rates_adas_origin, '-', label='Ne{}'.format(i), alpha =0.5)
            ax.loglog(electron_temperatures, ionisation_rates_adas_pow, '--', color=tmp[0].get_color(), alpha = 0.5)
            ax.loglog(electron_temperatures, ionisation_rates_cherab, ':', color=tmp[0].get_color())
        except KeyError:
            continue

    ax.plot([], [], "k-",label="adas origin")
    ax.plot([], [], "k--", label="adas power10")
    ax.plot([], [], "k:", label="cherab")
    ax.set_ylim(1E-23, 1E-11)
    ax.legend(loc=(1.05,0.1))
    ax.set_xlabel("Electron Temperature (eV)")
    ax.set_ylabel("ionisation rate [m^3s^-1]")
    ax.set_title("Ionisation Rates")
    fig_ionisation[0].tight_layout()


    fig_recombination = plt.subplots(figsize=(12, 7))
    ax = fig_recombination[1]
    fig_recombination[0].subplots_adjust(right=0.7)
    for i in range(1, neon.atomic_number+1):
        try:
            recombination_rates_adas_origin = [Cm3ToM3.to(10 ** recom_interp_adas_origin[i](np.log10(PerCm3ToPerM3.inv(electron_density)), np.log10(x))) for x in electron_temperatures]
            recombination_rates_adas_pow = [Cm3ToM3.to(recom_interp_adas_pow[i](PerCm3ToPerM3.inv(electron_density), x)) for x in electron_temperatures]
            recombination_rates_cherab = [recom_interp_cherab[i](electron_density, x) for x in electron_temperatures]
            tmp = ax.loglog(electron_temperatures, recombination_rates_adas_origin, '-', label='Ne{}'.format(i), alpha =0.5)
            ax.loglog(electron_temperatures, recombination_rates_adas_pow, '--', color=tmp[0].get_color(), alpha = 0.5)
            ax.loglog(electron_temperatures, recombination_rates_cherab, ':', color=tmp[0].get_color())
        except KeyError:
            continue
    ax.plot([], [], "k-",label="adas origin")
    ax.plot([], [], "k--", label="adas power10")
    ax.plot([], [], "k:", label="cherab")
    plt.ylim(1E-21, 1E-15)
    plt.legend(loc=(1.05,0.1))
    plt.xlabel("Electron Temperature (eV)")
    ax.set_ylabel("ionisation rate [m^3s^-1]")
    plt.title("Recombination Rates")
    fig_recombination[0].tight_layout()


    fig_ionbal = plt.subplots(figsize=(12, 7))
    ax = fig_ionbal[1]
    fig_ionbal[0].subplots_adjust(right=0.7)
    for i in range(neon.atomic_number+1):
        tmp = ax.semilogx(electron_temperatures, ion_balance_adas_origin[i, :], '-', label='Ne{}'.format(i), alpha = 0.5)
        ax.semilogx(electron_temperatures, ion_balance_adas_pow[i, :], '--', color=tmp[0].get_color(), alpha = 0.5)
        ax.semilogx(electron_temperatures, ion_balance_cherab[i, :], ':', color=tmp[0].get_color())


    ax.plot([], [], "k-",label="adas origin")
    ax.plot([], [], "k--", label="adas power10")
    ax.plot([], [], "k:", label="cherab")
    ax.legend(loc=(1.05,0.1))
    ax.set_xlabel("Electron Temperature (eV)")
    ax.set_ylabel("abundance [a.u.]")
    ax.set_title('Fractional Abundance')
    ax.set_ylim((0,1.2))
    fig_ionbal[0].tight_layout()


    fig_ionbal_part = plt.subplots()
    ax = fig_ionbal_part[1]
    for i in range(1):
        tmp = ax.semilogx(electron_temperatures, ion_balance_adas_origin[i, :], '-', label='Ne{}'.format(i))
        ax.semilogx(electron_temperatures, ion_balance_adas_pow[i, :], '--', color=tmp[0].get_color())
        ax.semilogx(electron_temperatures, ion_balance_cherab[i, :], ':', color=tmp[0].get_color())

    ax.plot([], [], "k-",label="adas origin")
    ax.plot([], [], "k--", label="adas power10")
    ax.plot([], [], "k:", label="cherab")
    ax.set_xlim(1,10)
    ax.set_ylim(0,1.2)
    ax.legend()
    plt.xlabel("Electron Temperature (eV)")
    plt.title('Fractional Abundance')
    plt.show()
