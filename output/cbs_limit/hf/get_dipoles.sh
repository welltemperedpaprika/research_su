#!/bin/bash

#returns the dipole moment in X Y Z directions of all molecules for the
#given method type in a text file.

function get_d {
  #$1 is the file name
  name=$1
  q="$(grep -E -A2 -m 1 "Dipole" ${name} | grep -E -o "\-?[0-9][0-9.]*" | xargs | sed 's/ /, /g')"
  echo "$q"
}

filename="dipoles.txt"
suffix='p.out'
> "$filename"
for f in *.out
do
  q=$(get_d $f)
  name=$(echo $f | sed -e "s/$suffix$//")
  echo "${name}, ${q}" >> "$filename"
done
