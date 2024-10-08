#!/bin/bash
git checkout dev
git pull
git checkout main
git merge dev
git add .
git commit -m "update from dev push"
git push
make
