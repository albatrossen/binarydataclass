from io import BytesIO
from dataclasses import is_dataclass, fields, field
from typing import TypeVar, Type, Union, Any, List
from enum import Enum
import inspect
import dataclasses

T = TypeVar('T')

def _resolve(scope, metadata, name):
    value = metadata.get(name, None)
    if isinstance(value, str):
        return scope[value]
    return value

def _list_from_bytesio(cls: Type[T] , io: BytesIO, scope, metadata):
    subtype = cls.__args__[0]
    count = _resolve(scope, metadata, 'size')
    return [from_bytesio(subtype, io, scope, metadata) for _ in range(count)]

def _union_from_bytesio(cls: Type[T] , io: BytesIO, scope, metadata):
    tag = _resolve(scope, metadata, 'union_tag')
    union_map = _resolve(scope, metadata, 'union_map')
    if union_map is None:
        union_map = dict(zip(tag.__class__, cls.__args__))
    subcls = union_map[tag]
    return from_bytesio(subcls, io, scope, metadata)


def _bytes_from_bytesio(cls: Type[T] , io: BytesIO, scope, metadata):
    size = _resolve(scope, metadata, 'bits') // 8
    val = bytearray(size)
    read = io.readinto(val)
    if read != size:
        raise ValueError(f"Expected {size} bytes but only got {read}")
    return cls(val)

def _int_from_bytesio(cls: Type[T] , io: BytesIO, scope, metadata):
    size = _resolve(scope, metadata, 'bits')
    if size is None:
        size = getattr(cls, 'bits')
    signed = _resolve(scope, metadata, 'signed')
    if signed is None:
        signed = getattr(cls, 'signed', False)
    val = _bytes_from_bytesio(bytearray, io, scope, {'bits': size})
    return cls(int.from_bytes(val, 'big', signed=signed))


register = {
    list: _list_from_bytesio,
    Union: _union_from_bytesio,
    bytes: _bytes_from_bytesio,
    int: _int_from_bytesio,
}

def from_bytesio(cls: Type[T] , io: BytesIO, scope = None, metadata = None) -> T:
    handler = register.get(cls, None)
    if not handler:
        handler = getattr(cls, 'from_bytesio', None)
    if not handler:
        orig_type = getattr(cls, '__origin__', None)
        handler = register.get(orig_type, None)
    if handler:
        return handler(cls, io, scope, metadata)
    if is_dataclass(cls):
        values = {}
        for field in fields(cls):
            values[field.name] = from_bytesio(field.type, io, values, field.metadata)
        return cls(**values)
    if cls not in register:
        register[cls] = None
        for sub_class in cls.__mro__[1:]:
            if sub_class in register:
                handler = register[sub_class]
                register[cls] = handler
                return handler(cls, io, scope, metadata)
    raise NotImplementedError()

def from_bytes(cls: Type[T], s) -> T:
    data = BytesIO(s)
    decoded = from_bytesio(cls, data)
    if data.read(1):
        raise ValueError('Extra data at end')
    return decoded

def binaryfield(field=None, endianess=None, bits=None, signed=None, bytes=None, size=None, **kwargs):
    if bits and bytes:
        raise ValueError("Not possible to supply both bits and bytes at the same time")
    elif bytes:
        bits = 8 * bytes
    del bytes
    metadata = {k:v for k,v in locals().items() if k is not 'kwargs'}
    return dataclasses.field(**kwargs, metadata=metadata)


def len_from(source, **kwargs):
    return binaryfield(bytes=source, **kwargs)

def union(source, union_map=None, **kwargs):
    return field(metadata={'union_tag': source, 'union_map': union_map}, **kwargs)

class Uint8(int):
    bits = 8

class Uint16(int):
    bits = 16

class Uint32(int):
    bits = 32

class Uint64(int):
    bits = 64

class Int8(int):
    bits = 8
    signed = True

class Int16(int):
    bits = 16
    signed = True

class Int32(int):
    bits = 32
    signed = True

class Int64(int):
    bits = 64
    signed = True