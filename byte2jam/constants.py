from midi import *

# note lengths, velocity according to midi library
HALF_NOTE_LENGTH = 100
FULL_NOTE_LENGTH = HALF_NOTE_LENGTH * 2
NOTE_VELOCITY = 20

# sequence sets in powers of 2
INITIAL_NOTE = (
    C_4, Cs_4, D_4, F_4,
    Fs_4, G_4, A_4, B_4
)

INTRO_SEQUENCE = (
    (0, 1, 3, 6),
    (0, 2, 1, 5),
    (0, 2, 5, 3),
    (0, 6, 2, 5),
)

TERMINAL_SEQUENCE = (
    (5, 2, 4, 0),
    (6, 3, 4, 0),
    (6, 1, 4, 0),
    (1, 3, 4, 0),
)

MODES = (
    (0, 2, 4, 5, 7, 9, 11),  # ionian
    (0, 2, 3, 5, 7, 9, 10),  # dorian
    (0, 1, 3, 5, 7, 8, 10),  # phrygian
    (0, 2, 4, 6, 7, 9, 11),  # lydian
    (0, 2, 4, 5, 7, 9, 10),  # mixolydian
    (0, 2, 3, 5, 7, 8, 10),  # aeolian
    (0, 1, 3, 5, 6, 8, 10),  # locrian
    (0, 1, 2, 4, 6, 8, 10),  # bragian (new mode) 
)
