#!/bin/bash
#ggrep for mac, grep for windows
function get_q {
  name=$1
  q="$(grep -E -A2 -m 1 "Quadrupole" ${name} | grep -E -o "\-?[0-9][0-9.]*" | xargs | sed 's/ /, /g')"
  echo "$q"
}

filename="quadrupoles.txt"
suffix='p.out'
> "$filename"
for f in *.out
do
  q=$(get_q $f)
  name=$(echo $f | sed -e "s/$suffix$//")
  echo "${name}, ${q}" >> "$filename"
done
