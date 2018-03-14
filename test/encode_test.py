import pytest
from byte2jam import schema

def test_encode_decode():
    test_bytes = bytes(b'I\'m feeling hungry!')
    encoded = schema.ByteJamSchema.from_bytes(test_bytes)
    assert bytes(encoded) == test_bytes
