import re
import numpy as np

ang_to_bohr = 1.88973
and2_to_bohr2 = 3.571079
debye_to_e = 0.3934303
e02_to_debye_ang = 1.345033669

def quadrupoles_from_energy(method, s):
    strings = re.finditer(r'{}'.format(method), s)
    energies = []
    for ele in strings[1:7]:
        ele = ele.group()
        energies.append(float(re.search(r'\-?[0-9][0-9.]{2,}', ele).group()))
    quadrupoles = []
    for i in range(len(energies) - 1):
        quadrupoles.append((energies[i] - energies[i + 1]) / (0.0002) * e02_to_debye_ang)
    return quadrupoles
