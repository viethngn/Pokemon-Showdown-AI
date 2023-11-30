from src.entities.pokemon import Pokemon


class PlayerState:

    def __init__(self,
                 pkm1: Pokemon,
                 pkm2: Pokemon,
                 pkm3: Pokemon,
                 pkm4: Pokemon,
                 pkm5: Pokemon,
                 pkm6: Pokemon,
                 reflect=False,
                 light_screen=False,
                 tailwind=False,
                 webbed=False):
        self.reflect = reflect
        self.light_screen = light_screen
        self.tailwind = tailwind
        self.webbed = webbed
        self.pkm1 = pkm1
        self.pkm2 = pkm2
        self.pkm3 = pkm3
        self.pkm4 = pkm4
        self.pkm5 = pkm5
        self.pkm6 = pkm6
