from binarydataclass import from_bytes, Uint8, Uint16, Uint32, Uint64
from dataclasses import dataclass

@dataclass
class Point:
    x: Uint8
    y: Uint8

def test_basic():
    obj = from_bytes(Point, b'\x01\x02')
    assert obj == Point(1,2)
    assert type(obj.x) == Uint8
    assert type(obj.y) == Uint8