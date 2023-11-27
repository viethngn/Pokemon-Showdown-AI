USE pokemon_showdown;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE tb_static_abilities;
TRUNCATE tb_static_learn_sets;
TRUNCATE tb_static_movedex;
TRUNCATE tb_static_pokedex;
TRUNCATE tb_static_type_chart;
SET FOREIGN_KEY_CHECKS = 1;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE tb_ps_players;
TRUNCATE tb_ps_replays;
TRUNCATE tb_ps_replay_details;
SET FOREIGN_KEY_CHECKS = 1;