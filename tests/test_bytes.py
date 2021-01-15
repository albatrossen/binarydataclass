from binarydataclass import from_bytes, Uint8, len_from
from dataclasses import dataclass

@dataclass
class Point:
    x: Uint8
    y: bytes = len_from(2)

def test_basic():
    obj = from_bytes(Point, b'\x01\x02\x05')
    assert type(obj) == Point
    assert type(obj.x) == Uint8 and obj.x == 1
    assert obj.y == bytes((2,5))
