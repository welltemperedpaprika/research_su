import re
import numpy as np
from pymatgen.core.periodic_table import Element

ang_to_bohr = 1.88973
ang2_to_bohr2 = 3.571079
debye_to_e = 0.3934303
ea02_to_debye_ang = 1.345033669
debye_ang_to_ea02 = 0.743477

def get_spin_polarization(string):
    info = re.search('(\<S\^2\>)\s=\s*(\-?[0-9][0-9.]*)', string).group(2)
    if float(info) == 0:
        return 0
    else:
        return 1

def get_electronic_dipole(string, dipole):
    info = re.search('molecule\s*\d\s\d\s([\s\S]*?)\$end', string).group(1)
    x = y = z = 0
    for l in info.splitlines():
        line = l.split()
        charge = Element(re.sub('\d+', '', line[0])).Z
        if len(line) == 1:
            line += [0, 0, 0]
        x += charge * float(line[1])
        y += charge * float(line[2])
        z += charge * float(line[3])
    x_elec = dipole[0] * debye_to_e - x * ang_to_bohr
    y_elec = dipole[1] * debye_to_e - y * ang_to_bohr
    z_elec = dipole[2] * debye_to_e - z * ang_to_bohr
    total_elec = np.sqrt(x_elec ** 2 + y_elec ** 2 + z_elec ** 2)
    return [x_elec, y_elec, z_elec, total_elec]

def get_electronic_quadrupole(string, quadrupole):
    info = re.search('molecule\s*\d\s\d\s([\s\S]*?)\$end', string).group(1)
    xx = yy = zz = 0
    for l in info.splitlines():
        line = l.split()
        charge = Element(re.sub('\d+', '', line[0])).Z
        if len(line) == 1:
            line += [0, 0, 0]
        xx += charge * float(line[1]) ** 2
        yy += charge * float(line[2]) ** 2
        zz += charge * float(line[3]) ** 2
    xx_elec = quadrupole[0] * debye_ang_to_ea02 - xx * ang2_to_bohr2
    yy_elec = quadrupole[1] * debye_ang_to_ea02 - yy * ang2_to_bohr2
    zz_elec = quadrupole[2] * debye_ang_to_ea02 - zz * ang2_to_bohr2
    return [xx_elec, yy_elec, zz_elec]

def get_stddev(string, dipole, quadrupole):
    info = re.search('molecule\s*\d\s\d\s([\s\S]*?)\$end', string).group(1)
    tote = int(re.search('molecule\s*(\d\s\d\s)', string).group(1).splitlines()[0].split()[0])
    for l in info.splitlines():
        line = l.split()
        charge = Element(re.sub('\d+', '', line[0])).Z
        tote += Element(re.sub('\d+', '', line[0])).Z
    xx_std = np.sqrt((quadrupole[0]/-tote) - (dipole[0]/-tote) ** 2)
    yy_std = np.sqrt((quadrupole[1]/-tote) - (dipole[1]/-tote) ** 2)
    zz_std = np.sqrt((quadrupole[2]/-tote) - (dipole[2]/-tote) ** 2)
    return [xx_std, yy_std, zz_std]
