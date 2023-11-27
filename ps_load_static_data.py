import argparse
import sys
from datetime import datetime

from src.utils.ps_parser import type_chart_parser, abilities_parser, movedex_parser, items_parser, pokedex_parser, \
    learn_sets_parser
from src.utils.ps_utils import load_static_data, save_to_files, read_config
import src.const.ps_constants as const
from src.utils.udf_utils import open_mysql_connection


def main():
    parser = argparse.ArgumentParser(
        prog='PokemonShowdownStaticDataLoaderCollector',
        description='This program collect/load the static pokemon related data from pokemonshowdown.com')
    parser.add_argument('-p', '--program_path')
    parser.add_argument('-o', '--output_type')
    args = parser.parse_args()

    # src parent path
    prog_path = args.program_path
    output_type = args.output_type
    start_time = datetime.now()

    # read configs
    configs = read_config(f'{prog_path}/conf/mysql_conf.json')

    # load static cache
    ps_static_data = load_static_data()

    if output_type == const.SQL:
        save_to_files(f'{prog_path}/replays/static_data/pokedex.sql', const.SQL, ps_static_data.pokedex, const.PKD,
                      ps_static_data)
        save_to_files(f'{prog_path}/replays/static_data/movedex.sql', const.SQL, ps_static_data.movedex, const.MVD)
        save_to_files(f'{prog_path}/replays/static_data/learn_sets.sql', const.SQL, ps_static_data.learn_sets, const.LS,
                      ps_static_data)
        save_to_files(f'{prog_path}/replays/static_data/abilities.sql', const.SQL, ps_static_data.abilities, const.AB)
        save_to_files(f'{prog_path}/replays/static_data/type_chart.sql', const.SQL, ps_static_data.type_chart, const.TC)
        save_to_files(f'{prog_path}/replays/static_data/items.sql', const.SQL, ps_static_data.items, const.ITM)

    elif output_type == const.CSV:
        save_to_files(f'{prog_path}/replays/static_data/pokedex.csv', const.CSV, ps_static_data.pokedex, const.PKD,
                      ps_static_data)
        save_to_files(f'{prog_path}/replays/static_data/movedex.csv', const.CSV, ps_static_data.movedex, const.MVD)
        save_to_files(f'{prog_path}/replays/static_data/learn_sets.csv', const.CSV, ps_static_data.learn_sets, const.LS,
                      ps_static_data)
        save_to_files(f'{prog_path}/replays/static_data/abilities.csv', const.CSV, ps_static_data.abilities, const.AB)
        save_to_files(f'{prog_path}/replays/static_data/type_chart.csv', const.CSV, ps_static_data.type_chart, const.TC)
        save_to_files(f'{prog_path}/replays/static_data/items.csv', const.CSV, ps_static_data.items, const.ITM)

    elif output_type == const.MYSQL:
        # open mysql connection
        mysql_conn = open_mysql_connection(configs)

        type_chart_sql = type_chart_parser(ps_static_data.type_chart, const.SQL)
        abilities_sql = abilities_parser(ps_static_data.abilities, const.SQL)
        movedex_sql = movedex_parser(ps_static_data.movedex, const.SQL)
        # items_sql = items_parser(ps_static_data.items, const.SQL)
        pokedex_sql = pokedex_parser(ps_static_data.pokedex, ps_static_data, const.SQL)
        learn_sets_sql = learn_sets_parser(ps_static_data.learn_sets, ps_static_data, const.SQL)

        # load type chart data to mysql
        for sql in type_chart_sql:
            mysql_conn.insert(sql)

        # load abilities data to mysql
        for sql in abilities_sql:
            mysql_conn.insert(sql)

        # load movedex chart data to mysql
        for sql in movedex_sql:
            mysql_conn.insert(sql)

        # load items chart data to mysql
        # for sql in items_sql:
        #     mysql_conn.insert(sql)

        # load pokedex chart data to mysql
        for sql in pokedex_sql:
            mysql_conn.insert(sql)

        # load learn sets data to mysql
        for sql in learn_sets_sql:
            mysql_conn.insert(sql)

    else:
        sys.exit(f"Invalid datatype: {output_type}\nExpect: {const.SQL} | {const.MYSQL} | {const.CSV}")

    end_time = datetime.now()
    print(f"Process finishes. Time taken: {end_time - start_time}")


if __name__ == '__main__':
    main()
