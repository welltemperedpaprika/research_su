import argparse
from pathlib import Path
import re
import json

parser = argparse.ArgumentParser(description='Utility functions to modify output json object')
parser.add_argument('-f', '--filename')
parser.add_argument('-a', '--add', nargs='+', help='Adds key, value pair to json')
parser.add_argument('-m', '--modify', nargs='+', help='Modifies old key to new value.')
parser.add_argument('-d', '--delete', nargs='+', help='Deletes the file.')
parser.add_argument('-p', '--pop', nargs='+', help='Pops the key.')
parser.add_argument('-c', '--clear', help='Clears the json object.')
args = parser.parse_args()
if args.filename:
    molecule_name = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(1)
    method = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(2)
    basis = re.search(r'([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)', args.filename).group(3)
output_path = Path.home() / "summer/research/output"
with open(output_path/"output.json") as f:
    data = json.load(f)



def delete(molecule, method, basis):
    for c, d in enumerate(data[molecule]):
        if d['method'] == method and d['basis'] == basis:
            data[molecule].pop(c)
    return

def pop(molecule, method, basis, key):
    for d in data[molecule]:
        if d['method'] == method and d['basis'] == basis:
            d.pop(key, None)
    return

def modify(molecule, method, basis, old, new):
    for d in data[molecule]:
        if d['method'] == method and d['basis'] == basis:
            d[old] = new
    return

def add(molecule, method, basis, key, value):
    for d in data[molecule]:
        if d['method'] == method and d['basis'] == basis:
            d[key] = value
    return

def clear():
    data.clear()

if args.add:
    add(molecule_name, method, basis, args.a[0], args.a[1])
if args.modify:
    modify(molecule, method, basis, args.m[0])
if args.pop:
    pop(molecule, method, basis, args.p[0])
if args.delete:
    delete(molecule, method, basis)
if args.clear:
    clear()

with open(output_path/"output.json", 'w') as outfile:
    json.dump(data, outfile)
