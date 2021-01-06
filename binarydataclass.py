from io import BytesIO
from dataclasses import is_dataclass, fields, field
from typing import TypeVar, Type, Union
from enum import Enum

T = TypeVar('T')

def from_bytesio(cls: Type[T] , io: BytesIO) -> T:
    if hasattr(cls, 'from_bytesio'):
        value = cls.from_bytesio(io)
        return value
    if is_dataclass(cls):
        values = {}
        for field in fields(cls):
            orig_type = getattr(field.type, '__origin__', None)
            if orig_type == list:
                subtype = field.type.__args__[0]
                count = field.metadata.get('len_from', None)
                if isinstance(count, str):
                    count = values[count]
                values[field.name] = [from_bytesio(subtype, io) for _ in range(count)]
            elif orig_type == Union:
                tag = field.metadata.get('union_tag', None)
                if isinstance(tag, str):
                    tag = values[tag]
                union_map = field.metadata.get('union_map', None)
                if union_map is None:
                    union_map = dict(zip(tag.__class__, field.type.__args__))
                subcls = union_map[tag]
                values[field.name] = from_bytesio(subcls, io)
            elif orig_type is not None:
                raise NotImplementedError()
            else:
                values[field.name] = from_bytesio(field.type, io)
        return cls(**values)        

def from_bytes(cls: Type[T], s) -> T:
    return from_bytesio(cls, BytesIO(s))

def len_from(source, **kwargs):
    return field(metadata={'len_from': source}, **kwargs)

def union(source, union_map=None, **kwargs):
    return field(metadata={'union_tag': source, 'union_map': union_map}, **kwargs)

class Uint8(int):
    @classmethod
    def from_bytesio(cls, io):
        return cls(int.from_bytes(io.read(1), 'big'))