from binarydataclass import from_bytes, Uint8, Uint64
from dataclasses import dataclass
from typing import List
from pytest import raises


@dataclass
class Point:
    x: Uint8
    y: Uint8


@dataclass
class BigPoint:
    x: Uint64
    y: Uint64


def test_toomuch():
    with raises(ValueError):
        obj = from_bytes(Point, b"\x05\x01\x01")


def test_toolittle():
    with raises(ValueError):
        obj = from_bytes(Point, b"\x03")


def test_toomuch64():
    with raises(ValueError):
        obj = from_bytes(BigPoint, b"\xff" * 20)


def test_toolittle64():
    with raises(ValueError):
        obj = from_bytes(BigPoint, b"\x03" * 10)
