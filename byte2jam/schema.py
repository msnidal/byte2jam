import abjad
from byte2jam import constants, utils

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

        self.scale = [Note(utils.map_note(
            constants.INITIAL_NOTE[initial_note_index],
            constants.MODES[modal_index],
            x), False) for x in range(7)]

    @classmethod
    def from_bytes(cls, data):
        """
        Encodes values into a MIDI pattern that is returned. Call midi.writemidifile
        on the pattern to save to disc.
        """
        # need something to work with
        try:
            values = bytes(data)
        except TypeError:
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
                Note(*utils.get_nibble_note_data(byte >> 4, initial_note, mode)),
                Note(*utils.get_nibble_note_data(byte & 15, initial_note, mode))
                ])

        # create note schema from extracted byte data
        return cls(initial_note_index, modal_index, seq_index, content_notes)

    @classmethod
    def from_model(cls, lilypond_file):
        """ Decodes values from a lilypond file pattern. Returns a bytearray bit string. """
        pattern = lilypond_file['score'].items[0]

        # extract the padding data
        notes = []
        for note in pattern[0]:
            notes.append(Note(note.written_pitch.number,
                note.written_duration.pair == (1,4)))

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

        return cls(initial_note_index, modal_index, sequence_index, notes[4:-4])

    def __bytes__(self):
        """
        Returns a byte string from the schema class, ordered according to the
        conventions defined in constants.py
        """
        li = []

        header = (self.initial_note_index << 5) | (self.modal_index << 2) | self.sequence
        li.append(header)

        number_of_bytes = len(self.content_notes) // 2 + len(self.content_notes) % 2

        for byte_index in range(number_of_bytes):
            byte = (self.content_notes[2 * byte_index].modal_position(self.scale) << 5) | \
                    (self.content_notes[2 * byte_index].is_half_note << 4)
            if (2 * byte_index + 1) < len(self.content_notes):
                byte |= ((self.content_notes[2 * byte_index + 1].modal_position(self.scale) << 1) | \
                        (self.content_notes[2 * byte_index + 1].is_half_note))

            li.append(byte)

        return bytes(li)

    def get_model(self):
        """
        Returns an abjad model according to this object's schema. See constants.py
        for sequences.
        """

        # create midi file
        staff = abjad.Staff()
        voice = abjad.Voice()
        staff.append(voice)

        # insert intro pad sequence from seq_index
        for sequence_index in range(4):
            intro_note = Note(utils.map_note(
                constants.INITIAL_NOTE[self.initial_note_index],
                constants.MODES[self.modal_index],
                constants.INTRO_SEQUENCE[self.sequence][sequence_index]), False)
            voice.append(utils.get_note_events(intro_note, 0))

        # populate content
        for note in self.content_notes:
            voice.append(utils.get_note_events(note, 0))

        # insert terminal pad sequence from seq_index
        for sequence_index in range(4):
            outro_note = Note(utils.map_note(
                constants.INITIAL_NOTE[self.initial_note_index],
                constants.MODES[self.modal_index],
                constants.TERMINAL_SEQUENCE[self.sequence][sequence_index]), False)
            voice.append(utils.get_note_events(outro_note, 0))

        # append everything in staff
        lilypond_file = abjad.LilyPondFile.new(staff)
        lilypond_file.header_block.title = abjad.Markup(str(bytes(self)))
        lilypond_file.header_block.composer = abjad.Markup("byte2jam")
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.top_margin = 15
        lilypond_file.layout_block.left_margin = 15

        return lilypond_file

    def export_midi(self):
        model = self.get_model()
        saver = abjad.persist(model)
        saver.as_midi()

    def export_pdf(self):
        model = self.get_model()
        saver = abjad.persist(model)
        saver.as_pdf()

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
