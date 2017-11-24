
from cherab.core.atomic import carbon
from cherab.openadas import OpenADAS


adas = OpenADAS()

myrate = adas.impact_excitation_rate(carbon, 1, ("2s1 2p1 3d1 2D4.5", "2s2 4d1 2D4.5"))


