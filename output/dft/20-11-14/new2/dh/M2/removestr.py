import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

with open(args.file, 'r') as file:
    f = file.read()

toremove = re.findall('(Total QAlloc)([\s\S]*?)(2 of 14)', f)[0][1]
f = f.replace(toremove, '')

for i in [3, 5, 7, 9, 11, 13]:
    toremove = re.findall('({0} of 14)([\s\S]*?)({1} of 14)'.format(i, i+1), f)[0][1]
    f = f.replace(toremove, '')

with open(args.file, 'w') as file:
    file.write(f)
