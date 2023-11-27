import argparse
import sys
from datetime import datetime

import src.const.ps_constants as const
from src.utils.ps_parser import sql_ps_player_parser, sql_ps_replay_parser, sql_ps_replay_detail_parser
from src.utils.ps_utils import save_to_files, read_config
from src.utils.udf_utils import open_mysql_connection


def main():
    parser = argparse.ArgumentParser(
        prog='PokemonShowdownDataCollector',
        description='This program insert battle replay data into the MySQL db')
    parser.add_argument('-f', '--filepath')
    parser.add_argument('-d', '--datatype')
    parser.add_argument('-o', '--output_type')
    args = parser.parse_args()

    filepath = args.filepath
    datatype = args.datatype
    output_type = args.output_type
    start_time = datetime.now()

    print(f"Loading from file {filepath}")

    # src parent path
    prog_path = '/'.join(filepath.split('/')[:-3])
    output_file_name_prefix = '_'.join(filepath.split('/')[-1].split('_')[:2])

    # read configs
    configs = read_config(f'{prog_path}/conf/mysql_conf.json')

    # open mysql connection
    mysql_conn = open_mysql_connection(configs)

    if datatype == const.PS_PLAYER:
        sql_list = sql_ps_player_parser(filepath)
        if output_type == const.SQL:
            save_to_files(f"{prog_path}/sql_output/tb_ps_players/{output_file_name_prefix}_tb_players.sql", const.SQL,
                          sql_list)
        elif output_type == const.MYSQL:
            for sql in sql_list:
                mysql_conn.insert(sql)
        else:
            sys.exit(f"Invalid output_type: {output_type}\nExpect: {const.SQL} | {const.MYSQL}")
    elif datatype == const.PS_REPLAY:
        sql_list = sql_ps_replay_parser(filepath, mysql_conn)
        if output_type == const.SQL:
            save_to_files(f"{prog_path}/sql_output/tb_ps_replays/{output_file_name_prefix}_tb_ps_replays.sql",
                          const.SQL, sql_list)
        elif output_type == const.MYSQL:
            for sql in sql_list:
                mysql_conn.insert(sql)
    elif datatype == const.PS_RDETAILS:
        sql_list = sql_ps_replay_detail_parser(filepath, mysql_conn)
        if output_type == const.SQL:
            save_to_files(f"{prog_path}/sql_output/tb_ps_replay_details/{output_file_name_prefix}_tb_ps_replay_details.sql", const.SQL,
                          sql_list)
        elif output_type == const.MYSQL:
            for sql in sql_list:
                mysql_conn.insert(sql)
        else:
            sys.exit(f"Invalid output_type: {output_type}\nExpect: {const.SQL} | {const.MYSQL}")
    else:
        sys.exit(f"Invalid datatype: {datatype}\nExpect: {const.PS_PLAYER} | {const.PS_REPLAY} | {const.PS_RDETAILS}")

    end_time = datetime.now()
    print(f"Process finishes. Time taken: {end_time - start_time}")


if __name__ == '__main__':
    main()
