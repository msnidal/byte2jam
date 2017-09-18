import midi
from utils import map_note, get_note_events
from constants import *

class ByteJamSchema:
    """ This schema decode is intended to be a generalized encoder/decoder from bytearrays to MIDI. While currently functional it can be
    extended in the future with additional constructors and encoders to handle arbitrary schemas. """
    initial_note = None
    mode = None
    sequence = None
    content_notes = []

    def __init__(self, initial_note, mode, sequence, content_notes):
        self.initial_note = initial_note
        self.mode = mode
        self.sequence = sequence
        self.content_notes = content_notes

    def get_bytearray(self, scale):
        """ Returns a byte string from the schema class, ordered according to the conventions defined in constants.py """
        li = []

        header = (self.initial_note << 5) | (self.mode << 2) | self.sequence
        li.append(header)

        for byte_index in xrange((len(self.content_notes) // 2) + (len(self.content_notes) % 2)):
            byte = (self.content_notes[2*byte_index].modal_position(scale) << 5) | (self.content_notes[2*byte_index].is_half_note << 4)
            if len(self.content_notes) > (2*byte_index + 1):
                byte |= ((self.content_notes[2*byte_index + 1].modal_position(scale) << 1) | (self.content_notes[2*byte_index + 1].is_half_note))

            li.append(byte)

        return bytearray(li)

    def get_midi_pattern(self):
        """ Returns a MIDI pattern according to this object's schema. See constants.py for sequences. """
        # create midi file
        pattern = midi.Pattern()
        track = midi.Track()
        pattern.append(track)

        note_events = []

        # insert intro pad sequence from seq_index
        note_events.append(get_note_events(Note(map_note(self.initial_note, self.mode, INTRO_SEQUENCE[self.sequence][0]), False), 0))
        note_events.append(get_note_events(Note(map_note(self.initial_note, self.mode, INTRO_SEQUENCE[self.sequence][1]), True), 0))
        note_events.append(get_note_events(Note(map_note(self.initial_note, self.mode, INTRO_SEQUENCE[self.sequence][2]), True), 0))
        note_events.append(get_note_events(Note(map_note(self.initial_note, self.mode, INTRO_SEQUENCE[self.sequence][3]), False), 0))

        # populate content
        for note in self.content_notes:
            note_events.append(get_note_events(note, 0))

        # insert terminal pad sequence from seq_index
        note_events.append(get_note_events(Note(map_note(self.initial_note, self.mode, TERMINAL_SEQUENCE[self.sequence][0]), False), 0))
        note_events.append(get_note_events(Note(map_note(self.initial_note, self.mode, TERMINAL_SEQUENCE[self.sequence][1]), True), 0))
        note_events.append(get_note_events(Note(map_note(self.initial_note, self.mode, TERMINAL_SEQUENCE[self.sequence][2]), True), 0))
        note_events.append(get_note_events(Note(map_note(self.initial_note, self.mode, TERMINAL_SEQUENCE[self.sequence][3]), False), 0))

        # append everything in note_events
        for on, off in note_events:
            track.append(on)
            track.append(off)

        track.append(midi.EndOfTrackEvent(tick=0))
        return pattern

class Note:
    """ This class describes a musical note. It comprises an absolute pitch (in
    semi-tones) and a length datum. """
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
