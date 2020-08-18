import argparse
from pathlib import Path
import re
import json
from get_electronic import get_electronic_dipole, get_electronic_quadrupole, get_stddev, get_spin_polarization
from get_quadrupoles_from_energy import quadrupoles_from_energy, dipoles_from_energy
from collections import defaultdict
import os

def find(l, molecule, method, basis):
    for c, e in enumerate(l):
        if e['name'] == molecule and e['method'] == method and e['basis'] == basis:
            return c
    return False

parser = argparse.ArgumentParser(description='Processes a qchem output file and stores it as a dictionary with relevant params.')
parser.add_argument('filename')
args = parser.parse_args()
molecule_name = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(1)
method = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(2)
if method == 'MGGA':
    method = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(2) + "_" +re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(3)
    basis = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(4)
else:
    basis = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(3)
output_path = Path.home() / "summer/research/output"

with open(output_path / "jacob_ladder.json") as f:
    jacob_ladder = json.load(f)
with open(Path(args.filename), 'r') as file:
    s = file.read()
object = {"name": molecule_name, "method": method, "basis": basis}
method_type = ""
if method != "ccsdT" and method != "hf":
    method_type = "dft"
else:
    method_type = "wft"
object["method_type"] = method_type
if method_type == "dft":
    object["method_level"] = int(jacob_ladder[method])
    quadrupole_string = re.search(r'Quadrupole((.*\n){3})', s).group()
    quadrupole = re.findall(r'(\-?[0-9][0-9.]*)', quadrupole_string)
    object["quadrupoles"] = [float(quadrupole[0]), float(quadrupole[2]), float(quadrupole[5])]
    object["quadrupoles_off_diag"] = [float(quadrupole[1]), float(quadrupole[3]), float(quadrupole[4])] #XY XZ XY
    dipole_string = re.search(r'Dipole((.*\n){3})', s).group()
    dipole = re.findall(r'(\-?[0-9][0-9.]*)', dipole_string)
    object["dipoles"] = [float(x) for x in dipole]
    object["quadrupoles_elec"] = get_electronic_quadrupole(s, object["quadrupoles"])
    object["dipoles_elec"] = get_electronic_dipole(s, object["dipoles"])
    object["std_dev"] = get_stddev(s, object["dipoles_elec"], object["quadrupoles_elec"])
    object["spin_polarized"] = get_spin_polarization(s)
if method_type == "wft":
    if method == "ccsdT":
        object["quadrupoles_ccsdt"] = quadrupoles_from_energy('CCSD\(T\) total', s)
        object["quadrupoles_mp2"] = quadrupoles_from_energy('MP2 energy', s)
        object["quadrupoles_ccsd"] = quadrupoles_from_energy('CCSD total', s)
        quadrupole_string = re.search(r'Quadrupole((.*\n){3})', s).group()
        quadrupole = re.findall(r'(\-?[0-9][0-9.]*)', quadrupole_string)
        object["quadrupoles_hf"] = [float(quadrupole[0]), float(quadrupole[2]), float(quadrupole[5])]
        object["dipoles_ccsdt"] = dipoles_from_energy('CCSD\(T\) total', s)
        object["dipoles_mp2"] = dipoles_from_energy('MP2 energy', s)
        object["dipoles_ccsd"] = dipoles_from_energy('CCSD total', s)
        dipole_string = re.search(r'Dipole((.*\n){3})', s).group()
        dipole = re.findall(r'(\-?[0-9][0-9.]*)', dipole_string)
        object["dipoles_hf"] = [float(x) for x in dipole]
        object["spin_polarized"] = get_spin_polarization(s)
    if method == 'hf':
        object["quadrupoles_ccsdt"] = [0, 0, 0]
        object["quadrupoles_mp2"] = [0, 0, 0]
        object["quadrupoles_ccsd"] = [0, 0, 0]
        quadrupole_string = re.search(r'Quadrupole((.*\n){3})', s).group()
        quadrupole = re.findall(r'(\-?[0-9][0-9.]*)', quadrupole_string)
        object["quadrupoles_hf"] = [float(quadrupole[0]), float(quadrupole[2]), float(quadrupole[5])]
        object["dipoles_ccsdt"] = [0, 0, 0, 0]
        object["dipoles_mp2"] = [0, 0, 0, 0]
        object["dipoles_ccsd"] = [0, 0, 0, 0]
        dipole_string = re.search(r'Dipole((.*\n){3})', s).group()
        dipole = re.findall(r'(\-?[0-9][0-9.]*)', dipole_string)
        object["dipoles_hf"] = [float(x) for x in dipole]
        object["spin_polarized"] = get_spin_polarization(s)

if os.path.exists(output_path/"output.json"):
    with open(output_path/"output.json") as f:
        data = json.load(f)
    if molecule_name not in data.keys():
        data[molecule_name] = []
    c = find(data[molecule_name], molecule_name, method, basis)
    if c is False:
        data[molecule_name].append(object)
    else:
        data[molecule_name][c] = object
        print('{0} values updated.'.format(args.filename))
    with open(output_path/"output.json", 'w') as outfile:
        json.dump(data, outfile)

print('{0} wrote to json completed.'.format(args.filename))
