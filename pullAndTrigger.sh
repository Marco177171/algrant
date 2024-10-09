#!/bin/bash
git checkout dev
git pull
git checkout main
git merge dev
make
