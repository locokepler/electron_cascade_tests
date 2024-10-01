#!/bin/zsh

# This script should be able to take a brand new copy of this from GitHub and run
# a basic electron cascade demo. It makes its own starting electron.

# make an example LMCP like structure using the included python code
python3 millichannel_slab.py > demo_LMCP.topas

./externally_generated_secondary_iterate.sh demo_electron.phsp demo_backplane.phsp

python3 backplane_plots.py