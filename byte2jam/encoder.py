import midi
import constants
from schema import Note, ByteJamSchema
from utils import get_nibble_note_data

def encode(data):
    """
    Encodes values into a MIDI pattern that is returned. Call midi.writemidifile
    on the pattern to save to disc.
    """
    # need something to work with
    try:
        values = bytearray(data)
    except e:
        return None

    # get header data from first byte of values
    initial_note_index = values[0] >> 5
    modal_index = (values[0] >> 2) & 7
    seq_index = values[0] & 3

    initial_note = constants.INITIAL_NOTE[initial_note_index]
    mode = constants.MODES[modal_index]

    content_notes = []

    # get note data from each succeeding byte
    for byte in values[1:]:
        content_notes.extend([
            Note(*get_nibble_note_data(byte >> 4, initial_note, mode)),
            Note(*get_nibble_note_data(byte & 15, initial_note, mode))
            ])

    # create note schema from extracted byte data
    schema = ByteJamSchema(initial_note_index, modal_index, seq_index, content_notes)
    return schema.get_midi_pattern()

def decode(pattern):
    """ Decodes values from a well formed MIDI pattern. Returns a bytearray bit string. """
    # extract the padding data
    notes = []
    for event in pattern[0]:
        if type(event) is midi.events.NoteOffEvent:
            notes.append(Note(event.pitch, event.tick == constants.HALF_NOTE_LENGTH))

    # get key
    initial_note = notes[0]

    # extract schemas from note sequence: mode from scale and intro sequence
    scale = sorted(notes[1:4] + notes[-4:], key=lambda x: x.pitch)
    mode = tuple([x.get_displacement(initial_note) for x in scale])
    sequence = tuple([x.modal_position(scale) for x in notes[:4]])

    try:
        initial_note_index = constants.INITIAL_NOTE.index(initial_note.pitch)
        modal_index = constants.MODES.index(mode)
        sequence_index = constants.INTRO_SEQUENCE.index(sequence)
    except ValueError:
        # One of the flag criteria do not match the schema layout, invalid sequence
        return None

    schema = ByteJamSchema(initial_note_index, modal_index, sequence_index, notes[4:-4])
    return schema.get_bytearray(scale)
