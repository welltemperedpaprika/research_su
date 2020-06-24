import glob, os, re, pandas
from pymatgen.core.periodic_table import Element

output = {'X':[], 'Y':[], 'Z':[], 'XX':[], 'YY':[], 'ZZ':[], 'tot_e':[]}
for f in glob.glob('*.inp'):
    with open(f, 'r') as myfile:
        s = myfile.read()
    info = re.search('molecule\s*\d\s\d\s([\s\S]*?)\$end', s).group(1)
    x = y = z = xx = yy = zz = tote = 0
    for l in info.splitlines():
        line = l.split()
        charge = Element(line[0][0]).Z
        tote += Element(line[0][0]).Z
        x += charge * float(line[1])
        y += charge * float(line[2])
        z += charge * float(line[3])
        xx += charge * float(line[1]) ** 2
        yy += charge * float(line[2]) ** 2
        zz += charge * float(line[3]) ** 2
    output['X'].append(x)
    output['Y'].append(y)
    output['Z'].append(z)
    output['XX'].append(xx)
    output['YY'].append(yy)
    output['ZZ'].append(zz)
    output['tot_e'].append(tote)

df = pandas.DataFrame.from_dict(output)
df.to_csv('data.csv')
