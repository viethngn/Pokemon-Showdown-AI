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

# constants for insert toe MySQL datatype
PS_REPLAY = 'ps_replay'
PS_RDETAILS = 'ps_replay_detail'
PS_PLAYER = 'ps_player'

# write file mode & output type
JSON = 'json'
CSV = 'csv'
SQL = 'sql'
MYSQL = 'mysql'
