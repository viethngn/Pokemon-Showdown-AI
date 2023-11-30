from src.const.ps_constants import W_NONE, T_NONE
from src.entities.player_state import PlayerState


class GameState:

    def __init__(self,
                 p1state: PlayerState,
                 p2state: PlayerState,
                 weather=W_NONE,
                 terrain=T_NONE):
        self.p1state = p1state
        self.p2state = p2state
        self.weather = weather
        self.terrain = terrain
