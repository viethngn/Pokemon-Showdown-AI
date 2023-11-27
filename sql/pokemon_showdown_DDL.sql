DROP DATABASE IF EXISTS `pokemon_showdown`;
CREATE DATABASE `pokemon_showdown` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `pokemon_showdown`;

CREATE TABLE `tb_static_type_chart` (
  `def_type` varchar(100) NOT NULL,
  `bug` decimal(10,2) NOT NULL,
  `dark` decimal(10,2) NOT NULL,
  `dragon` decimal(10,2) NOT NULL,
  `electric` decimal(10,2) NOT NULL,
  `fairy` decimal(10,2) NOT NULL,
  `fighting` decimal(10,2) NOT NULL,
  `fire` decimal(10,2) NOT NULL,
  `flying` decimal(10,2) NOT NULL,
  `ghost` decimal(10,2) NOT NULL,
  `grass` decimal(10,2) NOT NULL,
  `ground` decimal(10,2) NOT NULL,
  `ice` decimal(10,2) NOT NULL,
  `normal` decimal(10,2) NOT NULL,
  `poison` decimal(10,2) NOT NULL,
  `psychic` decimal(10,2) NOT NULL,
  `rock` decimal(10,2) NOT NULL,
  `steel` decimal(10,2) NOT NULL,
  `water` decimal(10,2) NOT NULL,
  PRIMARY KEY (`def_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Defensive Type chart of all pokemons';

CREATE TABLE `tb_static_abilities` (
  `num` varchar(50) NOT NULL,
  `ability_code` varchar(100) NOT NULL,
  `ability_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='All pokemon abilities';

CREATE TABLE `tb_static_movedex` (
  `num` int NOT NULL,
  `move_name` varchar(100) NOT NULL,
  `move_code` varchar(100) NOT NULL,
  `base_power` int NOT NULL,
  `category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` varchar(100) NOT NULL,
  `accuracy` int NOT NULL,
  `priority` int NOT NULL,
  `pp` int NOT NULL,
  `target` varchar(100) NOT NULL,
  `isZ` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`num`),
  KEY `tb_static_movedex_FK` (`type`),
  CONSTRAINT `tb_static_movedex_FK` FOREIGN KEY (`type`) REFERENCES `tb_static_type_chart` (`def_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='All Pokemon moves';

CREATE TABLE `tb_static_pokedex` (
  `num` varchar(100) NOT NULL,
  `pkm_name` varchar(100) NOT NULL,
  `type1` varchar(100) NOT NULL,
  `type2` varchar(100) DEFAULT NULL,
  `base_hp` int NOT NULL,
  `base_atk` int NOT NULL,
  `base_def` int NOT NULL,
  `base_spa` int NOT NULL,
  `base_spd` int NOT NULL,
  `base_spe` int NOT NULL,
  `evolution` varchar(100) DEFAULT NULL,
  `evolve_level` int DEFAULT NULL,
  `ability1` varchar(50) NOT NULL,
  `ability2` varchar(50) DEFAULT NULL,
  `ability_hidden` varchar(50) DEFAULT NULL,
  `form` varchar(100) DEFAULT NULL,
  `base_species` varchar(100) DEFAULT NULL,
  `pkm_code` varchar(100) NOT NULL,
  PRIMARY KEY (`num`),
  KEY `tb_static_pokedex_FK_3` (`type1`),
  KEY `tb_static_pokedex_FK_4` (`type2`),
  KEY `tb_static_pokedex_FK_1` (`ability2`),
  KEY `tb_static_pokedex_FK_2` (`ability_hidden`),
  KEY `tb_static_pokedex_FK` (`ability1`),
  CONSTRAINT `tb_static_pokedex_FK` FOREIGN KEY (`ability1`) REFERENCES `tb_static_abilities` (`num`),
  CONSTRAINT `tb_static_pokedex_FK_1` FOREIGN KEY (`ability2`) REFERENCES `tb_static_abilities` (`num`),
  CONSTRAINT `tb_static_pokedex_FK_2` FOREIGN KEY (`ability_hidden`) REFERENCES `tb_static_abilities` (`num`),
  CONSTRAINT `tb_static_pokedex_FK_3` FOREIGN KEY (`type1`) REFERENCES `tb_static_type_chart` (`def_type`),
  CONSTRAINT `tb_static_pokedex_FK_4` FOREIGN KEY (`type2`) REFERENCES `tb_static_type_chart` (`def_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Pokedex!';

CREATE TABLE `tb_static_learn_sets` (
  `num` int NOT NULL AUTO_INCREMENT,
  `pkm_num` varchar(100) NOT NULL,
  `move_num` int NOT NULL,
  `learn_method` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `learn_level` int DEFAULT NULL,
  PRIMARY KEY (`num`),
  KEY `tb_static_learn_sets_FK` (`move_num`),
  KEY `tb_static_learn_sets_FK_1` (`pkm_num`),
  CONSTRAINT `tb_static_learn_sets_FK` FOREIGN KEY (`move_num`) REFERENCES `tb_static_movedex` (`num`),
  CONSTRAINT `tb_static_learn_sets_FK_1` FOREIGN KEY (`pkm_num`) REFERENCES `tb_static_pokedex` (`num`)
) ENGINE=InnoDB AUTO_INCREMENT=87992 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='All Pokemon possible moveset';

CREATE TABLE `tb_ps_players` (
  `id` varchar(100) NOT NULL,
  `player_name` varchar(100) NOT NULL,
  `register_time` varchar(100) NOT NULL,
  `elo` int NOT NULL,
  `gxe` decimal(10,2) DEFAULT NULL,
  `rpr` decimal(10,2) DEFAULT NULL,
  `rpr_std` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Pokemon Showdown player details & rankings';

CREATE TABLE `tb_ps_replays` (
  `id` varchar(100) NOT NULL,
  `upload_time` varchar(100) NOT NULL,
  `format` varchar(100) NOT NULL,
  `player1` varchar(100) NOT NULL,
  `player2` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tb_ps_replays_FK` (`player1`),
  KEY `tb_ps_replays_FK_1` (`player2`),
  CONSTRAINT `tb_ps_replays_FK` FOREIGN KEY (`player1`) REFERENCES `tb_ps_players` (`id`),
  CONSTRAINT `tb_ps_replays_FK_1` FOREIGN KEY (`player2`) REFERENCES `tb_ps_players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Pokemon Showdown Replays';

CREATE TABLE `tb_ps_replay_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `replay_id` varchar(100) NOT NULL,
  `turn` int NOT NULL,
  `player_id` varchar(100) NOT NULL,
  `pkm_id` varchar(100) NOT NULL,
  `move_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tb_ps_replay_details_FK_1` (`player_id`),
  KEY `tb_ps_replay_details_FK_2` (`move_id`),
  KEY `tb_ps_replay_details_FK_3` (`pkm_id`),
  KEY `tb_ps_replay_details_FK` (`replay_id`),
  CONSTRAINT `tb_ps_replay_details_FK` FOREIGN KEY (`replay_id`) REFERENCES `tb_ps_replays` (`id`),
  CONSTRAINT `tb_ps_replay_details_FK_1` FOREIGN KEY (`player_id`) REFERENCES `tb_ps_players` (`id`),
  CONSTRAINT `tb_ps_replay_details_FK_2` FOREIGN KEY (`move_id`) REFERENCES `tb_static_movedex` (`num`),
  CONSTRAINT `tb_ps_replay_details_FK_3` FOREIGN KEY (`pkm_id`) REFERENCES `tb_static_pokedex` (`num`)
) ENGINE=InnoDB AUTO_INCREMENT=153844 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Details of each battle by turn';

CREATE TABLE `tb_ps_data_warehouse` (
  `turn_id` int NOT NULL DEFAULT '0',
  `battle_id` varchar(100) NOT NULL,
  `battle_turn` int NOT NULL,
  `turn_from_player` varchar(100) NOT NULL,
  `battle_time` datetime(6) DEFAULT NULL,
  `battle_format` varchar(100) NOT NULL,
  `player1` varchar(100) NOT NULL,
  `player1_elo` int NOT NULL,
  `player2` varchar(100) NOT NULL,
  `player2_elo` int NOT NULL,
  `move_name` varchar(100) NOT NULL,
  `move_power` int NOT NULL,
  `move_category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `move_type` varchar(100) NOT NULL,
  `pkm_name` varchar(100) NOT NULL,
  `pkm_total_base_stats` bigint NOT NULL DEFAULT '0',
  `pkm_type1` varchar(100) NOT NULL,
  `pkm_type2` varchar(100) DEFAULT NULL,
  `pkm_bug_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_dark_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_dragon_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_electric_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_fairy_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_fighting_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_fire_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_flying_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_ghost_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_grass_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_ground_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_ice_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_normal_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_poison_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_psychic_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_rock_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_steel_resist` varchar(7) NOT NULL DEFAULT '',
  `pkm_water_resist` varchar(7) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;