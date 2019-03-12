
import numpy as np
import matplotlib.pyplot as plt
from cherab.core.atomic import neon
from cherab.openadas import OpenADAS


# initialise the atomic data provider
adas = OpenADAS(permit_extrapolation=True)

electron_temperatures = [10**x for x in np.linspace(np.log10(1), np.log10(1000), num=100)]
ne = 1E18

numstates = neon.atomic_number + 1

# Collect rate coefficients
coef_ion = {}
coef_recom = {}
for i in np.linspace(1, 10, 10):
    try:
        coef_ion[i] = adas.ionisation_rate(neon, int(i))
    except ValueError:
        pass
    try:
        coef_recom[i] = adas.recombination_rate(neon, int(i))
    except ValueError:
        pass


def solve_ion_balance(ne, te):

    matbal = np.zeros((numstates, numstates))

    matbal[0, 0] -= coef_ion[1](ne, te)
    matbal[0, 1] += coef_recom[1](ne, te)
    matbal[-1, -1] -= coef_recom[9](ne, te)
    matbal[-1, -2] += coef_ion[10](ne, te)

    for i in range(1, numstates - 1):
        matbal[i, i - 1] += coef_ion[i](ne, te)
        matbal[i, i] -= (coef_ion[i + 1](ne, te) + coef_recom[i](ne, te))
        matbal[i, i + 1] += coef_recom[i + 1](ne, te)

    matbal = np.concatenate((matbal, np.ones((1, matbal.shape[1]))), axis=0)
    matbal = np.concatenate((matbal, np.zeros((matbal.shape[0], 1))), axis=1)
    solution = np.zeros((matbal.shape[0]))
    solution[-1] = 1
    tmp = np.linalg.lstsq(matbal, solution)[0][0:-1]

    return tmp


ion_balance = np.zeros((neon.atomic_number+1, 100))
for j, te in enumerate(electron_temperatures):
    ion_balance[:, j] = solve_ion_balance(ne, te)


for i in range(neon.atomic_number+1):
    try:
        ionisation_rates = [coef_ion[i](1E19, x) for x in electron_temperatures]
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
        recombination_rates = [coef_recom[i](1E19, x) for x in electron_temperatures]
        plt.loglog(electron_temperatures, recombination_rates, '.-', label='Ne{}'.format(i))
    except KeyError:
        continue
plt.ylim(1E-21, 1E-10)
plt.legend()
plt.xlabel("Electron Temperature (eV)")
plt.title("Recombination Rates")


plt.figure()
for i in range(neon.atomic_number+1):
    plt.semilogx(electron_temperatures, ion_balance[i, :], '.-', label='Ne{}'.format(i))
plt.xlabel("Electron Temperature (eV)")
plt.title('Fractional Abundance')
plt.show()



