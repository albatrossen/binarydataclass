from binarydataclass import from_bytes, Uint8, Uint16, Uint32, Uint64, Int8, Int16, Int32, Int64, binaryfield, int_decoder
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
    a: int = binaryfield(int_decoder(bits=8))
    b: int = binaryfield(int_decoder(bits=16))
    c: int = binaryfield(int_decoder(bits=32))
    d: int = binaryfield(int_decoder(bits=64))
    e: int = binaryfield(int_decoder(bits=8, signed=True))
    f: int = binaryfield(int_decoder(bits=16, signed=True))
    g: int = binaryfield(int_decoder(bits=32, signed=True))
    h: int = binaryfield(int_decoder(bits=64, signed=True))

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