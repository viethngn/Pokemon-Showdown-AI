from src.db.mysql_connector import MySQLConnector
from src.entities.game_state import GameState
from src.entities.player_state import PlayerState
from src.entities.pokemon import Pokemon
from src.utils.ps_utils import clean_pkm_name_text
import src.const.ps_constants as const


def get_player_pkm_list(log: list[str]):
    p1 = []
    p2 = []
    for row in log:
        if '|poke|' in row:
            if '|p1|' in row:
                p1.append(clean_pkm_name_text(row.split('|')[3].split(',')[0]))
            else:
                p2.append(clean_pkm_name_text(row.split('|')[3].split(',')[0]))
        else:
            continue
    return p1, p2


def create_player_state(mysql_conn: MySQLConnector, pkm_list: list[str]):
    pkms = []

    has_bug = False
    has_dark = False
    has_dragon = False
    has_electric = False
    has_fairy = False
    has_fighting = False
    has_fire = False
    has_flying = False
    has_ghost = False
    has_grass = False
    has_ground = False
    has_ice = False
    has_normal = False
    has_poison = False
    has_psychic = False
    has_rock = False
    has_steel = False
    has_water = False

    for pkm_code in pkm_list:
        db_res = mysql_conn.select(f"select * from tb_static_pokedex where pkm_code = '{pkm_code}';")
        if len(db_res) == 0:
            raise Exception(f"No pokemon data found. Pokemon code is {pkm_code}")
        pkm_detail = db_res[0]
        pkm = Pokemon(pkm_detail[0], pkm_code)

        if pkm_detail[2] == 'bug' or (pkm_detail[3] and pkm_detail[3] == 'bug'):
            has_bug = True
        elif pkm_detail[2] == 'dark' or (pkm_detail[3] and pkm_detail[3] == 'dark'):
            has_dark = True
        elif pkm_detail[2] == 'dragon' or (pkm_detail[3] and pkm_detail[3] == 'dragon'):
            has_dragon = True
        elif pkm_detail[2] == 'electric' or (pkm_detail[3] and pkm_detail[3] == 'electric'):
            has_electric = True
        elif pkm_detail[2] == 'fairy' or (pkm_detail[3] and pkm_detail[3] == 'fairy'):
            has_fairy = True
        elif pkm_detail[2] == 'fighting' or (pkm_detail[3] and pkm_detail[3] == 'fighting'):
            has_fighting = True
        elif pkm_detail[2] == 'fire' or (pkm_detail[3] and pkm_detail[3] == 'fire'):
            has_fire = True
        elif pkm_detail[2] == 'flying' or (pkm_detail[3] and pkm_detail[3] == 'flying'):
            has_flying = True
        elif pkm_detail[2] == 'ghost' or (pkm_detail[3] and pkm_detail[3] == 'ghost'):
            has_ghost = True
        elif pkm_detail[2] == 'grass' or (pkm_detail[3] and pkm_detail[3] == 'grass'):
            has_grass = True
        elif pkm_detail[2] == 'ground' or (pkm_detail[3] and pkm_detail[3] == 'ground'):
            has_ground = True
        elif pkm_detail[2] == 'ice' or (pkm_detail[3] and pkm_detail[3] == 'ice'):
            has_ice = True
        elif pkm_detail[2] == 'normal' or (pkm_detail[3] and pkm_detail[3] == 'normal'):
            has_normal = True
        elif pkm_detail[2] == 'poison' or (pkm_detail[3] and pkm_detail[3] == 'poison'):
            has_poison = True
        elif pkm_detail[2] == 'psychic' or (pkm_detail[3] and pkm_detail[3] == 'psychic'):
            has_psychic = True
        elif pkm_detail[2] == 'rock' or (pkm_detail[3] and pkm_detail[3] == 'rock'):
            has_rock = True
        elif pkm_detail[2] == 'steel' or (pkm_detail[3] and pkm_detail[3] == 'steel'):
            has_steel = True
        elif pkm_detail[2] == 'water' or (pkm_detail[3] and pkm_detail[3] == 'water'):
            has_water = True
        else:
            raise Exception(f"Invalid typing. Pokemon code is {pkm_code}")

        pkms.append(pkm)

    player_state = PlayerState(pkms=pkms,
                               has_bug=has_bug,
                               has_dark=has_dark,
                               has_dragon=has_dragon,
                               has_electric=has_electric,
                               has_fairy=has_fairy,
                               has_fighting=has_fighting,
                               has_fire=has_fire,
                               has_flying=has_flying,
                               has_ghost=has_ghost,
                               has_grass=has_grass,
                               has_ground=has_ground,
                               has_ice=has_ice,
                               has_normal=has_normal,
                               has_poison=has_poison,
                               has_psychic=has_psychic,
                               has_rock=has_rock,
                               has_steel=has_steel,
                               has_water=has_water)

    return player_state


def initiate_game_state(mysql_conn: MySQLConnector, p1_win: bool, player_pkm_list: list) -> GameState:
    # p1
    p1state = create_player_state(mysql_conn, player_pkm_list[0])
    # p2
    p2state = create_player_state(mysql_conn, player_pkm_list[1])

    return GameState(p1state, p2state, p1_win)


def ini_data_file(out_filepath: str):
    header_row = 'p1_win,T_ELECTRIC,T_GRASSY,T_MISTY,T_PSYCHIC,W_SUN,W_RAIN,W_SAND,W_SNOW,W_EX_SUN,W_EX_RAIN,W_EX_WIND,R_TRICK_ROOM,R_WONDER_ROOM,R_MAGIC_ROOM,p1_reflect,p1_light_screen,p1_tailwind,p1_webbed,p1_has_bug,p1_has_dark,p1_has_dragon,p1_has_electric,p1_has_fairy,p1_has_fighting,p1_has_fire,p1_has_flying,p1_has_ghost,p1_has_grass,p1_has_ground,p1_has_ice,p1_has_normal,p1_has_poison,p1_has_psychic,p1_has_rock,p1_has_steel,p1_has_water,p2_reflect,p2_light_screen,p2_tailwind,p2_webbed,p2_has_bug,p2_has_dark,p2_has_dragon,p2_has_electric,p2_has_fairy,p2_has_fighting,p2_has_fire,p2_has_flying,p2_has_ghost,p2_has_grass,p2_has_ground,p2_has_ice,p2_has_normal,p2_has_poison,p2_has_psychic,p2_has_rock,p2_has_steel,p2_has_water,p1_pkm1_hp,p1_pkm1_BURN,p1_pkm1_FREEZE,p1_pkm1_PARALYSIS,p1_pkm1_POISON,p1_pkm1_BADLY_POISON,p1_pkm1_SLEEP,p1_pkm1_volatile_status,p1_pkm1_atk_boost,p1_pkm1_def_boost,p1_pkm1_spa_boost,p1_pkm1_spd_boost,p1_pkm1_spe_boost,p1_pkm2_hp,p1_pkm2_BURN,p1_pkm2_FREEZE,p1_pkm2_PARALYSIS,p1_pkm2_POISON,p1_pkm2_BADLY_POISON,p1_pkm2_SLEEP,p1_pkm2_volatile_status,p1_pkm2_atk_boost,p1_pkm2_def_boost,p1_pkm2_spa_boost,p1_pkm2_spd_boost,p1_pkm2_spe_boost,p1_pkm3_hp,p1_pkm3_BURN,p1_pkm3_FREEZE,p1_pkm3_PARALYSIS,p1_pkm3_POISON,p1_pkm3_BADLY_POISON,p1_pkm3_SLEEP,p1_pkm3_volatile_status,p1_pkm3_atk_boost,p1_pkm3_def_boost,p1_pkm3_spa_boost,p1_pkm3_spd_boost,p1_pkm3_spe_boost,p1_pkm4_hp,p1_pkm4_BURN,p1_pkm4_FREEZE,p1_pkm4_PARALYSIS,p1_pkm4_POISON,p1_pkm4_BADLY_POISON,p1_pkm4_SLEEP,p1_pkm4_volatile_status,p1_pkm4_atk_boost,p1_pkm4_def_boost,p1_pkm4_spa_boost,p1_pkm4_spd_boost,p1_pkm4_spe_boost,p1_pkm5_hp,p1_pkm5_BURN,p1_pkm5_FREEZE,p1_pkm5_PARALYSIS,p1_pkm5_POISON,p1_pkm5_BADLY_POISON,p1_pkm5_SLEEP,p1_pkm5_volatile_status,p1_pkm5_atk_boost,p1_pkm5_def_boost,p1_pkm5_spa_boost,p1_pkm5_spd_boost,p1_pkm5_spe_boost,p1_pkm6_hp,p1_pkm6_BURN,p1_pkm6_FREEZE,p1_pkm6_PARALYSIS,p1_pkm6_POISON,p1_pkm6_BADLY_POISON,p1_pkm6_SLEEP,p1_pkm6_volatile_status,p1_pkm6_atk_boost,p1_pkm6_def_boost,p1_pkm6_spa_boost,p1_pkm6_spd_boost,p1_pkm6_spe_boost,p2_pkm1_hp,p2_pkm1_BURN,p2_pkm1_FREEZE,p2_pkm1_PARALYSIS,p2_pkm1_POISON,p2_pkm1_BADLY_POISON,p2_pkm1_SLEEP,p2_pkm1_volatile_status,p2_pkm1_atk_boost,p2_pkm1_def_boost,p2_pkm1_spa_boost,p2_pkm1_spd_boost,p2_pkm1_spe_boost,p2_pkm2_hp,p2_pkm2_BURN,p2_pkm2_FREEZE,p2_pkm2_PARALYSIS,p2_pkm2_POISON,p2_pkm2_BADLY_POISON,p2_pkm2_SLEEP,p2_pkm2_volatile_status,p2_pkm2_atk_boost,p2_pkm2_def_boost,p2_pkm2_spa_boost,p2_pkm2_spd_boost,p2_pkm2_spe_boost,p2_pkm3_hp,p2_pkm3_BURN,p2_pkm3_FREEZE,p2_pkm3_PARALYSIS,p2_pkm3_POISON,p2_pkm3_BADLY_POISON,p2_pkm3_SLEEP,p2_pkm3_volatile_status,p2_pkm3_atk_boost,p2_pkm3_def_boost,p2_pkm3_spa_boost,p2_pkm3_spd_boost,p2_pkm3_spe_boost,p2_pkm4_hp,p2_pkm4_BURN,p2_pkm4_FREEZE,p2_pkm4_PARALYSIS,p2_pkm4_POISON,p2_pkm4_BADLY_POISON,p2_pkm4_SLEEP,p2_pkm4_volatile_status,p2_pkm4_atk_boost,p2_pkm4_def_boost,p2_pkm4_spa_boost,p2_pkm4_spd_boost,p2_pkm4_spe_boost,p2_pkm5_hp,p2_pkm5_BURN,p2_pkm5_FREEZE,p2_pkm5_PARALYSIS,p2_pkm5_POISON,p2_pkm5_BADLY_POISON,p2_pkm5_SLEEP,p2_pkm5_volatile_status,p2_pkm5_atk_boost,p2_pkm5_def_boost,p2_pkm5_spa_boost,p2_pkm5_spd_boost,p2_pkm5_spe_boost,p2_pkm6_hp,p2_pkm6_BURN,p2_pkm6_FREEZE,p2_pkm6_PARALYSIS,p2_pkm6_POISON,p2_pkm6_BADLY_POISON,p2_pkm6_SLEEP,p2_pkm6_volatile_status,p2_pkm6_atk_boost,p2_pkm6_def_boost,p2_pkm6_spa_boost,p2_pkm6_spd_boost,p2_pkm6_spe_boost'
    with open(out_filepath, 'w') as gs_file:
        gs_file.write(f"{header_row}\n")


def game_state_to_file(out_filepath: str, data: GameState):
    with open(out_filepath, 'a') as gs_file:
        line = game_state_to_row(data)
        gs_file.write(f"{line}\n")

    print(f"Writing line to file {out_filepath}:")
    print(line)


def game_state_to_row(data: GameState):
    p1_win = int(data.p1_win)
    T_ELECTRIC = 1 if data.terrain == const.T_ELECTRIC else 0
    T_GRASSY = 1 if data.terrain == const.T_GRASSY else 0
    T_MISTY = 1 if data.terrain == const.T_MISTY else 0
    T_PSYCHIC = 1 if data.terrain == const.T_PSYCHIC else 0
    W_SUN = 1 if data.weather == const.W_SUN else 0
    W_RAIN = 1 if data.weather == const.W_RAIN else 0
    W_SAND = 1 if data.weather == const.W_SAND else 0
    W_SNOW = 1 if data.weather == const.W_SNOW else 0
    W_EX_SUN = 1 if data.weather == const.W_EX_SUN else 0
    W_EX_RAIN = 1 if data.weather == const.W_EX_RAIN else 0
    W_EX_WIND = 1 if data.weather == const.W_EX_WIND else 0
    R_TRICK_ROOM = 1 if data.room == const.R_TRICK_ROOM else 0
    R_WONDER_ROOM = 1 if data.room == const.R_WONDER_ROOM else 0
    R_MAGIC_ROOM = 1 if data.room == const.R_MAGIC_ROOM else 0
    p1_reflect = int(data.p1state.reflect)
    p1_light_screen = int(data.p1state.light_screen)
    p1_tailwind = int(data.p1state.tailwind)
    p1_webbed = int(data.p1state.webbed)
    p1_has_bug = int(data.p1state.has_bug)
    p1_has_dark = int(data.p1state.has_dark)
    p1_has_dragon = int(data.p1state.has_dragon)
    p1_has_electric = int(data.p1state.has_electric)
    p1_has_fairy = int(data.p1state.has_fairy)
    p1_has_fighting = int(data.p1state.has_fighting)
    p1_has_fire = int(data.p1state.has_fire)
    p1_has_flying = int(data.p1state.has_flying)
    p1_has_ghost = int(data.p1state.has_ghost)
    p1_has_grass = int(data.p1state.has_grass)
    p1_has_ground = int(data.p1state.has_ground)
    p1_has_ice = int(data.p1state.has_ice)
    p1_has_normal = int(data.p1state.has_normal)
    p1_has_poison = int(data.p1state.has_poison)
    p1_has_psychic = int(data.p1state.has_psychic)
    p1_has_rock = int(data.p1state.has_rock)
    p1_has_steel = int(data.p1state.has_steel)
    p1_has_water = int(data.p1state.has_water)
    p2_reflect = int(data.p2state.reflect)
    p2_light_screen = int(data.p2state.light_screen)
    p2_tailwind = int(data.p2state.tailwind)
    p2_webbed = int(data.p2state.webbed)
    p2_has_bug = int(data.p2state.has_bug)
    p2_has_dark = int(data.p2state.has_dark)
    p2_has_dragon = int(data.p2state.has_dragon)
    p2_has_electric = int(data.p2state.has_electric)
    p2_has_fairy = int(data.p2state.has_fairy)
    p2_has_fighting = int(data.p2state.has_fighting)
    p2_has_fire = int(data.p2state.has_fire)
    p2_has_flying = int(data.p2state.has_flying)
    p2_has_ghost = int(data.p2state.has_ghost)
    p2_has_grass = int(data.p2state.has_grass)
    p2_has_ground = int(data.p2state.has_ground)
    p2_has_ice = int(data.p2state.has_ice)
    p2_has_normal = int(data.p2state.has_normal)
    p2_has_poison = int(data.p2state.has_poison)
    p2_has_psychic = int(data.p2state.has_psychic)
    p2_has_rock = int(data.p2state.has_rock)
    p2_has_steel = int(data.p2state.has_steel)
    p2_has_water = int(data.p2state.has_water)
    p1_pkm1_hp = data.p1state.pkms[0].hp
    p1_pkm1_BURN = 1 if data.p1state.pkms[0].status_condition == const.BURN else 0
    p1_pkm1_FREEZE = 1 if data.p1state.pkms[0].status_condition == const.FREEZE else 0
    p1_pkm1_PARALYSIS = 1 if data.p1state.pkms[0].status_condition == const.PARALYSIS else 0
    p1_pkm1_POISON = 1 if data.p1state.pkms[0].status_condition == const.POISON else 0
    p1_pkm1_BADLY_POISON = 1 if data.p1state.pkms[0].status_condition == const.BADLY_POISON else 0
    p1_pkm1_SLEEP = 1 if data.p1state.pkms[0].status_condition == const.SLEEP else 0
    p1_pkm1_volatile_status = int(data.p1state.pkms[0].volatile_status)
    p1_pkm1_atk_boost = data.p1state.pkms[0].atk_boost
    p1_pkm1_def_boost = data.p1state.pkms[0].def_boost
    p1_pkm1_spa_boost = data.p1state.pkms[0].spa_boost
    p1_pkm1_spd_boost = data.p1state.pkms[0].spd_boost
    p1_pkm1_spe_boost = data.p1state.pkms[0].spe_boost
    p1_pkm2_hp = data.p1state.pkms[1].hp
    p1_pkm2_BURN = 1 if data.p1state.pkms[1].status_condition == const.BURN else 0
    p1_pkm2_FREEZE = 1 if data.p1state.pkms[1].status_condition == const.FREEZE else 0
    p1_pkm2_PARALYSIS = 1 if data.p1state.pkms[1].status_condition == const.PARALYSIS else 0
    p1_pkm2_POISON = 1 if data.p1state.pkms[1].status_condition == const.POISON else 0
    p1_pkm2_BADLY_POISON = 1 if data.p1state.pkms[1].status_condition == const.BADLY_POISON else 0
    p1_pkm2_SLEEP = 1 if data.p1state.pkms[1].status_condition == const.SLEEP else 0
    p1_pkm2_volatile_status = int(data.p1state.pkms[1].volatile_status)
    p1_pkm2_atk_boost = data.p1state.pkms[1].atk_boost
    p1_pkm2_def_boost = data.p1state.pkms[1].def_boost
    p1_pkm2_spa_boost = data.p1state.pkms[1].spa_boost
    p1_pkm2_spd_boost = data.p1state.pkms[1].spd_boost
    p1_pkm2_spe_boost = data.p1state.pkms[1].spe_boost
    p1_pkm3_hp = data.p1state.pkms[2].hp
    p1_pkm3_BURN = 1 if data.p1state.pkms[2].status_condition == const.BURN else 0
    p1_pkm3_FREEZE = 1 if data.p1state.pkms[2].status_condition == const.FREEZE else 0
    p1_pkm3_PARALYSIS = 1 if data.p1state.pkms[2].status_condition == const.PARALYSIS else 0
    p1_pkm3_POISON = 1 if data.p1state.pkms[2].status_condition == const.POISON else 0
    p1_pkm3_BADLY_POISON = 1 if data.p1state.pkms[2].status_condition == const.BADLY_POISON else 0
    p1_pkm3_SLEEP = 1 if data.p1state.pkms[2].status_condition == const.SLEEP else 0
    p1_pkm3_volatile_status = int(data.p1state.pkms[2].volatile_status)
    p1_pkm3_atk_boost = data.p1state.pkms[2].atk_boost
    p1_pkm3_def_boost = data.p1state.pkms[2].def_boost
    p1_pkm3_spa_boost = data.p1state.pkms[2].spa_boost
    p1_pkm3_spd_boost = data.p1state.pkms[2].spd_boost
    p1_pkm3_spe_boost = data.p1state.pkms[2].spe_boost
    p1_pkm4_hp = data.p1state.pkms[3].hp
    p1_pkm4_BURN = 1 if data.p1state.pkms[3].status_condition == const.BURN else 0
    p1_pkm4_FREEZE = 1 if data.p1state.pkms[3].status_condition == const.FREEZE else 0
    p1_pkm4_PARALYSIS = 1 if data.p1state.pkms[3].status_condition == const.PARALYSIS else 0
    p1_pkm4_POISON = 1 if data.p1state.pkms[3].status_condition == const.POISON else 0
    p1_pkm4_BADLY_POISON = 1 if data.p1state.pkms[3].status_condition == const.BADLY_POISON else 0
    p1_pkm4_SLEEP = 1 if data.p1state.pkms[3].status_condition == const.SLEEP else 0
    p1_pkm4_volatile_status = int(data.p1state.pkms[3].volatile_status)
    p1_pkm4_atk_boost = data.p1state.pkms[3].atk_boost
    p1_pkm4_def_boost = data.p1state.pkms[3].def_boost
    p1_pkm4_spa_boost = data.p1state.pkms[3].spa_boost
    p1_pkm4_spd_boost = data.p1state.pkms[3].spd_boost
    p1_pkm4_spe_boost = data.p1state.pkms[3].spe_boost
    p1_pkm5_hp = data.p1state.pkms[4].hp
    p1_pkm5_BURN = 1 if data.p1state.pkms[4].status_condition == const.BURN else 0
    p1_pkm5_FREEZE = 1 if data.p1state.pkms[4].status_condition == const.FREEZE else 0
    p1_pkm5_PARALYSIS = 1 if data.p1state.pkms[4].status_condition == const.PARALYSIS else 0
    p1_pkm5_POISON = 1 if data.p1state.pkms[4].status_condition == const.POISON else 0
    p1_pkm5_BADLY_POISON = 1 if data.p1state.pkms[4].status_condition == const.BADLY_POISON else 0
    p1_pkm5_SLEEP = 1 if data.p1state.pkms[4].status_condition == const.SLEEP else 0
    p1_pkm5_volatile_status = int(data.p1state.pkms[4].volatile_status)
    p1_pkm5_atk_boost = data.p1state.pkms[4].atk_boost
    p1_pkm5_def_boost = data.p1state.pkms[4].def_boost
    p1_pkm5_spa_boost = data.p1state.pkms[4].spa_boost
    p1_pkm5_spd_boost = data.p1state.pkms[4].spd_boost
    p1_pkm5_spe_boost = data.p1state.pkms[4].spe_boost
    p1_pkm6_hp = data.p1state.pkms[5].hp
    p1_pkm6_BURN = 1 if data.p1state.pkms[5].status_condition == const.BURN else 0
    p1_pkm6_FREEZE = 1 if data.p1state.pkms[5].status_condition == const.FREEZE else 0
    p1_pkm6_PARALYSIS = 1 if data.p1state.pkms[5].status_condition == const.PARALYSIS else 0
    p1_pkm6_POISON = 1 if data.p1state.pkms[5].status_condition == const.POISON else 0
    p1_pkm6_BADLY_POISON = 1 if data.p1state.pkms[5].status_condition == const.BADLY_POISON else 0
    p1_pkm6_SLEEP = 1 if data.p1state.pkms[5].status_condition == const.SLEEP else 0
    p1_pkm6_volatile_status = int(data.p1state.pkms[5].volatile_status)
    p1_pkm6_atk_boost = data.p1state.pkms[5].atk_boost
    p1_pkm6_def_boost = data.p1state.pkms[5].def_boost
    p1_pkm6_spa_boost = data.p1state.pkms[5].spa_boost
    p1_pkm6_spd_boost = data.p1state.pkms[5].spd_boost
    p1_pkm6_spe_boost = data.p1state.pkms[5].spe_boost
    p2_pkm1_hp = data.p2state.pkms[0].hp
    p2_pkm1_BURN = 1 if data.p2state.pkms[0].status_condition == const.BURN else 0
    p2_pkm1_FREEZE = 1 if data.p2state.pkms[0].status_condition == const.FREEZE else 0
    p2_pkm1_PARALYSIS = 1 if data.p2state.pkms[0].status_condition == const.PARALYSIS else 0
    p2_pkm1_POISON = 1 if data.p2state.pkms[0].status_condition == const.POISON else 0
    p2_pkm1_BADLY_POISON = 1 if data.p2state.pkms[0].status_condition == const.BADLY_POISON else 0
    p2_pkm1_SLEEP = 1 if data.p2state.pkms[0].status_condition == const.SLEEP else 0
    p2_pkm1_volatile_status = int(data.p2state.pkms[0].volatile_status)
    p2_pkm1_atk_boost = data.p2state.pkms[0].atk_boost
    p2_pkm1_def_boost = data.p2state.pkms[0].def_boost
    p2_pkm1_spa_boost = data.p2state.pkms[0].spa_boost
    p2_pkm1_spd_boost = data.p2state.pkms[0].spd_boost
    p2_pkm1_spe_boost = data.p2state.pkms[0].spe_boost
    p2_pkm2_hp = data.p2state.pkms[1].hp
    p2_pkm2_BURN = 1 if data.p2state.pkms[1].status_condition == const.BURN else 0
    p2_pkm2_FREEZE = 1 if data.p2state.pkms[1].status_condition == const.FREEZE else 0
    p2_pkm2_PARALYSIS = 1 if data.p2state.pkms[1].status_condition == const.PARALYSIS else 0
    p2_pkm2_POISON = 1 if data.p2state.pkms[1].status_condition == const.POISON else 0
    p2_pkm2_BADLY_POISON = 1 if data.p2state.pkms[1].status_condition == const.BADLY_POISON else 0
    p2_pkm2_SLEEP = 1 if data.p2state.pkms[1].status_condition == const.SLEEP else 0
    p2_pkm2_volatile_status = int(data.p2state.pkms[1].volatile_status)
    p2_pkm2_atk_boost = data.p2state.pkms[1].atk_boost
    p2_pkm2_def_boost = data.p2state.pkms[1].def_boost
    p2_pkm2_spa_boost = data.p2state.pkms[1].spa_boost
    p2_pkm2_spd_boost = data.p2state.pkms[1].spd_boost
    p2_pkm2_spe_boost = data.p2state.pkms[1].spe_boost
    p2_pkm3_hp = data.p2state.pkms[2].hp
    p2_pkm3_BURN = 1 if data.p2state.pkms[2].status_condition == const.BURN else 0
    p2_pkm3_FREEZE = 1 if data.p2state.pkms[2].status_condition == const.FREEZE else 0
    p2_pkm3_PARALYSIS = 1 if data.p2state.pkms[2].status_condition == const.PARALYSIS else 0
    p2_pkm3_POISON = 1 if data.p2state.pkms[2].status_condition == const.POISON else 0
    p2_pkm3_BADLY_POISON = 1 if data.p2state.pkms[2].status_condition == const.BADLY_POISON else 0
    p2_pkm3_SLEEP = 1 if data.p2state.pkms[2].status_condition == const.SLEEP else 0
    p2_pkm3_volatile_status = int(data.p2state.pkms[2].volatile_status)
    p2_pkm3_atk_boost = data.p2state.pkms[2].atk_boost
    p2_pkm3_def_boost = data.p2state.pkms[2].def_boost
    p2_pkm3_spa_boost = data.p2state.pkms[2].spa_boost
    p2_pkm3_spd_boost = data.p2state.pkms[2].spd_boost
    p2_pkm3_spe_boost = data.p2state.pkms[2].spe_boost
    p2_pkm4_hp = data.p2state.pkms[3].hp
    p2_pkm4_BURN = 1 if data.p2state.pkms[3].status_condition == const.BURN else 0
    p2_pkm4_FREEZE = 1 if data.p2state.pkms[3].status_condition == const.FREEZE else 0
    p2_pkm4_PARALYSIS = 1 if data.p2state.pkms[3].status_condition == const.PARALYSIS else 0
    p2_pkm4_POISON = 1 if data.p2state.pkms[3].status_condition == const.POISON else 0
    p2_pkm4_BADLY_POISON = 1 if data.p2state.pkms[3].status_condition == const.BADLY_POISON else 0
    p2_pkm4_SLEEP = 1 if data.p2state.pkms[3].status_condition == const.SLEEP else 0
    p2_pkm4_volatile_status = int(data.p2state.pkms[3].volatile_status)
    p2_pkm4_atk_boost = data.p2state.pkms[3].atk_boost
    p2_pkm4_def_boost = data.p2state.pkms[3].def_boost
    p2_pkm4_spa_boost = data.p2state.pkms[3].spa_boost
    p2_pkm4_spd_boost = data.p2state.pkms[3].spd_boost
    p2_pkm4_spe_boost = data.p2state.pkms[3].spe_boost
    p2_pkm5_hp = data.p2state.pkms[4].hp
    p2_pkm5_BURN = 1 if data.p2state.pkms[4].status_condition == const.BURN else 0
    p2_pkm5_FREEZE = 1 if data.p2state.pkms[4].status_condition == const.FREEZE else 0
    p2_pkm5_PARALYSIS = 1 if data.p2state.pkms[4].status_condition == const.PARALYSIS else 0
    p2_pkm5_POISON = 1 if data.p2state.pkms[4].status_condition == const.POISON else 0
    p2_pkm5_BADLY_POISON = 1 if data.p2state.pkms[4].status_condition == const.BADLY_POISON else 0
    p2_pkm5_SLEEP = 1 if data.p2state.pkms[4].status_condition == const.SLEEP else 0
    p2_pkm5_volatile_status = int(data.p2state.pkms[4].volatile_status)
    p2_pkm5_atk_boost = data.p2state.pkms[4].atk_boost
    p2_pkm5_def_boost = data.p2state.pkms[4].def_boost
    p2_pkm5_spa_boost = data.p2state.pkms[4].spa_boost
    p2_pkm5_spd_boost = data.p2state.pkms[4].spd_boost
    p2_pkm5_spe_boost = data.p2state.pkms[4].spe_boost
    p2_pkm6_hp = data.p2state.pkms[5].hp
    p2_pkm6_BURN = 1 if data.p2state.pkms[5].status_condition == const.BURN else 0
    p2_pkm6_FREEZE = 1 if data.p2state.pkms[5].status_condition == const.FREEZE else 0
    p2_pkm6_PARALYSIS = 1 if data.p2state.pkms[5].status_condition == const.PARALYSIS else 0
    p2_pkm6_POISON = 1 if data.p2state.pkms[5].status_condition == const.POISON else 0
    p2_pkm6_BADLY_POISON = 1 if data.p2state.pkms[5].status_condition == const.BADLY_POISON else 0
    p2_pkm6_SLEEP = 1 if data.p2state.pkms[5].status_condition == const.SLEEP else 0
    p2_pkm6_volatile_status = int(data.p2state.pkms[5].volatile_status)
    p2_pkm6_atk_boost = data.p2state.pkms[5].atk_boost
    p2_pkm6_def_boost = data.p2state.pkms[5].def_boost
    p2_pkm6_spa_boost = data.p2state.pkms[5].spa_boost
    p2_pkm6_spd_boost = data.p2state.pkms[5].spd_boost
    p2_pkm6_spe_boost = data.p2state.pkms[5].spe_boost

    return f"{p1_win},{T_ELECTRIC},{T_GRASSY},{T_MISTY},{T_PSYCHIC},{W_SUN},{W_RAIN},{W_SAND},{W_SNOW},{W_EX_SUN},{W_EX_RAIN},{W_EX_WIND},{R_TRICK_ROOM},{R_WONDER_ROOM},{R_MAGIC_ROOM},{p1_reflect},{p1_light_screen},{p1_tailwind},{p1_webbed},{p1_has_bug},{p1_has_dark},{p1_has_dragon},{p1_has_electric},{p1_has_fairy},{p1_has_fighting},{p1_has_fire},{p1_has_flying},{p1_has_ghost},{p1_has_grass},{p1_has_ground},{p1_has_ice},{p1_has_normal},{p1_has_poison},{p1_has_psychic},{p1_has_rock},{p1_has_steel},{p1_has_water},{p2_reflect},{p2_light_screen},{p2_tailwind},{p2_webbed},{p2_has_bug},{p2_has_dark},{p2_has_dragon},{p2_has_electric},{p2_has_fairy},{p2_has_fighting},{p2_has_fire},{p2_has_flying},{p2_has_ghost},{p2_has_grass},{p2_has_ground},{p2_has_ice},{p2_has_normal},{p2_has_poison},{p2_has_psychic},{p2_has_rock},{p2_has_steel},{p2_has_water},{p1_pkm1_hp},{p1_pkm1_BURN},{p1_pkm1_FREEZE},{p1_pkm1_PARALYSIS},{p1_pkm1_POISON},{p1_pkm1_BADLY_POISON},{p1_pkm1_SLEEP},{p1_pkm1_volatile_status},{p1_pkm1_atk_boost},{p1_pkm1_def_boost},{p1_pkm1_spa_boost},{p1_pkm1_spd_boost},{p1_pkm1_spe_boost},{p1_pkm2_hp},{p1_pkm2_BURN},{p1_pkm2_FREEZE},{p1_pkm2_PARALYSIS},{p1_pkm2_POISON},{p1_pkm2_BADLY_POISON},{p1_pkm2_SLEEP},{p1_pkm2_volatile_status},{p1_pkm2_atk_boost},{p1_pkm2_def_boost},{p1_pkm2_spa_boost},{p1_pkm2_spd_boost},{p1_pkm2_spe_boost},{p1_pkm3_hp},{p1_pkm3_BURN},{p1_pkm3_FREEZE},{p1_pkm3_PARALYSIS},{p1_pkm3_POISON},{p1_pkm3_BADLY_POISON},{p1_pkm3_SLEEP},{p1_pkm3_volatile_status},{p1_pkm3_atk_boost},{p1_pkm3_def_boost},{p1_pkm3_spa_boost},{p1_pkm3_spd_boost},{p1_pkm3_spe_boost},{p1_pkm4_hp},{p1_pkm4_BURN},{p1_pkm4_FREEZE},{p1_pkm4_PARALYSIS},{p1_pkm4_POISON},{p1_pkm4_BADLY_POISON},{p1_pkm4_SLEEP},{p1_pkm4_volatile_status},{p1_pkm4_atk_boost},{p1_pkm4_def_boost},{p1_pkm4_spa_boost},{p1_pkm4_spd_boost},{p1_pkm4_spe_boost},{p1_pkm5_hp},{p1_pkm5_BURN},{p1_pkm5_FREEZE},{p1_pkm5_PARALYSIS},{p1_pkm5_POISON},{p1_pkm5_BADLY_POISON},{p1_pkm5_SLEEP},{p1_pkm5_volatile_status},{p1_pkm5_atk_boost},{p1_pkm5_def_boost},{p1_pkm5_spa_boost},{p1_pkm5_spd_boost},{p1_pkm5_spe_boost},{p1_pkm6_hp},{p1_pkm6_BURN},{p1_pkm6_FREEZE},{p1_pkm6_PARALYSIS},{p1_pkm6_POISON},{p1_pkm6_BADLY_POISON},{p1_pkm6_SLEEP},{p1_pkm6_volatile_status},{p1_pkm6_atk_boost},{p1_pkm6_def_boost},{p1_pkm6_spa_boost},{p1_pkm6_spd_boost},{p1_pkm6_spe_boost},{p2_pkm1_hp},{p2_pkm1_BURN},{p2_pkm1_FREEZE},{p2_pkm1_PARALYSIS},{p2_pkm1_POISON},{p2_pkm1_BADLY_POISON},{p2_pkm1_SLEEP},{p2_pkm1_volatile_status},{p2_pkm1_atk_boost},{p2_pkm1_def_boost},{p2_pkm1_spa_boost},{p2_pkm1_spd_boost},{p2_pkm1_spe_boost},{p2_pkm2_hp},{p2_pkm2_BURN},{p2_pkm2_FREEZE},{p2_pkm2_PARALYSIS},{p2_pkm2_POISON},{p2_pkm2_BADLY_POISON},{p2_pkm2_SLEEP},{p2_pkm2_volatile_status},{p2_pkm2_atk_boost},{p2_pkm2_def_boost},{p2_pkm2_spa_boost},{p2_pkm2_spd_boost},{p2_pkm2_spe_boost},{p2_pkm3_hp},{p2_pkm3_BURN},{p2_pkm3_FREEZE},{p2_pkm3_PARALYSIS},{p2_pkm3_POISON},{p2_pkm3_BADLY_POISON},{p2_pkm3_SLEEP},{p2_pkm3_volatile_status},{p2_pkm3_atk_boost},{p2_pkm3_def_boost},{p2_pkm3_spa_boost},{p2_pkm3_spd_boost},{p2_pkm3_spe_boost},{p2_pkm4_hp},{p2_pkm4_BURN},{p2_pkm4_FREEZE},{p2_pkm4_PARALYSIS},{p2_pkm4_POISON},{p2_pkm4_BADLY_POISON},{p2_pkm4_SLEEP},{p2_pkm4_volatile_status},{p2_pkm4_atk_boost},{p2_pkm4_def_boost},{p2_pkm4_spa_boost},{p2_pkm4_spd_boost},{p2_pkm4_spe_boost},{p2_pkm5_hp},{p2_pkm5_BURN},{p2_pkm5_FREEZE},{p2_pkm5_PARALYSIS},{p2_pkm5_POISON},{p2_pkm5_BADLY_POISON},{p2_pkm5_SLEEP},{p2_pkm5_volatile_status},{p2_pkm5_atk_boost},{p2_pkm5_def_boost},{p2_pkm5_spa_boost},{p2_pkm5_spd_boost},{p2_pkm5_spe_boost},{p2_pkm6_hp},{p2_pkm6_BURN},{p2_pkm6_FREEZE},{p2_pkm6_PARALYSIS},{p2_pkm6_POISON},{p2_pkm6_BADLY_POISON},{p2_pkm6_SLEEP},{p2_pkm6_volatile_status},{p2_pkm6_atk_boost},{p2_pkm6_def_boost},{p2_pkm6_spa_boost},{p2_pkm6_spd_boost},{p2_pkm6_spe_boost}"
