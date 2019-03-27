from cherab.openadas.parse.adf11 import parse_adf11
from cherab.openadas import repository
from cherab.core.atomic import neon, hydrogen
from cherab.openadas import OpenADAS
from cherab.openadas.parse import parse_adf11
from cherab.core.utility import RecursiveDict, Cm3ToM3, PerCm3ToPerM3
import numpy as np
from cherab.core.math import Interpolate2DCubic
import matplotlib.pyplot as plt
import unittest
from cherab.openadas.rates.atomic import IonisationRate, RecombinationRate, ThermalCXRate

class TestADAS2CherabChargeConvention(unittest.TestCase):

   def testIonisingCharge(self):

        adas = OpenADAS(permit_extrapolation=False)
        #todo get a list of all elements and test
        elem = neon
        #test if ionisation rates for Z=0 to Z=atomic_number-1 exist as they should
        for i in range(elem.atomic_number):
            self.assertIsInstance(adas.ionisation_rate(ion=elem, charge=0), IonisationRate,
                                  "Ionisation of {}{}+ is missing".format(elem.symbol, i))

        #test if ionisation of bare nucleus is not available
        self.assertRaises(RuntimeError, adas.ionisation_rate, ion=elem, charge=elem.atomic_number)


   def testRecombiningCharge(self):

       adas = OpenADAS(permit_extrapolation=False)
       #todo get a list of all elements and test
       elem = neon
       #test if ionisation rates for Z=1 to Z=atomic_number exist as they should
       for i in range(1, elem.atomic_number+1):
           self.assertIsInstance(adas.recombination_rate(ion=elem, charge=i), RecombinationRate,
                                 "Recombination of {}{}+ is missing".format(elem.symbol, i))

       #test if ionisation of bare nucleus is not available
       self.assertRaises(RuntimeError, adas.recombination_rate, ion=elem, charge=0)

   def testCXCharge(self):

       adas = OpenADAS(permit_extrapolation=False)
       #todo get a list of all elements and test
       elem = neon
       donot = hydrogen
       #test if thermal cx rates for Z=1 to Z=atomic_number exist as they should
       for i in range(1, elem.atomic_number+1):
           self.assertIsInstance(adas.thermal_cx_rate(donor_element=hydrogen, donor_charge=0, receiver_element=elem, receiver_charge=i),
                                 ThermalCXRate, "Recombination of {}{}+ is missing".format(elem.symbol, i))

       #test if ionisation of bare nucleus is not available
       self.assertRaises(RuntimeError, adas.thermal_cx_rate, donor_element=hydrogen, donor_charge=0,
                         receiver_element=elem, receiver_charge=0)

if __name__ == "__main__":
    unittest.main()
