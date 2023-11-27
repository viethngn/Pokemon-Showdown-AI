#!/bin/sh

# exit when any command fails
set -e

# get argument if exist. else default as not running new collect_ps_battle_data.sh
if [ ! -z "$1" ] && [ "$1" = "collector" ]
  then
    echo "Collecting new battle data: [ON]"
    collector=true
  else
    echo "Collecting new battle data: [OFF]"
    collector=false
fi

# get the program dir
prog_dir=$(pwd)

# remove old logs
rm -f log/*.log

sh "${prog_dir}"/exec/prepare_directories.sh

echo "Start preparing MySQL database pokemon_showdown"
SECONDS=0
sh "${prog_dir}"/exec/prepare_mysql_db.sh 2>&1 | tee -a log/prepare_mysql_db.log >/dev/null
elapsed=$SECONDS
echo "Finished preparing MySQL database pokemon_showdown. Time taken: $(($elapsed / 60))m$(($elapsed % 60))s"

echo "Start loading static data"
SECONDS=0
sh "${prog_dir}"/exec/load_static_data.sh 2>&1 | tee -a log/load_static_data.log >/dev/null
elapsed=$SECONDS
echo "Finished loading static data. Time taken: $(($elapsed / 60))m$(($elapsed % 60))s"

if [ $collector = true ]
then
  echo "Start collecting battle data from APIs"
  SECONDS=0
  sh collect_ps_battle_data.sh >/dev/null
  elapsed=$SECONDS
  echo "Finished collecting battle data from APIs. Time taken: $(($elapsed / 60))m$(($elapsed % 60))s"
fi

echo "Start loading battle data"
SECONDS=0
sh "${prog_dir}"/exec/load_ps_battle_data.sh 2>&1 | tee -a log/load_ps_battle_data.log >/dev/null
elapsed=$SECONDS
echo "Finished loading battle data. Time taken: $(($elapsed / 60))m$(($elapsed % 60))s"

echo "Start preparing MySQL data delivery layer"
SECONDS=0
sh "${prog_dir}"/exec/prepare_data_delivery_layer.sh 2>&1 | tee -a log/prepare_data_delivery_layer.log | grep -v "mysql*" | grep -v "Querying*"
elapsed=$SECONDS
echo "Finished preparing MySQL data delivery layer. Time taken: $(($elapsed / 60))m$(($elapsed % 60))s"
