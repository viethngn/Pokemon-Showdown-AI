from src.entities.pokemon import Pokemon


class PlayerState:

    def __init__(self,
                 pkms: list[Pokemon],
                 reflect=False,
                 light_screen=False,
                 tailwind=False,
                 webbed=False,
                 has_bug=False,
                 has_dark=False,
                 has_dragon=False,
                 has_electric=False,
                 has_fairy=False,
                 has_fighting=False,
                 has_fire=False,
                 has_flying=False,
                 has_ghost=False,
                 has_grass=False,
                 has_ground=False,
                 has_ice=False,
                 has_normal=False,
                 has_poison=False,
                 has_psychic=False,
                 has_rock=False,
                 has_steel=False,
                 has_water=False):
        self.reflect = reflect
        self.light_screen = light_screen
        self.tailwind = tailwind
        self.webbed = webbed
        self.pkms = pkms
        self.has_bug = has_bug
        self.has_dark = has_dark
        self.has_dragon = has_dragon
        self.has_electric = has_electric
        self.has_fairy = has_fairy
        self.has_fighting = has_fighting
        self.has_fire = has_fire
        self.has_flying = has_flying
        self.has_ghost = has_ghost
        self.has_grass = has_grass
        self.has_ground = has_ground
        self.has_ice = has_ice
        self.has_normal = has_normal
        self.has_poison = has_poison
        self.has_psychic = has_psychic
        self.has_rock = has_rock
        self.has_steel = has_steel
        self.has_water = has_water
