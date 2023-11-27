use pokemon_showdown;
/*
	This procedure will insert data into warehouse table tb_ps_data_warehouse (Data Analytical Layer).
    Transformation includes:
		- Convert battle timestamp from UNIX to human readable format
        - Calculate the total base stats from each pokemon's individual stats
        - Deduce a pokemon's resistance to each type from the pokemon's type1 and type2
*/
drop procedure if exists insert_ps_data_warehouse;
delimiter //
create procedure insert_ps_data_warehouse(
        in id int,
        in replay_id varchar(100),
        in turn int,
        in player_id varchar(100),
        in pkm_id varchar(100),
        in move_id int
    )
begin
    insert into tb_ps_data_warehouse
    select id as turn_id,
			replay_id as battle_id,
			turn as battle_turn,
			player_id as turn_from_player,
			FROM_UNIXTIME(r.upload_time) as battle_time,
			r.format as battle_format,
			r.player1,
			p1.elo as player1_elo,
			r.player2,
			p2.elo as player2_elo,
			sm.move_name,
			sm.base_power as move_power,
			sm.category as move_category,
			sm.type as move_type,
			sp.pkm_name,
			sp.base_hp + sp.base_atk + sp.base_def + sp.base_spa + sp.base_spd + sp.base_spe as pkm_total_base_stats,
			sp.type1 as pkm_type1,
			sp.type2 as pkm_type2,
			case
				when stc2.def_type is null then
					case
						when stc1.bug < 1  then 'strong'
						when stc1.bug > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.bug = 1 and stc2.bug = 1) or (stc1.bug > 1 and stc2.bug < 1) or (stc1.bug < 1 and stc2.bug > 1)  then 'neutral'
						when stc1.bug > 1 or stc2.bug > 1 then 'weak'
						else 'strong'
					end
			end as pkm_bug_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.dark < 1  then 'strong'
						when stc1.dark > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.dark = 1 and stc2.dark = 1) or (stc1.dark > 1 and stc2.dark < 1) or (stc1.dark < 1 and stc2.dark > 1)  then 'neutral'
						when stc1.dark > 1 or stc2.dark > 1 then 'weak'
						else 'strong'
					end
			end as pkm_dark_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.dragon < 1  then 'strong'
						when stc1.dragon > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.dragon = 1 and stc2.dragon = 1) or (stc1.dragon > 1 and stc2.dragon < 1) or (stc1.dragon < 1 and stc2.dragon > 1)  then 'neutral'
						when stc1.dragon > 1 or stc2.dragon > 1 then 'weak'
						else 'strong'
					end
			end as pkm_dragon_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.electric < 1  then 'strong'
						when stc1.electric > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.electric = 1 and stc2.electric = 1) or (stc1.electric > 1 and stc2.electric < 1) or (stc1.electric < 1 and stc2.electric > 1)  then 'neutral'
						when stc1.electric > 1 or stc2.electric > 1 then 'weak'
						else 'strong'
					end
			end as pkm_electric_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.fairy < 1  then 'strong'
						when stc1.fairy > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.fairy = 1 and stc2.fairy = 1) or (stc1.fairy > 1 and stc2.fairy < 1) or (stc1.fairy < 1 and stc2.fairy > 1)  then 'neutral'
						when stc1.fairy > 1 or stc2.fairy > 1 then 'weak'
						else 'strong'
					end
			end as pkm_fairy_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.fighting < 1  then 'strong'
						when stc1.fighting > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.fighting = 1 and stc2.fighting = 1) or (stc1.fighting > 1 and stc2.fighting < 1) or (stc1.fighting < 1 and stc2.fighting > 1)  then 'neutral'
						when stc1.fighting > 1 or stc2.fighting > 1 then 'weak'
						else 'strong'
					end
			end as pkm_fighting_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.fire < 1  then 'strong'
						when stc1.fire > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.fire = 1 and stc2.fire = 1) or (stc1.fire > 1 and stc2.fire < 1) or (stc1.fire < 1 and stc2.fire > 1)  then 'neutral'
						when stc1.fire > 1 or stc2.fire > 1 then 'weak'
						else 'strong'
					end
			end as pkm_fire_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.flying < 1  then 'strong'
						when stc1.flying > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.flying = 1 and stc2.flying = 1) or (stc1.flying > 1 and stc2.flying < 1) or (stc1.flying < 1 and stc2.flying > 1)  then 'neutral'
						when stc1.flying > 1 or stc2.flying > 1 then 'weak'
						else 'strong'
					end
			end as pkm_flying_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.ghost < 1  then 'strong'
						when stc1.ghost > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.ghost = 1 and stc2.ghost = 1) or (stc1.ghost > 1 and stc2.ghost < 1) or (stc1.ghost < 1 and stc2.ghost > 1)  then 'neutral'
						when stc1.ghost > 1 or stc2.ghost > 1 then 'weak'
						else 'strong'
					end
			end as pkm_ghost_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.grass < 1  then 'strong'
						when stc1.grass > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.grass = 1 and stc2.grass = 1) or (stc1.grass > 1 and stc2.grass < 1) or (stc1.grass < 1 and stc2.grass > 1)  then 'neutral'
						when stc1.grass > 1 or stc2.grass > 1 then 'weak'
						else 'strong'
					end
			end as pkm_grass_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.ground < 1  then 'strong'
						when stc1.ground > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.ground = 1 and stc2.ground = 1) or (stc1.ground > 1 and stc2.ground < 1) or (stc1.ground < 1 and stc2.ground > 1)  then 'neutral'
						when stc1.ground > 1 or stc2.ground > 1 then 'weak'
						else 'strong'
					end
			end as pkm_ground_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.ice < 1  then 'strong'
						when stc1.ice > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.ice = 1 and stc2.ice = 1) or (stc1.ice > 1 and stc2.ice < 1) or (stc1.ice < 1 and stc2.ice > 1)  then 'neutral'
						when stc1.ice > 1 or stc2.ice > 1 then 'weak'
						else 'strong'
					end
			end as pkm_ice_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.normal < 1  then 'strong'
						when stc1.normal > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.normal = 1 and stc2.normal = 1) or (stc1.normal > 1 and stc2.normal < 1) or (stc1.normal < 1 and stc2.normal > 1)  then 'neutral'
						when stc1.normal > 1 or stc2.normal > 1 then 'weak'
						else 'strong'
					end
			end as pkm_normal_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.poison < 1  then 'strong'
						when stc1.poison > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.poison = 1 and stc2.poison = 1) or (stc1.poison > 1 and stc2.poison < 1) or (stc1.poison < 1 and stc2.poison > 1)  then 'neutral'
						when stc1.poison > 1 or stc2.poison > 1 then 'weak'
						else 'strong'
					end
			end as pkm_poison_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.psychic < 1  then 'strong'
						when stc1.psychic > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.psychic = 1 and stc2.psychic = 1) or (stc1.psychic > 1 and stc2.psychic < 1) or (stc1.psychic < 1 and stc2.psychic > 1)  then 'neutral'
						when stc1.psychic > 1 or stc2.psychic > 1 then 'weak'
						else 'strong'
					end
			end as pkm_psychic_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.rock < 1  then 'strong'
						when stc1.rock > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.rock = 1 and stc2.rock = 1) or (stc1.rock > 1 and stc2.rock < 1) or (stc1.rock < 1 and stc2.rock > 1)  then 'neutral'
						when stc1.rock > 1 or stc2.rock > 1 then 'weak'
						else 'strong'
					end
			end as pkm_rock_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.steel < 1  then 'strong'
						when stc1.steel > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.steel = 1 and stc2.steel = 1) or (stc1.steel > 1 and stc2.steel < 1) or (stc1.steel < 1 and stc2.steel > 1)  then 'neutral'
						when stc1.steel > 1 or stc2.steel > 1 then 'weak'
						else 'strong'
					end
			end as pkm_steel_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.water < 1  then 'strong'
						when stc1.water > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.water = 1 and stc2.water = 1) or (stc1.water > 1 and stc2.water < 1) or (stc1.water < 1 and stc2.water > 1)  then 'neutral'
						when stc1.water > 1 or stc2.water > 1 then 'weak'
						else 'strong'
					end
			end as pkm_water_resist
	from tb_ps_replays r
	join tb_ps_players p1 on p1.id = r.player1
	join tb_ps_players p2 on p2.id = r.player2
	join tb_static_pokedex sp on sp.num = pkm_id
	join tb_static_movedex sm on sm.num = move_id
	join tb_static_type_chart stc1 on stc1.def_type = sp.type1
	left join tb_static_type_chart stc2 on stc2.def_type = sp.type2
    where r.id = replay_id;
end //
delimiter ;

/*
	This procedure will create a data warehouse table for the Pokemon Showdown battle data.
    Transformation includes:
		- Convert battle timestamp from UNIX to human readable format
        - Calculate the total base stats from each pokemon's individual stats
        - Deduce a pokemon's resistance to each type from the pokemon's type1 and type2
*/
drop procedure if exists create_ps_data_warehouse;
delimiter //
create procedure create_ps_data_warehouse()
begin
	drop table if exists tb_ps_data_warehouse;
	create table tb_ps_data_warehouse
	select rd.id as turn_id,
			rd.replay_id as battle_id,
			rd.turn as battle_turn,
			rd.player_id as turn_from_player,
			FROM_UNIXTIME(r.upload_time) as battle_time,
			r.format as battle_format,
			r.player1,
			p1.elo as player1_elo,
			r.player2,
			p2.elo as player2_elo,
			sm.move_name,
			sm.base_power as move_power,
			sm.category as move_category,
			sm.type as move_type,
			sp.pkm_name,
			sp.base_hp + sp.base_atk + sp.base_def + sp.base_spa + sp.base_spd + sp.base_spe as pkm_total_base_stats,
			sp.type1 as pkm_type1,
			sp.type2 as pkm_type2,
			case
				when stc2.def_type is null then
					case
						when stc1.bug < 1  then 'strong'
						when stc1.bug > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.bug = 1 and stc2.bug = 1) or (stc1.bug > 1 and stc2.bug < 1) or (stc1.bug < 1 and stc2.bug > 1)  then 'neutral'
						when stc1.bug > 1 or stc2.bug > 1 then 'weak'
						else 'strong'
					end
			end as pkm_bug_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.dark < 1  then 'strong'
						when stc1.dark > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.dark = 1 and stc2.dark = 1) or (stc1.dark > 1 and stc2.dark < 1) or (stc1.dark < 1 and stc2.dark > 1)  then 'neutral'
						when stc1.dark > 1 or stc2.dark > 1 then 'weak'
						else 'strong'
					end
			end as pkm_dark_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.dragon < 1  then 'strong'
						when stc1.dragon > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.dragon = 1 and stc2.dragon = 1) or (stc1.dragon > 1 and stc2.dragon < 1) or (stc1.dragon < 1 and stc2.dragon > 1)  then 'neutral'
						when stc1.dragon > 1 or stc2.dragon > 1 then 'weak'
						else 'strong'
					end
			end as pkm_dragon_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.electric < 1  then 'strong'
						when stc1.electric > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.electric = 1 and stc2.electric = 1) or (stc1.electric > 1 and stc2.electric < 1) or (stc1.electric < 1 and stc2.electric > 1)  then 'neutral'
						when stc1.electric > 1 or stc2.electric > 1 then 'weak'
						else 'strong'
					end
			end as pkm_electric_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.fairy < 1  then 'strong'
						when stc1.fairy > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.fairy = 1 and stc2.fairy = 1) or (stc1.fairy > 1 and stc2.fairy < 1) or (stc1.fairy < 1 and stc2.fairy > 1)  then 'neutral'
						when stc1.fairy > 1 or stc2.fairy > 1 then 'weak'
						else 'strong'
					end
			end as pkm_fairy_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.fighting < 1  then 'strong'
						when stc1.fighting > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.fighting = 1 and stc2.fighting = 1) or (stc1.fighting > 1 and stc2.fighting < 1) or (stc1.fighting < 1 and stc2.fighting > 1)  then 'neutral'
						when stc1.fighting > 1 or stc2.fighting > 1 then 'weak'
						else 'strong'
					end
			end as pkm_fighting_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.fire < 1  then 'strong'
						when stc1.fire > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.fire = 1 and stc2.fire = 1) or (stc1.fire > 1 and stc2.fire < 1) or (stc1.fire < 1 and stc2.fire > 1)  then 'neutral'
						when stc1.fire > 1 or stc2.fire > 1 then 'weak'
						else 'strong'
					end
			end as pkm_fire_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.flying < 1  then 'strong'
						when stc1.flying > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.flying = 1 and stc2.flying = 1) or (stc1.flying > 1 and stc2.flying < 1) or (stc1.flying < 1 and stc2.flying > 1)  then 'neutral'
						when stc1.flying > 1 or stc2.flying > 1 then 'weak'
						else 'strong'
					end
			end as pkm_flying_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.ghost < 1  then 'strong'
						when stc1.ghost > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.ghost = 1 and stc2.ghost = 1) or (stc1.ghost > 1 and stc2.ghost < 1) or (stc1.ghost < 1 and stc2.ghost > 1)  then 'neutral'
						when stc1.ghost > 1 or stc2.ghost > 1 then 'weak'
						else 'strong'
					end
			end as pkm_ghost_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.grass < 1  then 'strong'
						when stc1.grass > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.grass = 1 and stc2.grass = 1) or (stc1.grass > 1 and stc2.grass < 1) or (stc1.grass < 1 and stc2.grass > 1)  then 'neutral'
						when stc1.grass > 1 or stc2.grass > 1 then 'weak'
						else 'strong'
					end
			end as pkm_grass_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.ground < 1  then 'strong'
						when stc1.ground > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.ground = 1 and stc2.ground = 1) or (stc1.ground > 1 and stc2.ground < 1) or (stc1.ground < 1 and stc2.ground > 1)  then 'neutral'
						when stc1.ground > 1 or stc2.ground > 1 then 'weak'
						else 'strong'
					end
			end as pkm_ground_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.ice < 1  then 'strong'
						when stc1.ice > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.ice = 1 and stc2.ice = 1) or (stc1.ice > 1 and stc2.ice < 1) or (stc1.ice < 1 and stc2.ice > 1)  then 'neutral'
						when stc1.ice > 1 or stc2.ice > 1 then 'weak'
						else 'strong'
					end
			end as pkm_ice_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.normal < 1  then 'strong'
						when stc1.normal > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.normal = 1 and stc2.normal = 1) or (stc1.normal > 1 and stc2.normal < 1) or (stc1.normal < 1 and stc2.normal > 1)  then 'neutral'
						when stc1.normal > 1 or stc2.normal > 1 then 'weak'
						else 'strong'
					end
			end as pkm_normal_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.poison < 1  then 'strong'
						when stc1.poison > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.poison = 1 and stc2.poison = 1) or (stc1.poison > 1 and stc2.poison < 1) or (stc1.poison < 1 and stc2.poison > 1)  then 'neutral'
						when stc1.poison > 1 or stc2.poison > 1 then 'weak'
						else 'strong'
					end
			end as pkm_poison_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.psychic < 1  then 'strong'
						when stc1.psychic > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.psychic = 1 and stc2.psychic = 1) or (stc1.psychic > 1 and stc2.psychic < 1) or (stc1.psychic < 1 and stc2.psychic > 1)  then 'neutral'
						when stc1.psychic > 1 or stc2.psychic > 1 then 'weak'
						else 'strong'
					end
			end as pkm_psychic_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.rock < 1  then 'strong'
						when stc1.rock > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.rock = 1 and stc2.rock = 1) or (stc1.rock > 1 and stc2.rock < 1) or (stc1.rock < 1 and stc2.rock > 1)  then 'neutral'
						when stc1.rock > 1 or stc2.rock > 1 then 'weak'
						else 'strong'
					end
			end as pkm_rock_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.steel < 1  then 'strong'
						when stc1.steel > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.steel = 1 and stc2.steel = 1) or (stc1.steel > 1 and stc2.steel < 1) or (stc1.steel < 1 and stc2.steel > 1)  then 'neutral'
						when stc1.steel > 1 or stc2.steel > 1 then 'weak'
						else 'strong'
					end
			end as pkm_steel_resist,
			case
				when stc2.def_type is null then
					case
						when stc1.water < 1  then 'strong'
						when stc1.water > 1 then 'weak'
						else 'neutral'
					end
				else
					case
						when (stc1.water = 1 and stc2.water = 1) or (stc1.water > 1 and stc2.water < 1) or (stc1.water < 1 and stc2.water > 1)  then 'neutral'
						when stc1.water > 1 or stc2.water > 1 then 'weak'
						else 'strong'
					end
			end as pkm_water_resist
	from tb_ps_replay_details rd
	join tb_ps_replays r on r.id = rd.replay_id
	join tb_ps_players p1 on p1.id = r.player1
	join tb_ps_players p2 on p2.id = r.player2
	join tb_static_pokedex sp on sp.num = rd.pkm_id
	join tb_static_movedex sm on sm.num = rd.move_id
	join tb_static_type_chart stc1 on stc1.def_type = sp.type1
	left join tb_static_type_chart stc2 on stc2.def_type = sp.type2;

	alter table pokemon_showdown.tb_ps_data_warehouse add constraint tb_ps_data_warehouse_pk primary key (turn_id);

end //
delimiter ;
