import midi
from schema import Note, ByteJamSchema
from utils import map_note
from constants import *

def get_nibble_note(nibble, initial_note, mode):
    """ Get a note in the sequence from a nibble (half-byte) """

    relative_position = nibble >> 1
    is_half_note = nibble & 1
    pitch = map_note(initial_note, mode, relative_position)

    return Note(pitch, is_half_note)

def encode(values):
    """
    Encodes values into a MIDI pattern that is returned. Call midi.writemidifile
    on the pattern to save to disc.
    """
    # need something to work with
    if type(values) != bytearray:
        return None

    # get header data from first byte of values
    initial_note = INITIAL_NOTE[(values[0] >> 5)]
    mode = (values[0] >> 2) & 7
    seq_index = values[0] & 3

    content_notes = []

    # get note data from each succeeding byte
    for byte in values[1:]:
        content_notes.extend([
            get_nibble_note(byte >> 4, initial_note, mode),
            get_nibble_note(byte & 15, initial_note, mode)
            ])

    # create note schema from extracted byte data
    schema = ByteJamSchema(initial_note, mode, seq_index, content_notes)
    return schema.get_midi_pattern()
    # midi.write_midifile("output.mid", pattern)

def decode(pattern):
    """ Decodes values from a well formed MIDI pattern. Returns a bytearray bit string. """
    # extract the padding data
    notes = []
    for event in pattern[0]:
        if type(event) is midi.events.NoteOffEvent:
            notes.append(Note(event.pitch, event.tick == HALF_NOTE_LENGTH))

    # get key
    initial_note = notes[0]

    # extract schemas from note sequence: mode from scale and intro sequence
    scale = sorted(notes[1:4] + notes[-4:], key=lambda x: x.pitch)
    mode = map(lambda x: x.get_displacement(initial_note), scale)
    sequence = map(lambda x: x.modal_position(scale), notes[:4])

    mode_index = None
    sequence_index = None
    initial_note_index = None

    try:
        initial_note_index = INITIAL_NOTE.index(initial_note.pitch)
        mode_index = MODES.index(mode)
        sequence_index = INTRO_SEQUENCE.index(sequence)
    except ValueError:
        # One of the flag criteria do not match the schema layout, invalid sequence
        return None

    schema = ByteJamSchema(initial_note_index, mode_index, sequence_index, notes[4:-4])
    return schema.get_bytearray(scale)
