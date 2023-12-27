#!/bin/sh

# exit when any command fails
set -e

# get the program dir
prog_dir=$(pwd)

# remove old logs
rm -f log/collect_ps_battle_data.log
rm -f log/ps_build_game_state_data.log
rm -f log/ps_seq_training_model.log


# get cur_date
cur_date=$(date '+%Y%m%d')
yester_date=$(date -v '-1d' '+%Y%m%d')

echo "Start collecting battle data from APIs"
SECONDS=0
sh "${prog_dir}"/exec/collect_ps_battle_data.sh 2>&1 | tee -a log/collect_ps_battle_data.log >/dev/null
elapsed=$SECONDS
echo "Finished collecting battle data from APIs. Time taken: $(($elapsed / 60))m$(($elapsed % 60))s"

echo "Start converting battle data to game state data"
SECONDS=0
replay_detail_files=$(find replays -type f -name "$cur_date*_replay_details.json")
for f in $replay_detail_files
do
  echo "Start processing replay details file ${prog_dir}/$f"
  python "${prog_dir}"/ps_build_game_state_data.py -p "${prog_dir}" -f "$f" 2>&1 | tee -a log/ps_build_game_state_data.log >/dev/null
done
elapsed=$SECONDS
echo "Finished converting battle data to game state data. Time taken: $(($elapsed / 60))m$(($elapsed % 60))s"

echo "Start training model"
SECONDS=0
python "${prog_dir}"/ml_model/seq_model/ps_seq_training_data.py -p ${prog_dir} -f "${prog_dir}/ml_model/game_state/${cur_date}_game_state.csv" 2>&1 | tee -a log/ps_seq_training_model.log >/dev/null
python "${prog_dir}"/ml_model/seq_model/ps_seq_training_model.py --retrain_model "${prog_dir}/ml_model/seq_model/${cur_date}" --sm_model_dir "${prog_dir}/ml_model/seq_model" --train "${prog_dir}/ml_model/seq_model" --epochs 150 --batch_size 32 2>&1 | tee -a log/ps_seq_training_model.log >/dev/null
elapsed=$SECONDS
echo "Finished training model. Time taken: $(($elapsed / 60))m$(($elapsed % 60))s"
