import argparse
import json
import re
from datetime import datetime

from src.db.mysql_connector import MySQLConnector
from src.entities.pokemon import Pokemon
from src.utils.ps_game_state_util import get_player_pkm_list, initiate_game_state, game_state_to_file, ini_data_file
from src.utils.ps_utils import get_cleaned_battle_log, read_config
from src.utils.udf_utils import open_mysql_connection


def set_boost(pkm: Pokemon, stat: str, value: int):
    if stat == 'atk':
        pkm.atk_boost += value
    elif stat == 'def':
        pkm.def_boost += value
    elif stat == 'spa':
        pkm.spa_boost += value
    elif stat == 'spd':
        pkm.spd_boost += value
    else:
        pkm.spe_boost += value


def set_unboost(pkm: Pokemon, stat: str, value: int):
    if stat == 'atk':
        pkm.atk_boost -= value
    elif stat == 'def':
        pkm.def_boost -= value
    elif stat == 'spa':
        pkm.spa_boost -= value
    elif stat == 'spd':
        pkm.spd_boost -= value
    else:
        pkm.spe_boost -= value


def get_pkm(pkm_code: str, pkms: list[Pokemon]):
    for pkm in pkms:
        if pkm.pkm_code == pkm_code:
            return pkm
    print(f"Can't get pkm: {pkm_code}")



def get_pkm_row_detail(row: str, battling_pkm: dict[str]):
    r_detail = (row.replace('p1a', 'p1').replace('p1b', 'p1')
                .replace('p2a', 'p2').replace('p2b', 'p2').lower())
    player = r_detail.split(': ')[0].split('|')[-1]
    print(r_detail)
    print(battling_pkm)
    pkm_nickname = re.sub(r'[^A-Za-z0-9 ]+', '', r_detail.split(': ')[1].split('|')[0]).replace(' ', '')
    pkm_code = battling_pkm[f"{player}_{pkm_nickname}"]
    return player, pkm_code


def get_side_row_detail(row: str):
    player = row.split(':')[0].split('|')[-1]
    effect = row.split('|')[-1].split(':')[-1].replace(' ', '')
    return player, effect


def write_game_state(mysql_conn: MySQLConnector, output_path: str, battle_log: tuple):
    # get battling pokemon dict
    battling_pkm = battle_log[0]

    # get the winner (1 = p1 wins, 0 = p2 wins)
    p1 = battle_log[1][0]
    p1_win = True if battle_log[1][-1].replace('|win|', '') in p1 else False

    # sublist the actual log
    turn_details = battle_log[1][2:-1]

    # player_pokemon_list
    player_pkm_list = get_player_pkm_list(turn_details[:15])
    log_offset = 2 + len(player_pkm_list[0]) + len(player_pkm_list[1])

    # skip if either player does not have full team
    if len(player_pkm_list[0]) < 6 or len(player_pkm_list[1]) < 6:
        return

    turn_details = turn_details[log_offset:]
    print(turn_details)

    game_state = initiate_game_state(mysql_conn, p1_win, player_pkm_list)
    game_state_to_file(output_path, game_state)

    start = False
    for row in turn_details:
        # skip pre-turns
        if row == '|turn|1':
            start = True
            continue
        if not start:
            continue

        # write game state to file
        if '|turn|' in row:
            game_state_to_file(output_path, game_state)

        # damage cal
        if '|-damage|' in row:
            player, pkm_code = get_pkm_row_detail(row, battling_pkm)
            if '/' in row.split('|')[-1]:
                hp = row.split('|')[-1].split('/')[0]
            elif '/' in row.split('|')[-2]:
                hp = row.split('|')[-2].split('/')[0]
            else:
                hp = row.split('|')[-3].split('/')[0]

            if player == 'p1':
                p1_pkm = get_pkm(pkm_code, game_state.p1state.pkms)
                if '|0 fnt' in row:
                    p1_pkm.hp = 0
                else:
                    p1_pkm.hp = hp
            else:
                p2_pkm = get_pkm(pkm_code, game_state.p2state.pkms)
                if '|0 fnt' in row:
                    p2_pkm.hp = 0
                else:
                    p2_pkm.hp = hp

        # volatile starts
        if '|-start|' in row:
            player, pkm_code = get_pkm_row_detail(row, battling_pkm)

            if player == 'p1':
                p1_pkm = get_pkm(pkm_code, game_state.p1state.pkms)
                p1_pkm.volatile_status = True
            else:
                p2_pkm = get_pkm(pkm_code, game_state.p2state.pkms)
                p2_pkm.volatile_status = True

            # volatile ends
            if '|-end|' in row:
                player, pkm_code = get_pkm_row_detail(row, battling_pkm)

                if player == 'p1':
                    p1_pkm = get_pkm(pkm_code, game_state.p1state.pkms)
                    p1_pkm.volatile_status = False
                else:
                    p2_pkm = get_pkm(pkm_code, game_state.p2state.pkms)
                    p2_pkm.volatile_status = False

        # heal
        if '|-heal|' in row:
            player, pkm_code = get_pkm_row_detail(row, battling_pkm)
            if '/' in row.split('|')[-1]:
                hp = row.split('|')[-1].split('/')[0]
            elif '/' in row.split('|')[-2]:
                hp = row.split('|')[-2].split('/')[0]
            else:
                hp = row.split('|')[-3].split('/')[0]

            if player == 'p1':
                p1_pkm = get_pkm(pkm_code, game_state.p1state.pkms)
                p1_pkm.hp = hp
            else:
                p2_pkm = get_pkm(pkm_code, game_state.p2state.pkms)
                p2_pkm.hp = hp

        # boost
        if '|-boost|' in row:
            player, pkm_code = get_pkm_row_detail(row, battling_pkm)
            if '[from]' in row.split('|')[-1]:
                boost_stat = row.split('|')[-3]
                boost_value = int(row.split('|')[-2])
            else:
                boost_stat = row.split('|')[-2]
                boost_value = int(row.split('|')[-1])
            if player == 'p1':
                p1_pkm = get_pkm(pkm_code, game_state.p1state.pkms)
                set_boost(p1_pkm, boost_stat, boost_value)
            else:
                p2_pkm = get_pkm(pkm_code, game_state.p2state.pkms)
                set_boost(p2_pkm, boost_stat, boost_value)

        # unboost
        if '|-unboost|' in row:
            player, pkm_code = get_pkm_row_detail(row, battling_pkm)
            if '[from]' in row.split('|')[-1]:
                unboost_stat = row.split('|')[-3]
                unboost_value = int(row.split('|')[-2])
            else:
                unboost_stat = row.split('|')[-2]
                unboost_value = int(row.split('|')[-1])
            if player == 'p1':
                p1_pkm = get_pkm(pkm_code, game_state.p1state.pkms)
                set_unboost(p1_pkm, unboost_stat, unboost_value)
            else:
                p2_pkm = get_pkm(pkm_code, game_state.p2state.pkms)
                set_unboost(p2_pkm, unboost_stat, unboost_value)

        # side status starts
        if '|-sidestart|' in row:
            player, effect = get_side_row_detail(row)
            if player == 'p1':
                if effect == 'tailwind':
                    game_state.p1state.tailwind = True
                elif effect == 'lightscreen':
                    game_state.p1state.light_screen = True
                elif effect == 'reflect':
                    game_state.p1state.reflect = True
                elif effect == 'stickyweb':
                    game_state.p1state.webbed = True
                else:
                    pass
            else:
                if effect == 'tailwind':
                    game_state.p2state.tailwind = True
                elif effect == 'lightscreen':
                    game_state.p2state.light_screen = True
                elif effect == 'reflect':
                    game_state.p2state.reflect = True
                elif effect == 'stickyweb':
                    game_state.p2state.webbed = True
                else:
                    pass

            # side status ends
            if '|-sideend|' in row:
                player, effect = get_side_row_detail(row)
                if player == 'p1':
                    if effect == 'tailwind':
                        game_state.p1state.tailwind = False
                    elif effect == 'lightscreen':
                        game_state.p1state.light_screen = False
                    elif effect == 'reflect':
                        game_state.p1state.reflect = False
                    elif effect == 'stickyweb':
                        game_state.p1state.webbed = False
                    else:
                        pass
                else:
                    if effect == 'tailwind':
                        game_state.p2state.tailwind = False
                    elif effect == 'lightscreen':
                        game_state.p2state.light_screen = False
                    elif effect == 'reflect':
                        game_state.p2state.reflect = False
                    elif effect == 'stickyweb':
                        game_state.p2state.webbed = False
                    else:
                        pass

    # write last game state
    game_state_to_file(output_path, game_state)


def main():
    parser = argparse.ArgumentParser(
        prog='PokemonShowdownMLGameStateData',
        description='This program prepare the game state data for training')
    parser.add_argument('-p', '--prog_path')
    parser.add_argument('-f', '--file_path')
    parser.add_argument('-o', '--output_path')
    args = parser.parse_args()

    file_path = args.file_path
    prog_path = args.prog_path
    start_time = datetime.now()
    output_path = f"{prog_path}/model_data/game_state/{start_time.strftime('%Y%m%d')}_game_state.csv"

    # read configs
    configs = read_config(f'{prog_path}/conf/mysql_conf.json')

    # open mysql connection
    mysql_conn = open_mysql_connection(configs)

    # load the replay detail files
    with open(file_path, 'r') as file:
        data = json.load(file)

    # create the output data file
    ini_data_file(output_path)

    for log in data:
        print(f"Processing battle log: {log['id']}")
        if '|start' not in log['log']:
            continue
        battle_log = get_cleaned_battle_log(log['log'])
        write_game_state(mysql_conn, output_path, battle_log)

    end_time = datetime.now()
    print(f"Process finishes. Time taken: {end_time - start_time}")


if __name__ == '__main__':
    main()
