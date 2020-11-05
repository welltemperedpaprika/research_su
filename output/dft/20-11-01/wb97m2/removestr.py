import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

with open(args.file, 'r') as file:
    f = file.read()

toremove = re.findall('(Total QAlloc)([\s\S]*?)(2 of 8)', f)[0][1]
f = f.replace(toremove, '')

with open(args.file, 'w') as file:
    file.write(f)
