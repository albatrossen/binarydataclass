from binarydataclass import from_bytes, Uint8
from dataclasses import dataclass


@dataclass
class Point:
    x: Uint8
    y: Uint8


@dataclass
class BoundingBox:
    corner_a: Point
    corner_b: Point


def test_nested_class():
    obj = from_bytes(BoundingBox, b"\x01\x02\x05\x04")
    assert type(obj) == BoundingBox
    assert type(obj.corner_a) == Point and obj.corner_a == Point(1, 2)
    assert type(obj.corner_b) == Point and obj.corner_b == Point(5, 4)
