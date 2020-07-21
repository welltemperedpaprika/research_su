import argparse
from pathlib import Path
import re
import json
from get_electronic import get_electronic_dipole, get_electronic_quadrupole, get_stddev
from get_quadrupoles_from_energy import get_quadrupoles_from_energy
from collections import defaultdict
import os

parser = argparse.ArgumentParser(description='Processes a qchem output file and stores it as a dictionary with relevant params.')
parser.add_argument('filename')
args = parser.parse_args()
molecule_name = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(1)
method = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(2)
basis = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(3)
output_path = Path.home() / "summer/research/output"

with open(output_path / "jacob_ladder.json") as f:
    jacob_ladder = json.load(f)
with open(args.filename, 'r') as file:
    s = file.read()
object = {"name": molecule_name, "method": method, "basis": basis}
method_type = ""
if method != "ccsdT" or method != "hf":
    method_type = "dft"
else:
    method_type = "wft"
object["method_type"] = method_type
if method_type == "dft":
    object["method_level"] = int(jacob_ladder[method])
    quadrupole_string = re.search(r'Quadrupole((.*\n){3})', s).group()
    quadrupole = re.findall(r'(\-?[0-9][0-9.]*)', quadrupole_string)
    object["quadrupoles"] = [float(quadrupole[0]), float(quadrupole[2]), float(quadrupole[5])]
    dipole_string = re.search(r'Dipole((.*\n){3})', s).group()
    dipole = re.findall(r'(\-?[0-9][0-9.]*)', dipole_string)
    object["dipoles"] = [float(x) for x in dipole]
    object["quadrupoles_elec"] = get_electronic_quadrupole(s, object["quadrupoles"])
    object["dipoles_elec"] = get_electronic_dipole(s, object["dipoles"])
    object["std_dev"] = get_stddev(s, object["dipoles_elec"], object["quadrupoles_elec"])

if method_type == "wft":
    if method == "ccsdT":
        object["quadrupoles_ccsdt"] = get_quadrupoles_from_energy('CCSD\(T\) total', s)
        object["quadrupoles_mp2"] = get_quadrupoles_from_energy('MP2 energy', s)
        object["quadrupoles_ccsd"] = get_quadrupoles_from_energy('CCSD total', s)
if os.path.exists(output_path/"output.json"):
    with open(output_path/"output.json") as f:
        data = json.load(f)
    if molecule_name not in data.keys():
        data[molecule_name] = []
    data[molecule_name].append(object)
    with open(output_path/"output.json", 'w') as outfile:
        json.dump(data, outfile)
else:
    data = defaultdict(list)
    data[molecule_name].append(object)
    with open(output_path/"output.json", 'w') as outfile:
        json.dump(data, outfile)

print('{0} wrote to json completed.'.format(args.filename))
