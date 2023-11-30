import argparse
import json
from datetime import datetime

from src.utils.ps_utils import get_cleaned_battle_log


def write_game_state(output_path: str, battle_id: str, battle_log: tuple):
    pass


def main():
    parser = argparse.ArgumentParser(
        prog='PokemonShowdownMLGameStateData',
        description='This program prepare the game state data for training')
    parser.add_argument('-f', '--file_path')
    parser.add_argument('-o', '--output_path')
    args = parser.parse_args()

    file_path = args.file_path
    output_path = args.output_path
    start_time = datetime.now()

    # load the replay detail files
    with open(file_path, 'r') as file:
        data = json.load(file)

    for log in data:
        battle_log = get_cleaned_battle_log(log)
        write_game_state(output_path, log['id'], battle_log)

    end_time = datetime.now()
    print(f"Process finishes. Time taken: {end_time - start_time}")


if __name__ == '__main__':
    main()