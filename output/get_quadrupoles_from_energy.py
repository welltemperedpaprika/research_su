import re
import numpy as np

ang_to_bohr = 1.88973
and2_to_bohr2 = 3.571079
debye_to_e = 0.3934303
e02_to_debye_ang = 1.345033669

def quadrupoles_from_energy(method, s):
    strings = re.finditer(r'({}).*'.format(method), s)
    strings = list(strings)
    energies = []
    for ele in strings[1:7]:
        ele = ele.group()
        energies.append(float(re.search(r'\-?[0-9][0-9.]{2,}', ele).group()))
    quadrupoles = []
    for i in range(0, len(energies), 2):
        quadrupoles.append((energies[i] - energies[i + 1]) / (0.0002) * e02_to_debye_ang)
    return quadrupoles

def dipoles_from_energy(method, s):
    strings = re.finditer(r'({}).*'.format(method), s)
    strings = list(strings)
    energies = []
    for ele in strings[7:len(strings)]:
        ele = ele.group()
        energies.append(float(re.search(r'\-?[0-9][0-9.]{2,}', ele).group()))
    dipoles = []
    for i in range(0, len(energies), 2):
        dipoles.append((energies[i] - energies[i + 1]) / (0.0002) / debye_to_e)
    return dipoles
