#!/bin/sh

# exit when any command fails
set -e

mkdir -p replays
mkdir -p replays/static_data
mkdir -p sql_output
mkdir -p sql_output/tb_ps_players
mkdir -p sql_output/tb_ps_replay_details
mkdir -p sql_output/tb_ps_replays
mkdir -p log