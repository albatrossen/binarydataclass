from binarydataclass import from_bytes, Uint8
from dataclasses import dataclass

@dataclass
class Point:
    x: Uint8
    y: Uint8
    z: Uint8

def test_basic():
    obj = from_bytes(Point, b'\x01\x02\x05')
    assert type(obj) == Point
    assert type(obj.x) == Uint8 and obj.x == 1
    assert type(obj.y) == Uint8 and obj.y == 2
    assert type(obj.z) == Uint8 and obj.z == 5