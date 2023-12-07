from src.const.ps_constants import W_NONE, T_NONE, R_NONE
from src.entities.player_state import PlayerState


class GameState:

    def __init__(self,
                 p1state: PlayerState,
                 p2state: PlayerState,
                 p1_win: bool,
                 weather=W_NONE,
                 terrain=T_NONE,
                 room=R_NONE):
        self.p1state = p1state
        self.p2state = p2state
        self.weather = weather
        self.terrain = terrain
        self.room = room
        self.p1_win = p1_win
