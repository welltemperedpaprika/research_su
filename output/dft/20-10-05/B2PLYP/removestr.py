import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

with open(args.file, 'r') as file:
    f = file.read()

toremove = re.findall('(2 of 8)([\s\S]*?)(3 of 8)', f)[0][1]
f = f.replace(toremove, '')

with open(args.file, 'w') as file:
    file.write(f)
    
