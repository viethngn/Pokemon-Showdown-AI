import json
import re

import src.const.ps_constants as const
from src.const.ps_pkm_special import SPECIAL_FORMS
from src.db.mysql_connector import MySQLConnector


def type_effectiveness_converter(eff_code):
    if eff_code == const.NORMAL_EF[0]:
        return const.NORMAL_EF[1]
    elif eff_code == const.SUPER_EF[0]:
        return const.SUPER_EF[1]
    elif eff_code == const.LESS_EF[0]:
        return const.LESS_EF[1]
    else:
        return const.NO_EF[1]


def type_chart_parser(json_data, mode=const.CSV):
    header = 'def_type,bug,dark,dragon,electric,fairy,fighting,fire,flying,ghost,grass,ground,ice,normal,poison,psychic,rock,steel,water'
    rows = [header] if mode == const.CSV else []

    for k, v in json_data.items():
        row = k
        for key, val in v['damageTaken'].items():
            if key.lower() in const.PKM_TYPES:
                row += f',{type_effectiveness_converter(val)}'

        if mode == const.SQL:
            row_items = row.split(',')
            row = (f"INSERT INTO pokemon_showdown.tb_static_type_chart ({header}) "
                   f"VALUES ('{row_items[0]}', {','.join(row_items[1:])}) "
                   f"ON DUPLICATE KEY UPDATE bug = {row_items[1]}, dark = {row_items[2]}, dragon = {row_items[3]}, "
                   f"electric = {row_items[4]}, fairy = {row_items[5]}, fighting = {row_items[6]}, fire = {row_items[7]}, "
                   f"flying = {row_items[8]}, ghost = {row_items[9]}, grass = {row_items[10]}, ground = {row_items[11]}, "
                   f"ice = {row_items[12]}, normal = {row_items[13]}, poison = {row_items[14]}, psychic = {row_items[15]}, "
                   f"rock = {row_items[16]}, steel = {row_items[17]}, water = {row_items[18]};")

        rows.append(row)
    return rows


def abilities_parser(json_data, mode=const.CSV):
    header = 'num,ability_code,ability_name'
    rows = [header] if mode == const.CSV else []

    for k, v in json_data.items():
        num = v['num']
        ability_code = k
        ability_name = v['name']

        if mode == const.SQL:
            row = (
                f"INSERT INTO pokemon_showdown.tb_static_abilities ({header}) VALUES ('{num}','{ability_code}','{ability_name}') "
                f"ON DUPLICATE KEY UPDATE ability_code = '{ability_code}', ability_name = '{ability_name}';")
        else:
            row = f'{num},{ability_code},{ability_name}'
        rows.append(row)
    return rows


def movedex_parser(json_data, mode=const.CSV):
    header = 'num,move_name,move_code,base_power,category,type,accuracy,priority,pp,target,isZ'
    rows = [header] if mode == const.CSV else []

    for k, v in json_data.items():
        # exclude fake moves, gmax moves, hiddenpower duplicates
        if 'shadowstrike' in k or 'paleowave' in k or 'gmax' in k or ('hiddenpower' in k and 'hiddenpower' != k):
            continue

        num = v['num']
        move_name = v['name']
        move_code = k
        base_power = v['basePower']
        category = v['category']
        type_ = v['type'].lower()
        accuracy = v['accuracy']
        priority = v['priority']
        pp = v['pp']
        target = v['target']
        isZ = v['isZ'] if 'isZ' in v.keys() is not None else ''

        if mode == const.SQL:
            row = (f"INSERT INTO pokemon_showdown.tb_static_movedex ({header}) "
                   f"VALUES ({num},'{move_name}','{move_code}',{base_power},'{category}','{type_}',{accuracy},{priority},{pp},'{target}','{isZ}') "
                   f"ON DUPLICATE KEY UPDATE move_name='{move_name}', move_code='{move_code}', base_power={base_power}, "
                   f"category='{category}', type='{type_}', accuracy={accuracy}, priority={priority}, pp={pp}, "
                   f"target='{target}', isZ='{isZ}';")
            row = (row.replace(",'',", ',NULL,').replace(',,', ',NULL,')
                   .replace("='',", '=NULL,').replace('=,', '=NULL,').replace(",'',", ',NULL,'))
        else:
            row = f'{num},{move_name},{move_code},{base_power},{category},{type_},{accuracy},{priority},{pp},{target},{isZ}'

        rows.append(row)
    return rows


def items_parser(json_data, mode=const.CSV):
    header = 'num,item_name,item_code,gen,mega_stone,z_move,item_user,fling_base_power'
    rows = [header] if mode == const.CSV else []

    for k, v in json_data.items():
        num = v['num']
        item_name = v['name']
        item_code = k
        gen = v['gen']
        mega_stone = v['megaStone'] if 'megaStone' in v.keys() else ''
        z_move = v['zMove'] if 'zMove' in v.keys() else ''
        item_user = v['itemUser'][0] if 'itemUser' in v.keys() else ''
        fling_base_power = v['fling']['basePower'] if 'fling' in v.keys() else ''

        if mode == const.SQL:
            row = (f"INSERT INTO pokemon_showdown.tb_static_items ({header}) "
                   f"VALUES ({num},'{item_name}','{item_code}',{gen},'{mega_stone}','{z_move}',{item_user},{fling_base_power}) "
                   f"ON DUPLICATE KEY UPDATE item_name='{item_name}', item_code='{item_code}', gen={gen}, "
                   f"mega_stone='{mega_stone}', z_move='{z_move}', item_user={item_user}, fling_base_power={fling_base_power};")
            row = (row.replace(",'',", ',NULL,').replace(',,', ',NULL,')
                   .replace("='',", '=NULL,').replace('=,', '=NULL,').replace(",'',", ',NULL,'))
        else:
            row = f'{num},{item_name},{item_code},{gen},{mega_stone},{z_move},{item_user},{fling_base_power}'

        rows.append(row)
    return rows


def pokedex_parser(json_data, cache, mode=const.CSV):
    header = ('num,pkm_name,type1,type2,base_hp,base_atk,base_def,base_spa,base_spd,base_spe,evolution,evolve_level,'
              'ability1,ability2,ability_hidden,form,base_species,pkm_code')
    rows = [header] if mode == const.CSV else []

    for k, v in json_data.items():
        num = v['num']
        pkm_name = v['name']
        type1 = v['types'][0].lower()
        type2 = v['types'][1].lower() if len(v['types']) > 1 else ''
        base_hp = v['baseStats']['hp']
        base_atk = v['baseStats']['atk']
        base_def = v['baseStats']['def']
        base_spa = v['baseStats']['spa']
        base_spd = v['baseStats']['spd']
        base_spe = v['baseStats']['spe']
        evolution = v['evos'][0] if 'evos' in v.keys() else ''
        evolve_level = v['evoLevel'] if 'evoLevel' in v.keys() else ''
        ability1 = cache.abilities[v['abilities']['0'].lower()
        .replace(' ', '').replace('-', '')
        .replace('(', '').replace(')', '')]['num'] if '0' in v['abilities'].keys() and v['abilities']['0'] else ''
        ability2 = cache.abilities[v['abilities']['1'].lower()
        .replace(' ', '').replace('-', '')
        .replace('(', '').replace(')', '')]['num'] if '1' in v['abilities'].keys() else ''
        ability_hidden = cache.abilities[v['abilities']['H'].lower()
        .replace(' ', '').replace('-', '')
        .replace('(', '').replace(')', '')]['num'] if 'H' in v['abilities'].keys() else ''
        form = v['forme'] if 'forme' in v.keys() else ''
        base_species = v['baseSpecies'] if 'baseSpecies' in v.keys() else ''
        pkm_code = k

        if k == "missingno":
            type1 = 'normal'
            ability1 = 10000

        if mode == const.SQL:
            row = ((f"INSERT INTO pokemon_showdown.tb_static_pokedex ({header}) "
                   f"VALUES ('{num}','{pkm_name}','{type1}','{type2}',{base_hp},{base_atk},{base_def},{base_spa},{base_spd},"
                   f"{base_spe},'{evolution}',{evolve_level},'{ability1}','{ability2}','{ability_hidden}','{form}',"
                   f"'{base_species}','{pkm_code}') "
                   f"ON DUPLICATE KEY UPDATE pkm_name='{pkm_name}',type1='{type1}',type2='{type2}',"
                   f"base_hp={base_hp},base_atk={base_atk},base_def={base_def},base_spa={base_spa},base_spd={base_spd},"
                   f"base_spe={base_spe},evolution='{evolution}',evolve_level={evolve_level},ability1='{ability1}',"
                   f"ability2='{ability2}',ability_hidden='{ability_hidden}',form='{form}',base_species='{base_species}',"
                   f"pkm_code='{pkm_code}';"))
            row = (row.replace(",'',", ',NULL,').replace(',,', ',NULL,')
                   .replace("='',", '=NULL,').replace('=,', '=NULL,').replace(",'',", ',NULL,'))
        else:
            row = (f'{num},{pkm_name},{type1},{type2},{base_hp},{base_atk},{base_def},{base_spa},{base_spd},{base_spe},'
                   f'{evolution},{evolve_level},{ability1},{ability2},{ability_hidden},{form},{base_species},{pkm_code}')

        rows.append(row)
    return rows


def parse_move_learn_code(ml_code):
    for code in const.LS_CODE:
        if code in ml_code:
            if code == const.LVL:
                return [code, ml_code.split(code)[1]]
            else:
                return [code]
        else:
            return []


def learn_sets_parser(json_data, cache, mode=const.CSV):
    header = 'num,pkm_num,move_num,learn_method,learn_level'
    rows = [header] if mode == const.CSV else []

    count_id = 1
    for k, v in json_data.items():
        if 'learnset' in v.keys() and k in cache.pokedex.keys():
            for move, learn in v['learnset'].items():
                # exclude fake moves, gmax moves, hiddenpower duplicates
                if 'shadowstrike' in move or 'paleowave' in move or 'gmax' in move or (
                        'hiddenpower' in move and 'hiddenpower' != move):
                    continue
                num = count_id
                pkm_num = cache.pokedex[k]['num']
                move_num = cache.movedex[move]['num']
                ls_decoded = parse_move_learn_code(learn[0])
                learn_method = ls_decoded[0] if len(ls_decoded) > 1 else ''
                learn_level = ls_decoded[1] if len(ls_decoded) > 1 else ''

                if mode == const.SQL:
                    row = (f"INSERT INTO pokemon_showdown.tb_static_learn_sets ({header}) "
                           f"VALUES ({num},'{pkm_num}',{move_num},'{learn_method}',{learn_level}) "
                           f"ON DUPLICATE KEY UPDATE pkm_num='{pkm_num}',move_num={move_num},"
                           f"learn_method='{learn_method}',learn_level={learn_level};")
                    row = (row.replace(",'',", ',NULL,').replace(',,', ',NULL,')
                           .replace("='',", '=NULL,').replace('=,', '=NULL,')
                           .replace('=;', '=NULL;').replace(',)', ',NULL)').replace(",'',", ',NULL,'))
                else:
                    row = f'{num},{pkm_num},{move_num},{learn_method},{learn_level}'

                rows.append(row)
                count_id += 1
    return rows


def sql_ps_player_parser(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    sql_out = []
    sql_prefix = "INSERT INTO pokemon_showdown.tb_ps_players (id, player_name, register_time, elo, gxe, rpr, rpr_std) VALUES "
    sql_suffix = " AS new ON DUPLICATE KEY UPDATE elo = new.elo, gxe = new.gxe, rpr = new.rpr, rpr_std = new.rpr_std;"

    for v in data.values():
        if 'gen9doublesou' in v['ratings']:
            p_id = v['userid']
            player_name = v['username']
            register_time = v['registertime']
            elo = int(v['ratings']['gen9doublesou']['elo'])
            gxe = round((v['ratings']['gen9doublesou']['gxe']), 2)
            rpr = round((v['ratings']['gen9doublesou']['rpr']), 2)
            rpr_std = round((v['ratings']['gen9doublesou']['rprd']), 2)

            # sql_str = (
            #     f"INSERT INTO pokemon_showdown.tb_ps_players (id, player_name, register_time, elo, gxe, rpr, rpr_std) "
            #     f"VALUES ('{p_id}', '{player_name}', '{register_time}', {elo}, {gxe}, {rpr}, {rpr_std}) "
            #     f"ON DUPLICATE KEY UPDATE elo = {elo}, gxe = {gxe}, rpr = {rpr}, rpr_std = {rpr_std};")
            #
            # sql_out.append(sql_str)

            sql_prefix = sql_prefix + f"('{p_id}', '{player_name}', '{register_time}', {elo}, {gxe}, {rpr}, {rpr_std}),"

    sql_out.append(sql_prefix[:-1] + sql_suffix)

    return sql_out


def sql_ps_replay_parser(filepath, mysql_conn: MySQLConnector):
    with open(filepath, 'r') as file:
        data = json.load(file)
    sql_out = []
    sql_prefix = "INSERT INTO pokemon_showdown.tb_ps_replays (id, upload_time, format, player1, player2) VALUES "
    sql_suffix = " AS new ON DUPLICATE KEY UPDATE upload_time = new.upload_time;"

    for v in data:
        upload_time = v['uploadtime']
        r_format = v['format']
        r_id = v['id']

        player1 = re.sub(r'[^A-Za-z0-9 ]+', '', v['p1']).replace(' ', '').lower()
        player2 = re.sub(r'[^A-Za-z0-9 ]+', '', v['p2']).replace(' ', '').lower()
        p_ids_db = mysql_conn.select(f"SELECT * FROM tb_ps_players WHERE id IN ('{player1}', '{player2}')")

        # skip through battles where there's not enough player data
        if len(p_ids_db) < 2:
            continue

        # sql_str = (f"INSERT INTO pokemon_showdown.tb_ps_replays (id, upload_time, format, player1, player2) "
        #            f"VALUES ('{r_id}', '{upload_time}', '{r_format}', '{player1}', '{player2}') "
        #            f"ON DUPLICATE KEY UPDATE upload_time = '{upload_time}';")

        # sql_out.append(sql_str)

        sql_prefix = sql_prefix + f"('{r_id}', '{upload_time}', '{r_format}', '{player1}', '{player2}'),"

    sql_out.append(sql_prefix[:-1] + sql_suffix)

    return sql_out


def remove_special_pkm_forms_from_battle_log(log):
    cleaned_log = log
    for base,special in SPECIAL_FORMS.items():
        for form in special:
            cleaned_log = cleaned_log.replace(form, base)
    return cleaned_log

def sql_ps_replay_detail_parser(filepath, mysql_conn: MySQLConnector):
    with open(filepath, 'r') as file:
        data = json.load(file)
    sql_out = []
    sql_command = "INSERT INTO pokemon_showdown.tb_ps_replay_details (replay_id, turn, player_id, pkm_id, move_id) VALUES "

    for v in data:
        player1 = re.sub(r'[^A-Za-z0-9 ]+', '', v['p1']).replace(' ', '').lower()
        player2 = re.sub(r'[^A-Za-z0-9 ]+', '', v['p2']).replace(' ', '').lower()
        p_ids_db = mysql_conn.select(f"SELECT * FROM tb_ps_players WHERE id IN ('{player1}', '{player2}')")

        # skip through battles where there's not enough player data
        if len(p_ids_db) < 2:
            continue

        replay_id = v['id']

        battle_log = remove_special_pkm_forms_from_battle_log(v['log'])

        pkm_list = re.findall("(?:switch\||drag\||replace\|).*?\n", battle_log)
        battling_pkm = {}
        for item in pkm_list:
            item = item.replace('p1a', 'p').replace('p1b', 'p').replace('p2a', 'p').replace('p2b', 'p')
            pkm_text = item.replace(' ', '').lower().split('|')[1:3]
            pkm_text = '|'.join(pkm_text).split('p:')[1].split(',')[0]
            p_key = re.sub(r'[^A-Za-z0-9 ]+', '', pkm_text.split('|')[0])
            p_val = re.sub(r'[^A-Za-z0-9 ]+', '', pkm_text.split('|')[1])
            if p_key in battling_pkm.keys():
                continue
            battling_pkm[p_key] = p_val

        moves_by_turn = re.findall("(?:\|turn\||\|move\|).*?\n", battle_log)

        turn = 1
        for mv in moves_by_turn:
            if '|turn|' in mv and mv.index == len(moves_by_turn) - 1:
                break

            if '|turn|' in mv:
                turn = int(mv.replace('|turn|', '').replace('\n', ''))
            else:
                mv_details = re.split('\||/', (mv.replace(' ', '').replace('|move|', '').lower()
                              .replace('p1a:', 'p1a/').replace('p1b:', 'p1a/')
                              .replace('p2a:', 'p1a/').replace('p2b:', 'p1a/')))
                if 'p1' in mv_details[0]:
                    player_id = player1
                else:
                    player_id = player2

                pkm_code = battling_pkm[re.sub(r'[^A-Za-z0-9 ]+', '', mv_details[1])]
                pkm_id = mysql_conn.select(f"SELECT num FROM tb_static_pokedex WHERE pkm_code = '{pkm_code}'")[0][0]
                move_code = re.sub(r'[^A-Za-z0-9 ]+', '', mv_details[2])
                move_id = mysql_conn.select(f"SELECT num FROM tb_static_movedex WHERE move_code = '{move_code}'")[0][0]

                # sql_str = (
                #     f"INSERT INTO pokemon_showdown.tb_ps_replay_details (replay_id, turn, player_id, pkm_id, move_id) "
                #     f"VALUES ('{replay_id}', {turn}, '{player_id}', '{pkm_id}', {move_id});")

                # sql_out.append(sql_str)

                sql_str = f"('{replay_id}', {turn}, '{player_id}', '{pkm_id}', {move_id})"
                sql_command = sql_command + f"{sql_str},"

    sql_out.append(f"{sql_command[:-1]};")

    return sql_out
