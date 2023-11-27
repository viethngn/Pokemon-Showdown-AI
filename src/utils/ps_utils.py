import csv
import json
from random import uniform
from time import sleep

import requests

import src.const.ps_constants as const
from src.cache.ps_static_data import PSStaticData
from src.utils.ps_parser import type_chart_parser, abilities_parser, movedex_parser, items_parser, \
    pokedex_parser, learn_sets_parser
from src.utils.udf_utils import fix_response_text


def load_static_data():
    return PSStaticData(get_type_chart(), get_abilities(), get_movedex(), get_items(), get_pokedex(), get_learn_sets())


def read_config(filename):
    print(f"Reading config file at {filename}")

    with open(filename, 'r') as file:
        configs = json.load(file)
    return configs


def get_ps_replays():
    replays = []

    # set page limit to call 25 pages in the paginated API
    for page in range(1, 26):
        print(f"Calling get replay API for page {page}")

        try:
            # response = requests.get(
            #     f'https://replay.pokemonshowdown.com/search.json?format=gen9doublesou&page={page}')
            response = requests.get(
                f'https://replay.pokemonshowdown.com/api/replays/search?username=&format=gen9doublesou&page={page}')
        except requests.exceptions.RequestException as e:
            print(f"""There is an error calling the get_ps_replays api at page {page}
            Error message: {e}""")
            break

        if response is not None:
            data = json.loads(response.text[1:])
            replays.extend(data)
        else:
            print(f"""There is an error calling the get_ps_replays api at page {page}
            No response received.""")
            break

        # ps has a limitation of 51 per page in the response
        # if there is less than 51 items then this is the last page
        if len(data) < 51:
            break

        # sleep randomly for at most 0.5 seconds
        sleep(uniform(0, 0.5))

    return replays


def get_replay_details(replays):
    replay_details = []

    for r in replays:
        print(f"Calling get replay detail API [Game-id: {r['id']}]")

        try:
            response = requests.get(f"https://replay.pokemonshowdown.com/{r['id']}.json")
        except requests.exceptions.RequestException as e:
            print(f"""There is s an error calling the get_replay_details api
            Error message: {e}""")
            break

        if response is not None:
            data = json.loads(response.text)
            replay_details.append(data)
        else:
            print(f"""There is an error calling the get_replay_details api
            No response received.""")
            break

        sleep(uniform(0, 0.3))

    return replay_details


def get_pokedex():
    response = get_ps_url_response(f"https://play.pokemonshowdown.com/data/pokedex.js")
    for k, v in response.items():
        # correct < 1 num (id)
        if v['num'] < 1:
            v['num'] += 10000
        if 'forme' in v.keys():
            v['num'] = f"{v['num']}-{v['forme']}"
    return response


def get_learn_sets():
    """
    In the learn sets, the code letters for how to learn a move are as following:
    L = Level up
    T = Move tutor
    M = TM/HM
    S = Event only
    V = Virtual console from Gen 1
    E = Egg move

    Code format: 8L25 -> Gen 8, learn at level 25

    :return:
    """
    return get_ps_url_response(f"https://play.pokemonshowdown.com/data/learnsets.js")


def get_type_chart():
    """
    Type chart explained:
    - Each key is the typing at defensive position
    - Values are types at attacking position

    Code explained:
    0 = x1 effective
    1 = x2 effective
    2 = x1/2 effective
    3 = Immune (x0 effective)

    :return:
    """
    return get_ps_url_response(f"https://play.pokemonshowdown.com/data/typechart.js")


def get_movedex():
    """
    Move category:
    0 = status
    1 = physical
    2 = special

    :return:
    """
    response = get_ps_url_response(f"https://play.pokemonshowdown.com/data/moves.js")
    for k, v in response.items():
        # correct < 1 num (id)
        if v['num'] < 1:
            v['num'] += 10000
        # correct names containing comma
        v['name'] = v['name'].replace(',', '_')
        # correct accuracy to all int (True -> 999)
        if v['accuracy'] is True:
            v['accuracy'] = 999
    return response


def get_items():
    response = get_ps_url_response(f"https://play.pokemonshowdown.com/data/items.js")
    for k, v in response.items():
        # correct < 1 num (id)
        if v['num'] < 1:
            v['num'] += 10000
    return response


def get_abilities():
    response = get_ps_url_response(f"https://play.pokemonshowdown.com/data/abilities.js")
    for k, v in response.items():
        # correct < 1 num (id)
        if v['num'] < 1:
            v['num'] += 10000
        # correct a duplicate key
        if v['num'] == 284:
            v['num'] = f"{v['num']}-{v['name'].split()[0].lower()}"
    return response


def get_ps_url_response(url):
    print(f"Calling get API: [{url}]")

    response = None

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"""There is s an error calling the url {url}
                    Error message: {e}""")

    if response is not None:
        # need to fix the json here since the response is not JSON corrected
        corrected_json = fix_response_text(response.text)

        response_json = json.loads(corrected_json)
        return response_json
    else:
        print(f"""There is an error calling the url {url}
                    No response received.""")
        return None


def get_player_details(player_ids):
    player_details = {}
    for p_id in player_ids:
        response = get_ps_url_response(f"https://pokemonshowdown.com/users/{p_id}.json")
        player_details[p_id] = response
        # sleep randomly for at most 0.5 seconds
        sleep(uniform(0, 0.5))

    return player_details


def save_to_files(filepath, mode, data, static=None, cache=None):
    """
    Save json data to file (json/csv)
    :param filepath: (str) filepath
    :param mode: (str) 'json' or 'csv'
    :param data: (dict/list) json object/sql string list
    :param static: (str) optional - whether the data is the static data that required parsing
    :param cache: (PSStaticData) optional - provide if need to access the in memory static data cache
    :return: None
    """
    print(f"Writing {mode} data to file {filepath}")

    if mode == const.JSON:
        json_formatted_data = json.dumps(data, indent=4)

        with open(filepath, 'w') as replay_file:
            replay_file.write(json_formatted_data)

    if mode == const.CSV:
        if static is None:
            data_file = open(filepath, 'w', newline='')
            csv_writer = csv.writer(data_file)

            count = 0
            for item in data:
                if count == 0:
                    header = item.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(item.values())

            data_file.close()

        else:
            csv_text_list = None

            if static == const.TC:
                csv_text_list = type_chart_parser(data)
            if static == const.AB:
                csv_text_list = abilities_parser(data)
            if static == const.MVD:
                csv_text_list = movedex_parser(data)
            if static == const.ITM:
                csv_text_list = items_parser(data)
            if static == const.PKD:
                csv_text_list = pokedex_parser(data, cache)
            if static == const.LS:
                csv_text_list = learn_sets_parser(data, cache)

            # writing parsed data to csv file
            with open(filepath, 'w') as file:
                for line in csv_text_list:
                    file.write(f'{line}\n')

    if mode == const.SQL:
        if static is None:
            # writing parsed data to sql file
            with open(filepath, 'w') as file:
                for line in data:
                    file.write(f'{line}\n')
        else:
            sql_text_list = None

            if static == const.TC:
                sql_text_list = type_chart_parser(data, const.SQL)
            if static == const.AB:
                sql_text_list = abilities_parser(data, const.SQL)
            if static == const.MVD:
                sql_text_list = movedex_parser(data, const.SQL)
            if static == const.ITM:
                sql_text_list = items_parser(data, const.SQL)
            if static == const.PKD:
                sql_text_list = pokedex_parser(data, cache, const.SQL)
            if static == const.LS:
                sql_text_list = learn_sets_parser(data, cache, const.SQL)

            # writing parsed data to sql file
            with open(filepath, 'w') as file:
                for line in sql_text_list:
                    file.write(f'{line}\n')
