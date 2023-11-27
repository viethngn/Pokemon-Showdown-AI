# Create the data warehouse (Data Analytical Layer)
/*
    This trigger will insert into table tb_ps_data_warehouse after an insert has been done into the table tb_ps_replay_details
 */
use pokemon_showdown;

drop trigger if exists insert_ps_data_warehouse;

delimiter $$

create trigger insert_ps_data_warehouse
after insert
on tb_ps_replay_details for each row
begin
    call insert_ps_data_warehouse(new.id, new.replay_id, new.turn, new.player_id, new.pkm_id, new.move_id);
end $$

delimiter ;
