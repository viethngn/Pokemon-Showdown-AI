#!/bin/sh

# exit when any command fails
set -e

# get the program dir
prog_dir=$(pwd)

echo "Start collecting Pokemon Showdown battle data from API"

# collect battle data for this run
python ps_battle_data_collector.py -p "$prog_dir"

echo "Finished collecting Pokemon Showdown battle data from API"