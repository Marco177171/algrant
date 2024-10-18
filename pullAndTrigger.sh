#!/bin/bash
git add .
git commit -m update
git push
git checkout dev
git pull
git checkout main
git merge dev
make
