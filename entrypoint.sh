#!/bin/sh
ECHO "CONDA INITIALIZATION!!!"
set -e
conda clean --all --yes
conda env remove --name fastcasso
conda env create -f environment.yml
./activate.sh
