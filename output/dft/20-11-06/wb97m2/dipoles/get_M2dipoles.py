import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

ang_to_bohr = 1.88973
and2_to_bohr2 = 3.571079
debye_to_e = 0.393456
e02_to_debye_ang = 1.345033669

with open(args.file, 'r') as file:
    f = file.read()

molecule_name = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.file).group(1)
basis = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.file).group(3)

def dipoles_from_energy(method, s):
    strings = re.finditer(r'({}).*'.format(method), s)
    strings = list(strings)
    energies = []
    for ele in [strings[-3], strings[-1]]:
        ele = ele.group()
        energies.append(float(re.search(r'\-?[0-9][0-9.]{2,}', ele).group()))
    if energies == []:
        return nan
    dipole = (energies[0] - energies[1]) / (0.0002) / debye_to_e
    return dipole

def mp2dipoles_from_energy(method, s):
    strings = re.finditer(r'({}).*'.format(method), s)
    strings = list(strings)
    energies = []
    for ele in [strings[-2], strings[-1]]:
        ele = ele.group()
        energies.append(float(re.search(r'\-?[0-9][0-9.]{2,}', ele).group()))
    if energies == []:
        return nan
    dipole = (energies[0] - energies[1]) / (0.0002) / debye_to_e
    return dipole

scf_dipole = dipoles_from_energy('Total energy in the final basis set', f)
scf_string = '{0} {1} {2}\n'.format(basis, molecule_name, scf_dipole)
with open('dipoles_scf_{0}.txt'.format(basis), 'a') as file:
    file.write(scf_string)

if basis != 'aug-cc-pcV5Zp':
    mp2_dipole = mp2dipoles_from_energy('MP2\s*total energy', f)
    mp2_string = '{0} {1} {2}\n'.format(basis, molecule_name, mp2_dipole)
    with open('dipoles_mp2_{0}.txt'.format(basis), 'a') as file:
        file.write(mp2_string)
