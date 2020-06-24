import re
import numpy as np
from pymatgen.core.periodic_table import Element

ang_to_bohr = 1.88973
and2_to_bohr2 = 3.571079
debye_to_e = 0.3934303
e02_to_debye_ang = 1.345033669

def get_electronic_dipole(string, dipole):
    info = re.search('molecule\s*\d\s\d\s([\s\S]*?)\$end', string).group(1)
    x = y = z = 0
    for l in info.splitlines():
        line = l.split()
        charge = Element(line[0][0]).Z
        x += charge * float(line[1])
        y += charge * float(line[2])
        z += charge * float(line[3])
    x_elec = dipole[0] * debye_to_e - x
    y_elec = dipole[1] * debye_to_e - y
    z_elec = dipole[2] * debye_to_e - z
    total_elec = np.sqrt(x_elec ** 2 + y_elec ** 2 + z_elec ** 2)
    return [x_elec, y_elec, z_elec, total_elec]

def get_electronic_quadrupole(string, quadrupole):
    info = re.search('molecule\s*\d\s\d\s([\s\S]*?)\$end', string).group(1)
    xx = yy = zz = 0
    for l in info.splitlines():
        line = l.split()
        charge = Element(line[0][0]).Z
        xx += charge * float(line[1]) ** 2
        yy += charge * float(line[2]) ** 2
        zz += charge * float(line[3]) ** 2
    xx_elec = quadrupole[0] * e02_to_debye_ang - xx
    yy_elec = quadrupole[1] * e02_to_debye_ang - yy
    zz_elec = quadrupole[2] * e02_to_debye_ang - zz
    return [xx_elec, yy_elec, zz_elec]

def get_stddev(string, dipole, quadrupole):
    info = re.search('molecule\s*\d\s\d\s([\s\S]*?)\$end', string).group(1)
    tote = 0
    for l in info.splitlines():
        line = l.split()
        charge = Element(line[0][0]).Z
        tote += Element(line[0][0]).Z
    xx_std = np.sqrt((quadrupole[0]/-tote) - (dipole[0]/-tote) ** 2)
    yy_std = np.sqrt((quadrupole[1]/-tote) - (dipole[1]/-tote) ** 2)
    zz_std = np.sqrt((quadrupole[2]/-tote) - (dipole[2]/-tote) ** 2)
    return [xx_std, yy_std, zz_std]
