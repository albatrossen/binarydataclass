from binarydataclass import from_bytes, Uint8, binaryfield, octets
from dataclasses import dataclass


@dataclass
class OctetPacket:
    x: Uint8
    y: bytes = binaryfield(octets(2))


def test_bytes():
    obj = from_bytes(OctetPacket, b"\x01\x02\x05")
    assert type(obj) == OctetPacket
    assert type(obj.x) == Uint8 and obj.x == 1
    assert obj.y == bytes((2, 5))
