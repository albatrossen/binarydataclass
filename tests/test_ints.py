from binarydataclass import from_bytes, Uint8, Uint16, Uint32, Uint64, Int8, Int16, Int32, Int64, len_from, binaryfield
from dataclasses import dataclass

@dataclass
class PointWithTypes:
    a: Uint8
    b: Uint16
    c: Uint32
    d: Uint64
    e: Int8
    f: Int16
    g: Int32
    h: Int64

@dataclass
class PointWithoutTypes:
    a: int = binaryfield(bytes=1)
    b: int = binaryfield(bytes=2)
    c: int = binaryfield(bytes=4)
    d: int = binaryfield(bytes=8)
    e: int = binaryfield(bytes=1, signed=True)
    f: int = binaryfield(bytes=2, signed=True)
    g: int = binaryfield(bytes=4, signed=True)
    h: int = binaryfield(bytes=8, signed=True)

def test_with_types():
    obj = from_bytes(PointWithTypes, b'\x01\x00\x02\x00\x00\x00\x05\xff\xff\xff\xff\xff\xff\xff\xff\x01\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\xff\xff\xff\xff')
    assert obj == PointWithTypes(
        1,
        2,
        5,
        18446744073709551615,
        1,
        -1,
        5,
        -1
    )

def test_without_types():
    obj = from_bytes(PointWithoutTypes, b'\x01\x00\x02\x00\x00\x00\x05\xff\xff\xff\xff\xff\xff\xff\xff\x01\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\xff\xff\xff\xff')
    assert obj == PointWithoutTypes(
        1,
        2,
        5,
        18446744073709551615,
        1,
        -1,
        5,
        -1
    )