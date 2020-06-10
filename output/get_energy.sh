#!/bin/bash

function get_e {
  #$1 is the file name
  name=$1
  q="$(grep -E "Total energy" ${name} | grep -E -o "\-?[0-9][0-9.]*" | xargs | sed 's/ /, /g')"
  echo "$q"
}

filename="totalenergies.txt"
suffix='p.out'
> "$filename"
for f in *.out
do
  q=$(get_e $f)
  name=$(echo $f | sed -e "s/$suffix$//")
  echo "${name}, ${q}" >> "$filename"
done
