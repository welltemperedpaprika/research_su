import argparse
from pathlib import Path
import re, sys
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('molecule')
parser.add_argument('method')
parser.add_argument('basis')
parser.add_argument('-mf', '--multipole_field', nargs='+', help='specify multipole field in direction')
parser.add_argument('-s', '--strength', nargs='+', type=float, help='specify field strength')
args = parser.parse_args()

input_path = Path.home() / "summer/research/geometries/geometries"
filename = input_path / "{}.xyz".format(args.molecule)

with open(filename, 'r') as file:
    molecule = file.read()
output_name = "{0}_{1}_{2}.inp".format(args.molecule, args.method, args.basis)
if path.exists(output_name):
    sys.exit('{0} already in path!'.format(output_name))

if args.method != 'ccsdT':
    if args.method == 'Slater':
        method_line = 'exchange slater'
    else:
        method_line = 'method {0}'.format(args.method)
    input = molecule + '''
$rem
jobtype sp
{0}
xc_grid 000099000590
basis {1}
max_scf_cycles 200
thresh 14
scf_convergence 8
scf_algorithm gdm
symmetry false
sym_ignore true
unrestricted true
gen_scfman true
internal_stability_iter 15
internal_stability_davidson_iter 200
mem_total 64000
mem_static 1500
n_frozen_core 0
$end

    '''.format(method_line, args.basis)
    if args.multipole_field is not None:
        multipole_field = args.multipole_field[0].split()
        for c, i in enumerate(multipole_field):
            input += '''
@@@@@@
$molecule
read
$end

$rem

jobtype sp
{0}
xc_grid 000099000590
basis {1}
max_scf_cycles 200
thresh 14
scf_convergence 8
mem_total 64000
mem_static 1500
symmetry false
sym_ignore true
scf_guess read
unrestricted true
scf_algorithm gdm
$end

$multipole_field
{2} {3}
$end

    '''.format(method_line, args.basis, i, args.strength[c])

if args.method == 'ccsdT':
    input = molecule + '''
$rem
jobtype sp
method {0}
xc_grid 000099000590
basis {1}
max_scf_cycles 200
thresh 14
scf_convergence 8
scf_algorithm gdm
symmetry false
sym_ignore true
unrestricted true
gen_scfman true
internal_stability_iter 15
internal_stability_davidson_iter 200
mem_total 128000
cc_memory 96000
cc_backend xm
mem_static 1500
n_frozen_core 0
$end

    '''.format('CCSD(T)', args.basis)

    if args.multipole_field is not None:
        multipole_field = args.multipole_field[0].split()
        for c, i in enumerate(multipole_field):
            input += '''
@@@@@@
$molecule
read
$end

$rem

jobtype sp
method {0}
xc_grid 000099000590
basis {1}
max_scf_cycles 200
thresh 14
scf_convergence 8
mem_total 128000
cc_memory 96000
cc_backend xm
mem_static 1500
symmetry false
sym_ignore true
scf_guess read
unrestricted true
scf_algorithm gdm
n_frozen_core 0
$end

$multipole_field
{2} {3}
$end

        '''.format('CCSD(T)', args.basis, i, args.strength[c])
with open(output_name, 'w') as f:
    f.write(input)
print('Input file created for {0} with method {1} and basis {2}'.format(args.molecule, args.method, args.basis))
