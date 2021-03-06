from binarydataclass import from_bytes, Uint8, binaryfield, var_size, fixed_size
from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: Uint8
    y: Uint8


@dataclass
class PolyLine:
    num_points: Uint8
    points: List[Point] = binaryfield(decoder=var_size("num_points"))


@dataclass
class Triangle:
    points: List[Point] = binaryfield(decoder=fixed_size(3))


def test_variable_array():
    obj = from_bytes(PolyLine, b"\x05\x01\x01\x02\x02\x03\x03\x04\x04\x05\x05")
    assert type(obj) == PolyLine
    assert type(obj.num_points) == Uint8 and obj.num_points == 5
    assert type(obj.points) == list and len(obj.points) == 5
    assert obj.points == [
        Point(1, 1),
        Point(2, 2),
        Point(3, 3),
        Point(4, 4),
        Point(5, 5),
    ]


def test_fixed_array():
    obj = from_bytes(PolyLine, b"\x03\x01\x01\x02\x02\x03\x03")
    assert type(obj) == PolyLine
    assert type(obj.points) == list and len(obj.points) == 3
    assert obj.points == [Point(1, 1), Point(2, 2), Point(3, 3)]
