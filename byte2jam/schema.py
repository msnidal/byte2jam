import midi
import constants
from utils import map_note, get_note_events

class ByteJamSchema:
    """
    This schema decode is intended to be a generalized encoder/decoder from bytearrays
    to MIDI. While currently functional it can be extended in the future with additional
    constructors and encoders to handle arbitrary schemas.
    """
    def __init__(self, initial_note_index, modal_index, sequence, content_notes):
        self.initial_note_index = initial_note_index
        self.modal_index = modal_index
        self.sequence = sequence
        self.content_notes = content_notes

    def get_bytearray(self, scale):
        """
        Returns a byte string from the schema class, ordered according to the
        conventions defined in constants.py
        """
        li = []

        header = (self.initial_note_index << 5) | (self.modal_index << 2) | self.sequence
        li.append(header)

        number_of_bytes = len(self.content_notes) // 2 + len(self.content_notes) % 2
        for byte_index in xrange(number_of_bytes):
            byte = (self.content_notes[2 * byte_index].modal_position(scale) << 5) | \
                    (self.content_notes[2 * byte_index].is_half_note << 4)
            if (2 * byte_index + 1) < len(self.content_notes):
                byte |= ((self.content_notes[2 * byte_index + 1].modal_position(scale) << 1) | \
                        (self.content_notes[2 * byte_index + 1].is_half_note))

            li.append(byte)

        return bytearray(li)

    def get_midi_pattern(self):
        """
        Returns a MIDI pattern according to this object's schema. See constants.py
        for sequences.
        """
        # create midi file
        pattern = midi.Pattern()
        track = midi.Track()
        pattern.append(track)

        note_events = []

        # insert intro pad sequence from seq_index
        for sequence_index in xrange(4):
            intro_note = Note(map_note(
                constants.INITIAL_NOTE[self.initial_note_index],
                constants.MODES[self.modal_index],
                constants.INTRO_SEQUENCE[self.sequence][sequence_index]), False)
            note_events.append(get_note_events(intro_note, 0))

        # populate content
        for note in self.content_notes:
            note_events.append(get_note_events(note, 0))

        # insert terminal pad sequence from seq_index
        for sequence_index in xrange(4):
            outro_note = Note(map_note(
                constants.INITIAL_NOTE[self.initial_note_index],
                constants.MODES[self.modal_index],
                constants.TERMINAL_SEQUENCE[self.sequence][sequence_index]), False)
            note_events.append(get_note_events(outro_note, 0))

        # append everything in note_events
        for on, off in note_events:
            track.append(on)
            track.append(off)

        track.append(midi.EndOfTrackEvent(tick=0))
        return pattern

class Note:
    """
    This class describes a musical note. It comprises an absolute pitch (in
    semi-tones) and a length datum.
    """
    pitch = None
    is_half_note = None

    def __init__(self, pitch, is_half_note):
        self.pitch = pitch
        self.is_half_note = is_half_note

    def get_displacement(self, initial_note):
        """ Returns the relative displacement of the note according to a key """
        return self.pitch - initial_note.pitch

    def modal_position(self, scale):
        """ Returns the position in a modal sequence (scale) of the note. """
        mode_position = False
        for index, note in enumerate(scale):
            if (self.pitch % 12) == (note.pitch % 12):
                mode_position = index + ((self.pitch - note.pitch) // 12)*7
        return mode_position
