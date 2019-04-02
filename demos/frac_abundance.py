import numpy as np
import matplotlib.pyplot as plt
from cherab.core.atomic import carbon, neon, hydrogen
from cherab.openadas import OpenADAS

# initialise the atomic data provider
adas = OpenADAS(permit_extrapolation=True)

elem = neon
temperature_steps = 100
ne = 1E19
n0 = 1e16
numstates = elem.atomic_number + 1

# Collect rate coefficients
coef_ion = {}
coef_recom = {}
coef_tcx = {}
for i in np.arange(1, elem.atomic_number + 1):
    try:
        coef_ion[i - 1] = adas.ionisation_rate(elem, int(i - 1))
    except ValueError:
        pass
    try:
        coef_recom[i] = adas.recombination_rate(elem, int(i))
        coef_tcx[i] = adas.thermal_cx_rate(hydrogen, 0, elem, int(i))
    except ValueError:
        pass


def solve_ion_balance(element, n_e, t_e, nh0=None):
    atomic_number = element.atomic_number
    matbal = np.zeros((atomic_number + 1, atomic_number + 1))

    matbal[0, 0] -= coef_ion[0](n_e, t_e)
    matbal[0, 1] += coef_recom[1](n_e, t_e)
    matbal[-1, -1] -= coef_recom[atomic_number](n_e, t_e)
    matbal[-1, -2] += coef_ion[atomic_number - 1](n_e, t_e)

    if nh0 is not None:
        matbal[0, 1] += nh0 / n_e * coef_tcx[1](n_e, t_e)
        matbal[-1, -1] -= nh0 / n_e * coef_tcx[1](n_e, t_e)

    for i in range(1, atomic_number):
        matbal[i, i - 1] += coef_ion[i - 1](n_e, t_e)
        matbal[i, i] -= (coef_ion[i](n_e, t_e) + coef_recom[i](n_e, t_e))
        matbal[i, i + 1] += coef_recom[i + 1](n_e, t_e)
        if nh0 is not None:
            matbal[i, i] -= nh0 / n_e * coef_tcx[i](n_e, t_e)
            matbal[i, i + 1] += nh0 / n_e * coef_tcx[i + 1](n_e, t_e)

    matbal = np.concatenate((matbal, np.ones((1, matbal.shape[1]))), axis=0)
    matbal = np.concatenate((matbal, np.zeros((matbal.shape[0], 1))), axis=1)
    solution = np.zeros((matbal.shape[0]))
    solution[-1] = 1
    tmp = np.linalg.lstsq(matbal, solution, rcond=1e-120)[0][0:-1]

    return tmp


electron_temperatures = [10 ** x for x in np.linspace(np.log10(coef_recom[1].raw_data["te"].min()),
                                                      np.log10(coef_recom[1].raw_data["te"].max()),
                                                      num=temperature_steps)]

ion_balance = np.zeros((elem.atomic_number + 1, len(electron_temperatures)))
ion_balance_tcx = np.zeros((elem.atomic_number + 1, len(electron_temperatures)))
for j, te in enumerate(electron_temperatures):
    ion_balance[:, j] = solve_ion_balance(elem, ne, te)
    ion_balance_tcx[:, j] = solve_ion_balance(elem, ne, te, n0)

for i in range(elem.atomic_number + 1):
    try:
        ionisation_rates = [coef_ion[i](1E19, x) for x in electron_temperatures]
        plt.loglog(electron_temperatures, ionisation_rates, '-x', label='{0}{1}'.format(elem.symbol, i))
    except KeyError:
        continue
plt.ylim(1E-21, 1E-10)
plt.legend()
plt.xlabel("Electron Temperature (eV)")
plt.title("Ionisation Rates")

plt.figure()
for i in range(elem.atomic_number + 1):
    try:
        recombination_rates = [coef_recom[i](1E19, x) for x in electron_temperatures]
        plt.loglog(electron_temperatures, recombination_rates, '-x', label='{0}{1}'.format(elem.symbol, i))
    except KeyError:
        continue
plt.ylim(1E-21, 1E-10)
plt.legend()
plt.xlabel("Electron Temperature (eV)")
plt.title("Recombination Rates")

plt.figure()
for i in range(elem.atomic_number + 1):
    try:
        tcx_rates = [coef_tcx[i](1E19, x) for x in electron_temperatures]
        plt.loglog(electron_temperatures, tcx_rates, '-x', label='{0}{1}'.format(elem.symbol, i))
    except KeyError:
        continue
plt.ylim(1E-21, 1E-10)
plt.legend()
plt.xlabel("Electron Temperature (eV)")
plt.title(" Thermal Charge-Exchange Recombination Rates")

plt.figure()
for i in range(elem.atomic_number + 1):
    pl = plt.semilogx(electron_temperatures, ion_balance[i, :], label='{0}{1}'.format(elem.symbol, i))
    plt.semilogx(electron_temperatures, ion_balance_tcx[i, :], '--',
                 color=pl[0].get_color())
plt.plot([], [], "k-", label="nh0 = 0")
plt.plot([], [], "k--", label="nh0 = 1e16 m^-3")
plt.xlabel("Electron Temperature (eV)")
plt.title('Fractional Abundance')
plt.legend()
plt.show()
