# constants for static data
PKD = 'pokedex'
MVD = 'movedex'
LS = 'learn sets'
TC = 'type chart'
AB = 'abilities'
ITM = 'items'

# constants for learn sets
"""
L = Level up
T = Move tutor
M = TM/HM
S = Event only
V = Virtual console from Gen 1
E = Egg move
"""
LVL = 'L'
TUTOR = 'T'
TM = 'M'
EVENT = 'S'
VCON = 'V'
EGG = 'E'
LS_CODE = [LVL, TUTOR, TM, EVENT, VCON, EGG]

# constants for move effectiveness
NORMAL_EF = (0, 1)
SUPER_EF = (1, 2)
LESS_EF = (2, 0.5)
NO_EF = (3, 0)

# constants for list of types
PKM_TYPES = ["bug","dark","dragon","electric","fairy","fighting","fire","flying","ghost","grass","ground","ice","normal","poison","psychic","rock","steel","water"]

# constants for insert to MySQL datatype
PS_REPLAY = 'ps_replay'
PS_RDETAILS = 'ps_replay_detail'
PS_PLAYER = 'ps_player'

# write file mode & output type
JSON = 'json'
CSV = 'csv'
SQL = 'sql'
MYSQL = 'mysql'

# Status Conditions
NO_STATUS = 0
BURN = 1
FREEZE = 2
PARALYSIS = 3
POISON = 4
BADLY_POISON = 5
SLEEP = 6

# Terrain
T_NONE = 0
T_ELECTRIC = 1
T_GRASSY = 2
T_MISTY = 3
T_PSYCHIC = 4

# Weather
W_NONE = 0
W_SUN = 1
W_RAIN = 2
W_SAND = 3
W_SNOW = 4
W_EX_SUN = 5
W_EX_RAIN = 6
W_EX_WIND = 7

# Room effect
R_NONE = 0
R_TRICK_ROOM = 1
R_WONDER_ROOM = 2
R_MAGIC_ROOM = 3
