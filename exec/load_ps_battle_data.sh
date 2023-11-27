#!/bin/sh

# exit when any command fails
set -e

# get argument if exist. else default as "mysql"
if [ -z "$1" ] || [ "$1" = "mysql" ]
then
  output_type="mysql"
else
  output_type="sql"
fi

# get the program dir
prog_dir=$(pwd)

echo "Start loading Pokemon Showdown battle data"

# load player details data
player_detail_files=$(find replays -type f -name '*_player_details.json')
for f in $player_detail_files
do
  echo "Start processing player details file ${prog_dir}/$f"
  python ps_load_battle_data.py -f ${prog_dir}/$f -d ps_player -o "${output_type}"
done

# load replay saves data
save_files=$(find replays -type f -name '*_replay_save.json')
for f in $save_files
do
  echo "Start processing replay saves file ${prog_dir}/$f"
  python ps_load_battle_data.py -f ${prog_dir}/$f -d ps_replay -o "${output_type}"
done

# load replay details data
replay_detail_files=$(find replays -type f -name '*_replay_details.json')
for f in $replay_detail_files
do
  echo "Start processing replay details file ${prog_dir}/$f"
  python ps_load_battle_data.py -f ${prog_dir}/$f -d ps_replay_detail -o "${output_type}"
done

echo "Finished loading Pokemon Showdown battle data"
