import abjad
from . import constants

def map_note(initial_note, mode, relative_position):
    """ Maps a MIDI note from an initial value, a mode, and a displacement on that mode """
    # relative displacement from 0 to 6, for each note in the mode.
    octave = relative_position // 7
    bounded_position = relative_position % 7

    return initial_note + mode[bounded_position] + 12 * octave

def get_note_events(note, start_delay):
    """ Gets a tuple of MIDI events to start and stop playing a note for a pitch """
    note_tuple = (1, 4) if note.is_half_note else (1, 8)

    return abjad.Note(note.pitch, note_tuple)

def get_nibble_note_data(nibble, initial_note, mode):
    """ Get a note data in the sequence from a nibble (half-byte) """

    relative_position = nibble >> 1
    is_half_note = nibble & 1
    pitch = map_note(initial_note, mode, relative_position)

    return pitch, is_half_note
