#!/bin/bash

echo -e "\033[0;32mSaving updates to GitHub...\033[0m"

git add .
git commit -m "save `date`"
git push origin HEAD
