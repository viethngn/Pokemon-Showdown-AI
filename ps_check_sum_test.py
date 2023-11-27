from tabulate import tabulate

from src.db.mysql_connector import MySQLConnector


def sql_check_sum():
    check_sum = []
    header = ['Table/View', 'Count', 'As Expected']

    mysql_conn = MySQLConnector(host='localhost',
                          user='autoaccess',
                          password='autoaccess',
                          database='pokemon_showdown',
                          port=3306)

    query_ps_players = 'select count(*) from tb_ps_players;'
    query_tb_ps_replays = 'select count(*) from tb_ps_replays;'
    query_tb_ps_replay_details = 'select count(*) from tb_ps_replay_details;'

    query_tb_ps_data_warehouse = 'select count(*) from tb_ps_data_warehouse;'

    query_view_top_20_most_used_pokemons = 'select count(*) from view_top_20_most_used_pokemons;'
    query_view_top_20_most_used_moves = 'select count(*) from view_top_20_most_used_moves;'
    query_view_pokemon_total_base_stats_summary_statistics = 'select count(*) from view_pokemon_total_base_stats_summary_statistics;'
    query_view_player_elo_summary_statistics = 'select count(*) from view_player_elo_summary_statistics;'
    query_view_battle_pkm_weaknesses = 'select count(*) from view_battle_pkm_weaknesses;'

    count_ps_players = mysql_conn.select(query_ps_players)[0][0]
    count_ps_replays = mysql_conn.select(query_tb_ps_replays)[0][0]
    count_ps_replay_details = mysql_conn.select(query_tb_ps_replay_details)[0][0]

    count_tb_ps_data_warehouse = mysql_conn.select(query_tb_ps_data_warehouse)[0][0]

    count_view_top_20_most_used_pokemons = mysql_conn.select(query_view_top_20_most_used_pokemons)[0][0]
    count_view_top_20_most_used_moves = mysql_conn.select(query_view_top_20_most_used_moves)[0][0]
    count_view_pokemon_total_base_stats_summary_statistics = mysql_conn.select(query_view_pokemon_total_base_stats_summary_statistics)[0][0]
    count_view_player_elo_summary_statistics = mysql_conn.select(query_view_player_elo_summary_statistics)[0][0]
    count_view_battle_pkm_weaknesses = mysql_conn.select(query_view_battle_pkm_weaknesses)[0][0]

    if count_ps_players == 1756:
        check_sum.append(('tb_ps_players', count_ps_players, True))
    else:
        check_sum.append(('tb_ps_players', count_ps_players, False))

    if count_ps_replays == 1495:
        check_sum.append(('tb_ps_replays', count_ps_replays, True))
    else:
        check_sum.append(('tb_ps_replays', count_ps_replays, False))

    if count_ps_replay_details == 140_709:
        check_sum.append(('tb_ps_replay_details', count_ps_replay_details, True))
    else:
        check_sum.append(('tb_ps_replay_details', count_ps_replay_details, False))

    if count_tb_ps_data_warehouse == 140_709:
        check_sum.append(('tb_ps_data_warehouse', count_tb_ps_data_warehouse, True))
    else:
        check_sum.append(('tb_ps_data_warehouse', count_tb_ps_data_warehouse, False))

    if count_view_top_20_most_used_pokemons == 20:
        check_sum.append(('view_top_20_most_used_pokemons', count_view_top_20_most_used_pokemons, True))
    else:
        check_sum.append(('view_top_20_most_used_pokemons', count_view_top_20_most_used_pokemons, False))

    if count_view_top_20_most_used_moves == 20:
        check_sum.append(('view_top_20_most_used_moves', count_view_top_20_most_used_moves, True))
    else:
        check_sum.append(('view_top_20_most_used_moves', count_view_top_20_most_used_moves, False))

    if count_view_pokemon_total_base_stats_summary_statistics == 1:
        check_sum.append(('view_pokemon_total_base_stats_summary_statistics', count_view_pokemon_total_base_stats_summary_statistics, True))
    else:
        check_sum.append(('view_pokemon_total_base_stats_summary_statistics', count_view_pokemon_total_base_stats_summary_statistics, False))

    if count_view_player_elo_summary_statistics == 1:
        check_sum.append(('view_player_elo_summary_statistics', count_view_player_elo_summary_statistics, True))
    else:
        check_sum.append(('view_player_elo_summary_statistics', count_view_player_elo_summary_statistics, False))

    if count_view_battle_pkm_weaknesses == 18:
        check_sum.append(('view_battle_pkm_weaknesses', count_view_battle_pkm_weaknesses, True))
    else:
        check_sum.append(('view_battle_pkm_weaknesses', count_view_battle_pkm_weaknesses, False))

    print('Check sum of tables & views test:')
    print(tabulate(check_sum, headers=header))

def main():
    sql_check_sum()


if __name__ == '__main__':
    main()