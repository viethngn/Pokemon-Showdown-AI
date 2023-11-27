import argparse
import json
from datetime import datetime

from src.utils.ps_utils import get_player_details, save_to_files


def remove_invalid_char_for_url(text):
    return text.replace(' ', '_').replace('?', '').replace('#', '')


def recover_player_details_from_replay_file(filename):
    with open(filename, 'r') as file:
        replays = json.loads(''.join(file.readlines()))

    player_ids = set()
    for replay in replays:
        player_ids.add(remove_invalid_char_for_url(replay['p1']))
        player_ids.add(remove_invalid_char_for_url(replay['p2']))
    player_details = get_player_details(player_ids)

    # save player details to file
    output_dir = '/'.join(filename.split('/')[:-1])
    save_to_files(
        f"{output_dir}/{datetime.now().strftime('%Y%m%d_%H')}_player_details.json",
        'json',
        player_details)


def main():
    parser = argparse.ArgumentParser(
        prog='PokemonShowdownDataRecovery',
        description='This program recover battle data from pokemonshowdown.com with input from a save file')
    parser.add_argument('-f', '--filename')
    args = parser.parse_args()

    filename = args.filename
    start_time = datetime.now()

    # recover player details
    recover_player_details_from_replay_file(filename)

    end_time = datetime.now()
    print(f"Process finishes. Time taken: {end_time - start_time}")


if __name__ == '__main__':
    main()
