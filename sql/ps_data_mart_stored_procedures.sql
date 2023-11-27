use pokemon_showdown;
/*
	This procedure will create a view for the summary statistics of Pokemon Showdown player elo ranking
*/
drop procedure if exists create_view_player_elo_summary_statistics;
delimiter //
create procedure create_view_player_elo_summary_statistics()
begin
    declare player_count int;
    declare mean_elo decimal;
    declare median_elo decimal;
    declare `25%ile_elo` decimal;
    declare `75%ile_elo` decimal;
    declare elo_std decimal;
    declare max_elo decimal;
    declare min_elo decimal;

    declare median_mark int;
    declare `25%ile_mark` int;
    declare `75%ile_mark` int;

    drop table if exists tmp_tb_all_player_elo;
    create table tmp_tb_all_player_elo
    select turn_from_player as player,
    round(avg(player1_elo), 2) as elo from tb_ps_data_warehouse
    group by turn_from_player
    order by elo;

    select count(*) into player_count from tmp_tb_all_player_elo;

    select floor(player_count / 2 - 1) into median_mark;
    select floor(player_count * 25 / 100 - 1) into `25%ile_mark`;
    select floor(player_count * 75 / 100 - 1) into `75%ile_mark`;

    select round(avg(elo), 2) into mean_elo from tmp_tb_all_player_elo;
    select elo into median_elo from tmp_tb_all_player_elo limit median_mark, 1;
    select elo into `25%ile_elo` from tmp_tb_all_player_elo limit `25%ile_mark`, 1;
    select elo into `75%ile_elo` from tmp_tb_all_player_elo limit `75%ile_mark`, 1;
    select stddev(elo) into elo_std from tmp_tb_all_player_elo;
    select max(elo) into max_elo from tmp_tb_all_player_elo;
    select min(elo) into min_elo from tmp_tb_all_player_elo;

    drop table tmp_tb_all_player_elo;

    drop view if exists view_player_elo_summary_statistics;
    drop table if exists tmp_view_player_elo_summary_statistics;
    create table tmp_view_player_elo_summary_statistics
    select player_count, mean_elo, elo_std, min_elo, `25%ile_elo`, median_elo, `75%ile_elo`, max_elo;
    create view view_player_elo_summary_statistics as
    select * from tmp_view_player_elo_summary_statistics;

end //
delimiter ;

/*
	This procedure will create a view for the summary statistics of Pokemon total base stats (tbs) in battle
*/
drop procedure if exists create_view_pokemon_total_base_stats_summary_statistics;
delimiter //
create procedure create_view_pokemon_total_base_stats_summary_statistics()
begin
    declare pokemmon_count int;
    declare mean_tbs int;
    declare median_tbs int;
    declare `25%ile_tbs` int;
    declare `75%ile_tbs` int;
    declare tbs_std decimal;
    declare max_tbs int;
    declare min_tbs int;

    declare median_mark int;
    declare `25%ile_mark` int;
    declare `75%ile_mark` int;

    drop table if exists tmp_tb_all_pkm_total_base_stats;
    create table tmp_tb_all_pkm_total_base_stats
    select pkm_name as pokemon,
    avg(pkm_total_base_stats) as pkm_total_base_stats from tb_ps_data_warehouse
    group by pkm_name
    order by pkm_total_base_stats;

    select count(*) into pokemmon_count from tmp_tb_all_pkm_total_base_stats;

    select floor(pokemmon_count / 2 - 1) into median_mark;
    select floor(pokemmon_count * 25 / 100 - 1) into `25%ile_mark`;
    select floor(pokemmon_count * 75 / 100 - 1) into `75%ile_mark`;

    select round(avg(pkm_total_base_stats), 2) into mean_tbs from tmp_tb_all_pkm_total_base_stats;
    select pkm_total_base_stats into median_tbs from tmp_tb_all_pkm_total_base_stats limit median_mark, 1;
    select pkm_total_base_stats into `25%ile_tbs` from tmp_tb_all_pkm_total_base_stats limit `25%ile_mark`, 1;
    select pkm_total_base_stats into `75%ile_tbs` from tmp_tb_all_pkm_total_base_stats limit `75%ile_mark`, 1;
    select stddev(pkm_total_base_stats) into tbs_std from tmp_tb_all_pkm_total_base_stats;
    select max(pkm_total_base_stats) into max_tbs from tmp_tb_all_pkm_total_base_stats;
    select min(pkm_total_base_stats) into min_tbs from tmp_tb_all_pkm_total_base_stats;

    drop table tmp_tb_all_pkm_total_base_stats;

    drop view if exists view_pokemon_total_base_stats_summary_statistics;
    drop table if exists tmp_view_pokemon_total_base_stats_summary_statistics;
    create table tmp_view_pokemon_total_base_stats_summary_statistics
    select pokemmon_count,mean_tbs,tbs_std,
           min_tbs,`25%ile_tbs`,median_tbs,`75%ile_tbs`,max_tbs;
    create view view_pokemon_total_base_stats_summary_statistics as
    select * from tmp_view_pokemon_total_base_stats_summary_statistics;

end //
delimiter ;

/*
	This procedure will create a view for the top 20 most used Pokemon in battle and their total base stats (tbs)
*/
drop procedure if exists create_view_top_20_most_used_pokemons;
delimiter //
create procedure create_view_top_20_most_used_pokemons()
begin
    drop view if exists view_top_20_most_used_pokemons;
    create view view_top_20_most_used_pokemons as
    select pkm_usage3.pkm_name,
    concat(round((pkm_usage3.num_use/(select count(*)
                                      from (select distinct battle_id, pkm_name, turn_from_player
                                            from tb_ps_data_warehouse) as pkm_usage1) * 100), 2), '%') as usage_rate,
    pkm_usage4.pkm_total_base_stats as pkm_tbs
    from
    (select pkm_usage2.pkm_name,
    count(pkm_usage2.pkm_name) as num_use
    from
    (select distinct battle_id, pkm_name, turn_from_player from tb_ps_data_warehouse) as pkm_usage2
    group by pkm_usage2.pkm_name
    order by num_use desc
    limit 20) as pkm_usage3
    join (select distinct pkm_name, pkm_total_base_stats from tb_ps_data_warehouse) as pkm_usage4
        on pkm_usage4.pkm_name = pkm_usage3.pkm_name;
end //
delimiter ;

/*
	This procedure will create a view for the top 24 most used Pokemon moves in battle
	and their category, power and type
*/
drop procedure if exists create_view_top_20_most_used_moves;
delimiter //
create procedure create_view_top_20_most_used_moves()
begin
    drop view if exists view_top_20_most_used_moves;
    create view view_top_20_most_used_moves as
    select mv_usage.move_name,
    concat(round((mv_usage.usage_count/(select count(*) from tb_ps_data_warehouse) * 100), 2), '%') as usage_rate,
    sm.move_category,
    sm.move_power,
    sm.move_type
    from
    (select move_name, count(move_name) as usage_count from tb_ps_data_warehouse
    group by move_name
    limit 20) as mv_usage
    join (select distinct move_name, move_category, move_power, move_type from tb_ps_data_warehouse) as sm
        on sm.move_name = mv_usage.move_name
    order by usage_rate desc;
end //
delimiter ;

/*
	This procedure will create a view for the summary statistics of Pokemon Showdown player elo ranking
*/
drop procedure if exists create_view_battle_pkm_weaknesses;
delimiter //
create procedure create_view_battle_pkm_weaknesses()
begin
    declare total_pokemon_used int;
    declare weak_to_bug varchar(100);
    declare weak_to_dark varchar(100);
    declare weak_to_dragon varchar(100);
    declare weak_to_electric varchar(100);
    declare weak_to_fairy varchar(100);
    declare weak_to_fighting varchar(100);
    declare weak_to_fire varchar(100);
    declare weak_to_flying varchar(100);
    declare weak_to_ghost varchar(100);
    declare weak_to_grass varchar(100);
    declare weak_to_ground varchar(100);
    declare weak_to_ice varchar(100);
    declare weak_to_normal varchar(100);
    declare weak_to_poison varchar(100);
    declare weak_to_psychic varchar(100);
    declare weak_to_rock varchar(100);
    declare weak_to_steel varchar(100);
    declare weak_to_water varchar(100);

    drop table if exists tmp_tb_all_pkm_type_resistance;
    create table tmp_tb_all_pkm_type_resistance
    select distinct pkm_name as pokemon,
    pkm_type1,
    pkm_type2,
    pkm_bug_resist,
    pkm_dark_resist,
    pkm_dragon_resist,
    pkm_electric_resist,
    pkm_fairy_resist,
    pkm_fighting_resist,
    pkm_fire_resist,
    pkm_flying_resist,
    pkm_ghost_resist,
    pkm_grass_resist,
    pkm_ground_resist,
    pkm_ice_resist,
    pkm_normal_resist,
    pkm_poison_resist,
    pkm_psychic_resist,
    pkm_rock_resist,
    pkm_steel_resist,
    pkm_water_resist
    from tb_ps_data_warehouse
    order by pkm_name;

    select count(*) into total_pokemon_used from tmp_tb_all_pkm_type_resistance;

    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_bug from tmp_tb_all_pkm_type_resistance where pkm_bug_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_dark from tmp_tb_all_pkm_type_resistance where pkm_dark_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_dragon from tmp_tb_all_pkm_type_resistance where pkm_dragon_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_electric from tmp_tb_all_pkm_type_resistance where pkm_electric_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_fairy from tmp_tb_all_pkm_type_resistance where pkm_fairy_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_fighting from tmp_tb_all_pkm_type_resistance where pkm_fighting_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_fire from tmp_tb_all_pkm_type_resistance where pkm_fire_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_flying from tmp_tb_all_pkm_type_resistance where pkm_flying_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_ghost from tmp_tb_all_pkm_type_resistance where pkm_ghost_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_grass from tmp_tb_all_pkm_type_resistance where pkm_grass_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_ground from tmp_tb_all_pkm_type_resistance where pkm_ground_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_ice from tmp_tb_all_pkm_type_resistance where pkm_ice_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_normal from tmp_tb_all_pkm_type_resistance where pkm_normal_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_poison from tmp_tb_all_pkm_type_resistance where pkm_poison_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_psychic from tmp_tb_all_pkm_type_resistance where pkm_psychic_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_rock from tmp_tb_all_pkm_type_resistance where pkm_rock_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_steel from tmp_tb_all_pkm_type_resistance where pkm_steel_resist = 'weak';
    select concat(round(count(*)/total_pokemon_used * 100, 2), '%') into weak_to_water from tmp_tb_all_pkm_type_resistance where pkm_water_resist = 'weak';

    drop table if exists tmp_tb_all_pkm_type_resistance;
    drop table if exists tmp_view_battle_pkm_weaknesses;
    create table tmp_view_battle_pkm_weaknesses
        (pkm_weakness varchar(30) not null,
        percentage varchar(10) not null) comment = 'Support table for view_battle_pkm_weaknesses';
    insert into tmp_view_battle_pkm_weaknesses values
        ('bug', weak_to_bug),
        ('dark', weak_to_dark),
        ('dark', weak_to_dark),
        ('electric', weak_to_electric),
        ('fairy', weak_to_fairy),
        ('fighting', weak_to_fighting),
        ('fire', weak_to_fire),
        ('flying', weak_to_flying),
        ('ghost', weak_to_ghost),
        ('grass', weak_to_grass),
        ('ground', weak_to_ground),
        ('ice', weak_to_ice),
        ('normal', weak_to_normal),
        ('poison', weak_to_poison),
        ('psychic', weak_to_psychic),
        ('rock', weak_to_rock),
        ('steel', weak_to_steel),
        ('water', weak_to_water);

    drop view if exists view_battle_pkm_weaknesses;
    create view view_battle_pkm_weaknesses as
    select * from tmp_view_battle_pkm_weaknesses order by percentage desc;

end //
delimiter ;