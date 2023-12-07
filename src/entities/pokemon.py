from src.const.ps_constants import NO_STATUS


class Pokemon:

    def __init__(self, pkm_id, pkm_code,
                 in_battle=False,
                 hp=100,
                 status_condition=NO_STATUS,
                 volatile_status=False,
                 atk_boost=0,
                 def_boost=0,
                 spa_boost=0,
                 spd_boost=0,
                 spe_boost=0):
        self.pkm_id = pkm_id
        self.pkm_code = pkm_code
        self.hp = hp
        self.in_battle = in_battle
        self.status_condition = status_condition
        self.volatile_status = volatile_status
        self.atk_boost = atk_boost
        self.def_boost = def_boost
        self.spa_boost = spa_boost
        self.spd_boost = spd_boost
        self.spe_boost = spe_boost

