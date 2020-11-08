import argparse
from pathlib import Path
import re, sys
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('molecule')
parser.add_argument('method')
parser.add_argument('basis')
parser.add_argument('-dh', '--double_hybrid', default=False, type=lambda x: (str(x).lower() == 'true'))
parser.add_argument('-os', '--old_stability', default=False, type=lambda x: (str(x).lower() == 'true'))
parser.add_argument('-ur', '--unrestricted', default=True, type=lambda x: (str(x).lower() == 'true'))
parser.add_argument('-mf', '--multipole_field', nargs='+', help='specify multipole field in direction')
parser.add_argument('-aly', '--analytic', default=False, type=lambda x: (str(x).lower() == 'true'))
parser.add_argument('-s', '--strength', nargs='+', type=float, help='specify field strength')
parser.add_argument('-ow', '--overwrite', default=False, type=lambda x: (str(x).lower() == 'true'))
parser.add_argument('-opt', '--optimize', default=False, type=lambda x: (str(x).lower() == 'true'))
args = parser.parse_args()

input_path = Path.home() / "summer/research/geometries/geometries"
basis_path = Path.home() / "summer/research/geometries/basis"
filename = input_path / "{}.xyz".format(args.molecule)

with open(filename, 'r') as file:
    molecule = file.read()
output_name = "{0}_{1}_{2}.inp".format(args.molecule, args.method, args.basis)
if not args.overwrite:
    if path.exists(output_name):
        sys.exit('{0} already in path!'.format(output_name))

def write(input_string):
    with open(output_name, 'w') as f:
        f.write(input_string)
    print('Input file created for {0} with method {1} and basis {2}'.format(args.molecule, args.method, args.basis))

ur = args.unrestricted
basis = args.basis
if args.method == 'wB97X-2TQZ':
    args.method = 'wB97X-2(TQZ)'
if args.method == 'XYGJ-OS':
    args.method = 'XYGJOS'
if args.method == 'wB97M2':
    args.method = 'wB97M(2)'
if args.analytic:
    input = molecule + '''
$rem
method {0}
basis {1}
CC_REF_PROP true
cc_fullresponse true
n_frozen_core 0
scf_convergence 8
scf_algorithm gdm
thresh 14
symmetry false
sym_ignore true
cc_memory 128000
mem_total 156000
mem_static  1500
internal_stability_iter 15
$end
'''.format(args.method, basis)
    write(input)
    sys.exit()

if args.method != 'ccsdT' and not args.double_hybrid:
    if args.method == 'Slater':
        method_line = 'exchange slater'
    else:
        method_line = 'method {0}'.format(args.method)
    basis_real = ''
    if args.basis == 'aug-cc-pcV5Z':
        if args.molecule in ['LiBH4', 'LiCl', 'Li', 'BeH2', 'BeH', 'NaCl', 'LiH', 'Na', 'Na2', 'Mg', 'Mg2', 'NaLi', 'NaH', 'Be']:
            basis = 'gen'
            basis_file = basis_path / "{0}.txt".format(args.molecule)
            with open(basis_file, 'r') as f:
                basis_real = f.read()
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
unrestricted {2}
gen_scfman true
internal_stability_iter 15
internal_stability_davidson_iter 200
mem_total 64000
mem_static 1500
n_frozen_core 0
$end

{3}
    '''.format(method_line, basis, ur, basis_real)
    if args.old_stability:
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
gen_scfman false
stability_analysis true
symmetry false
sym_ignore true
unrestricted {2}
gen_scfman true
mem_total 64000
mem_static 1500
n_frozen_core 0
max_cis_cycles 200
$end

{3}'''.format(method_line, basis, ur, basis_real)
    if args.optimize:
        input = molecule + '''
$rem
jobtype opt
{0}
basis {1}
symmetry false
sym_ignore true
thresh 14
mem_total 32000
mem_static 1500
$end
'''.format(method_line, basis)

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
unrestricted {2}
scf_algorithm gdm
$end

$multipole_field
{3} {4}
$end

{5}
    '''.format(method_line, args.basis, ur, i, args.strength[c], basis_real)
    write(input)
    sys.exit()

if args.method == 'ccsdT':
    basis_real = ''
    if args.basis == 'aug-cc-pcV5Z':
        if args.molecule in ['LiBH4', 'LiCl', 'Li', 'BeH2', 'BeH', 'NaCl', 'LiH', 'Na', 'Na2', 'Mg', 'Mg2', 'NaLi', 'NaH', 'Be']:
            basis = 'gen'
            basis_file = basis_path / "{0}.txt".format(args.molecule)
            with open(basis_file, 'r') as f:
                basis_real = f.read()
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
unrestricted {2}
gen_scfman true
internal_stability_iter 15
internal_stability_davidson_iter 200
mem_total 128000
cc_memory 96000
cc_backend xm
mem_static 1500
n_frozen_core 0
$end

{3}
    '''.format('CCSD(T)', basis, ur, basis_real)

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
unrestricted {2}
scf_algorithm gdm
n_frozen_core 0
$end

$multipole_field
{3} {4}
$end

{5}

        '''.format('CCSD(T)', basis, ur, i, args.strength[c], basis_real)
    write(input)
    sys.exit()

if args.double_hybrid == True:
    basis_real = ''
    aux_basis = ''
    basis = args.basis
    gen_scfman = 'true'
    if args.method == 'XYGJOS':
        if args.basis == 'aug-cc-pcVTZ':
            aux_basis = 'aux_basis rimp2-aug-cc-pVTZ'
        if args.basis == 'aug-cc-pcVQZ' or args.basis == 'aug-cc-pcV5Z':
            aux_basis = 'aux_basis rimp2-aug-cc-pVQZ'
        if args.molecule in ['LiBH4', 'LiCl', 'Li', 'BeH2', 'BeH', 'NaCl', 'LiH', 'Na', 'Na2', 'Mg', 'Mg2', 'NaLi', 'NaH', 'Be']:
            if args.basis == 'aug-cc-pcVTZ':
                aux_basis = 'aux_basis rimp2-cc-pVTZ'
            if args.basis == 'aug-cc-pcVQZ' or args.basis == 'aug-cc-pcV5Z':
                aux_basis = 'aux_basis rimp2-cc-pVQZ'
    if args.basis == 'aug-cc-pcV5Z':
        if args.molecule in ['LiBH4', 'LiCl', 'Li', 'BeH2', 'BeH', 'NaCl', 'LiH', 'Na', 'Na2', 'Mg', 'Mg2', 'NaLi', 'NaH', 'Be']:
            basis = 'gen'
            basis_file = basis_path / "{0}.txt".format(args.molecule)
            with open(basis_file, 'r') as f:
                basis_real = f.read()
        f_c = 500
    else:
        f_c = 0
    if args.method != 'wB97M(2)':
        input = molecule + '''
$rem
jobtype sp
exchange {0}
xc_grid 000099000590
basis {1}
{2}
max_scf_cycles 200
thresh 14
scf_convergence 8
scf_algorithm gdm
symmetry false
sym_ignore true
unrestricted false
gen_scfman {3}
internal_stability_iter 15
internal_stability_davidson_iter 200
mem_total 128000
cc_memory 96000
cc_backend xm
mem_static 1500
n_frozen_core {4}
$end

{5}
'''.format(args.method, basis, aux_basis, gen_scfman, f_c, basis_real)

    if args.method == 'wB97M(2)':
        input = molecule + '''
$rem
jobtype sp
method wB97M-V
xc_grid 000099000590
basis {0}
max_scf_cycles 200
thresh 14
scf_convergence 8
scf_algorithm gdm
symmetry false
sym_ignore true
unrestricted false
gen_scfman true
internal_stability_iter 15
internal_stability_davidson_iter 200
mem_total 128000
n_frozen_core {1}
$end

{2}

@@@@@@
$molecule
read
$end

$rem
jobtype sp
exchange wB97M(2)
xc_grid 000099000590
basis {3}
max_scf_cycles 200
thresh 14
scf_convergence 8
scf_algorithm gdm
symmetry false
sym_ignore true
unrestricted false
gen_scfman false
mem_total 128000
cc_memory 96000
cc_backend xm
mem_static 1500
n_frozen_core {4}
scf_guess read
$end

{5}
'''.format(basis, f_c, basis_real, basis, f_c, basis_real)

    if args.basis == 'aug-cc-pcV5Z' and args.method != 'XYG3' and args.method != 'XYGJOS' and args.method != 'wB97M(2)':
        input = input + '''
@@@@@@
$molecule
read
$end

$rem

jobtype sp
method HF
xc_grid 000099000590
basis {0}
max_scf_cycles 0
scf_guess read
thresh 14
scf_convergence 8
mem_total 128000
cc_memory 96000
cc_backend xm
mem_static 1500
symmetry false
sym_ignore true
scf_guess read
unrestricted false
scf_algorithm gdm
n_frozen_core 0
$end

{1}
    '''.format(basis, basis_real)
## if (B3LYP ==STABLE)
##business as usual for "exchange XYG3/XYGJOS"
##else
##job 0-> method b3lyp, gen_scfman true; stability
##job 1->exchange xyg3; field XX 0.001
##job 2->exchange xyg3; field XX -0.001

    if args.multipole_field is not None:
        multipole_field = args.multipole_field[0].split()
        if args.method != 'wB97M(2)':
            for c, i in enumerate(multipole_field):
                input += '''
@@@@@@
$molecule
read
$end

$rem
jobtype sp
exchange {0}
xc_grid 000099000590
basis {1}
{2}
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
unrestricted false
scf_algorithm gdm
n_frozen_core {3}
$end

{4}

$multipole_field
{5} {6}
$end

        '''.format(args.method, basis, aux_basis, f_c, basis_real, i, args.strength[c])
        else:
            for c, i in enumerate(multipole_field):
                input += '''
@@@@@@
$molecule
read
$end

$rem

jobtype sp
method wb97m-v
xc_grid 000099000590
basis {0}
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
unrestricted false
scf_algorithm gdm
n_frozen_core {1}
gen_scfman true
$end

$multipole_field
{2} {3}
$end

{4}

@@@@@@
$molecule
read
$end

$rem

jobtype sp
exchange wb97m(2)
xc_grid 000099000590
basis {5}
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
unrestricted false
scf_algorithm gdm
n_frozen_core {6}
$end

$multipole_field
{7} {8}
$end

{9}
'''.format(basis, f_c, i, args.strength[c], basis_real, basis, f_c, i, args.strength[c], basis_real)
    write(input)
    sys.exit()
