#!/bin/sh

# exit when any command fails
set -e

# get the program dir
prog_dir=$(pwd)

echo "Start loading Pokemon Showdown static data from API"

# load static data to mysql
python ps_load_static_data.py -p "${prog_dir}" -o mysql

echo "Fnished loading Pokemon Showdown static data from API"
