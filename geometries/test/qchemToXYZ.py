import glob, os, re, pandas
from pymatgen.core.periodic_table import Element

output = {'X':[], 'Y':[], 'Z':[], 'XX':[], 'YY':[], 'ZZ':[]}
for f in glob.glob('*.inp'):
    with open(f, 'r') as myfile:
        s = myfile.read()
    info = re.search('molecule\s*\d\s\d\s([\s\S]*?)\$end', s).group(1)
    x, y, z, xx, yy, zz = 0
    for l in info.splitlines():
        line = l.split()
        charge = Element(line[0][0]).Z
        x += charge * line[1]
        y += charge * line[2]
        z += charge * line[3]
        xx += charge * line[1] ** 2
        yy += charge * line[2] ** 2
        zz += charge * line[3] ** 2
    output['X'].append(x)
    output['Y'].append(y)
    output['Z'].append(z)
    output['XX'].append(xx)
    output['YY'].append(yy)
    output['ZZ'].append(zz)

df = pandas.DataFrame.from_dict(output)
df.to_csv('data.csv')
