#!/bin/bash

for f in *.out
do
  echo -e "$f \n==========\n" >> output.txt
  grep -n "Total energy" "$f" >> output.txt
  echo -e "\n==========\n" >> output.txt
  grep -n -A2 "Quadrupole" "$f" >> output.txt
  echo -e "\n------------\n" >> output.txt
done
echo "Finished."
