from io import BytesIO
from dataclasses import is_dataclass, fields, field
from typing import TypeVar, Type, Union
from enum import Enum

T = TypeVar('T')

def from_bytesio(cls: Type[T] , io: BytesIO, count = None) -> T:
    if hasattr(cls, 'from_bytesio'):
        value = cls.from_bytesio(io)
        return value
    if is_dataclass(cls):
        values = {}
        for field in fields(cls):
            count = field.metadata.get('len_from', None)
            if isinstance(count, str):
                count = values[count]
            values[field.name] = from_bytesio(field.type, io, count)
        return cls(**values)
    if hasattr(cls, '__origin__'):
        orig_type = cls.__origin__
        if orig_type == list:
            if count is None:
                raise NotImplemented()
            subtype = cls.__args__[0]
            return [from_bytesio(subtype, io) for _ in range(count)]
        if orig_type == Union:
            raise NotImplemented()
        raise NotImplemented()
        

def from_bytes(cls: Type[T], s) -> T:
    return from_bytesio(cls, BytesIO(s))

def len_from(source, **kwargs):
    return field(metadata={'len_from': source}, **kwargs)

def union(source, **kwargs):
    return field(metadata={'len_from': source}, **kwargs)

class Uint8(int):
    @classmethod
    def from_bytesio(cls, io):
        return cls(int.from_bytes(io.read(1), 'big'))