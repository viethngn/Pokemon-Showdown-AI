/*
    Create event to refresh all views every 1 minutes for the next 30 minutes
 */
use pokemon_showdown;

drop event if exists event_refresh_all_views;

delimiter $$

create event event_refresh_all_views
on schedule every 1 minute
starts current_timestamp()
ends current_timestamp() + interval 30 minute
do
	begin
        # Create view of summary statistics of Pokemon Showdown player elo ranking
        call create_view_player_elo_summary_statistics();

        # Create view of summary statistics of Pokemon total base stats
        call create_view_pokemon_total_base_stats_summary_statistics();

        # Create view of top 20 most used pokemons
        call create_view_top_20_most_used_pokemons();

        # Create view of top 20 most used moves
        call create_view_top_20_most_used_moves();

        # Create summary view of all battle pokemon weaknesses
        call create_view_battle_pkm_weaknesses();
	end$$
delimiter ;
