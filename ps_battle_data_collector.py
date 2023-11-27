import argparse
import json
import os
from datetime import datetime

from src.recovery.ps_recovery import remove_invalid_char_for_url
from src.utils.ps_utils import get_ps_replays, save_to_files, get_replay_details, get_player_details


def main():
    parser = argparse.ArgumentParser(
        prog='PokemonShowdownDataCollector',
        description='This program collect the live battle data from pokemonshowdown.com')
    parser.add_argument('-p', '--program_path')
    args = parser.parse_args()

    # src parent path
    prog_path = args.program_path
    start_time = datetime.now()

    replays = get_ps_replays()
    if replays is not None and len(replays) != 0:
        json_formatted_data = json.dumps(replays, indent=4)
        print(json_formatted_data)
    else:
        return

    # save replays to text
    os.makedirs(f"{prog_path}/replays/{start_time.strftime('%Y%m%d')}", exist_ok=True)
    save_to_files(
        f"{prog_path}/replays/{start_time.strftime('%Y%m%d')}/{start_time.strftime('%Y%m%d_%H')}_replay_save.json",
        'json',
        replays)
    save_to_files(
        f"{prog_path}/replays/{start_time.strftime('%Y%m%d')}/{start_time.strftime('%Y%m%d_%H')}_replay_save.csv",
        'csv',
        replays)

    # get replay details:
    r_details = get_replay_details(replays)

    # save replay details to file
    save_to_files(
        f"{prog_path}/replays/{start_time.strftime('%Y%m%d')}/{start_time.strftime('%Y%m%d_%H')}_replay_details.json",
        'json',
        r_details)

    # get player_details for this run
    player_ids = set()
    for replay in replays:
        player_ids.add(remove_invalid_char_for_url(replay['p1']))
        player_ids.add(remove_invalid_char_for_url(replay['p2']))
    player_details = get_player_details(player_ids)

    # save player details to file
    save_to_files(
        f"{prog_path}/replays/{start_time.strftime('%Y%m%d')}/{start_time.strftime('%Y%m%d_%H')}_player_details.json",
        'json',
        player_details)

    end_time = datetime.now()
    print(f"Process finishes. Time taken: {end_time - start_time}")


if __name__ == '__main__':
    main()
