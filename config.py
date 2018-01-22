""" config / constant variables """

# --- FRAME RELATED ---

# maximum size of each frame ( unit : byte )
FRAME_SIZES = [
    160000,
    640000,
    1280000,
    2560000,
    10240000,
    100000000000000,
]

# default value of how many frames will output image will be composed of
DEFAULT_N_FRAMES = 50

# default compress level ( to choose frame size )
DEFAULT_COMPRESS_LEVEL = 3


# --- PARTICLE RELATED ---

# number of particles that will decorate output
PARTICLE_NUMBERS = [
    50,
    250,
    500,
    1000,
    2000,
    5000,
]

# number of lanes that will decorate output
LANE_NUMBERS = [
    10,
    50,
    100,
    200,
    400,
    1000,
]

# default density level for PARTICLE_NUMBERS or LANE_NUMBERS
DEFAULT_DENSITY_LEVEL = 3

# possible particle types
PARTICLE_TYPES = [
    'SNOW',
]

# default particle type
DEFAULT_PARTICLE_TYPE = 'SNOW'

# particle speed levels (x_min, x_max, y_min, y_max)
SPEED_LEVELS = [
    (-2, 2, 1, 2),
    (-2, 2, 1, 3),
    (-2, 2, 2, 3),
    (-2, 2, 2, 5),
    (-2, 2, 2, 8),
    (-2, 2, 3, 15),
]

# default particle speed level for SPEED_LEVELS
DEFAULT_SPEED_LEVEL = 3

# particle size levels ( min, max )
SIZE_LEVELS = [
    (1, 3),
    (1, 5),
    (1, 7),
    (1, 10),
    (3, 10),
    (5, 15),
]

# default particle size level for SIZE_LEVELS
DEFAULT_SIZE_LEVEL = 3




