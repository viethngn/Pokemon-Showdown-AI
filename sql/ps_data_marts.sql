use pokemon_showdown;

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
