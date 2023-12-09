#!/bin/sh

# exit when any command fails
set -e

# get the program dir
prog_dir=$(pwd)

echo "Start building game state data from battle logs"

# collect battle data for this run
python ps_build_game_state_data.py -p "$prog_dir" 2>&1 | tee -a log/build_game_state_data.log >/dev/null

echo "Finished building game state data from battle logs"