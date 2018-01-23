import pytest
from byte2jam import encoder

def test_encode_decode():
    test_bytes = bytes(b'I\'m feeling hungry!')
    encoded = encoder.encode(test_bytes)
    assert encoder.decode(encoded) == test_bytes
