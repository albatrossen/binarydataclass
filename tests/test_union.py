from binarydataclass import from_bytes, Uint8, union
from dataclasses import dataclass
from typing import Union
from enum import Enum
from pytest import mark

@dataclass
class Point2D:
    x: Uint8
    y: Uint8

@dataclass
class Point3D:
    x: Uint8
    y: Uint8
    z: Uint8

class PointType(Uint8, Enum):
    POINT_2D = 1
    POINT_3D = 2

@dataclass
class Container:
    point_type: PointType
    point: Union[Point2D, Point3D] = union('point_type')


@mark.skip
def test_basic():
    obj = from_bytes(Container, b'\x01\x02\x05')
    assert type(obj) == Container
    assert obj.point_type == PointType.POINT_2D
    assert obj.point == Point2D(2,5)
