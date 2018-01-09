import unittest
from byte2jam.encoder import encode, decode

class TestEncode(unittest.TestCase):
    def setUp(self):
        self.test_bytes = bytearray(b"I'm feeling hungry!")
        pass

    def test_encode_decode(self):
        encoded = encode(self.test_bytes)
        self.assertEqual(decode(encoded), self.test_bytes)
