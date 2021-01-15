from io import BytesIO
from dataclasses import is_dataclass, fields, field
from typing import TypeVar, Type, Union, Any, List
from enum import Enum, auto
import inspect
import dataclasses

T = TypeVar("T")

registry = {}


def register(handler):
    def onto(cls):
        registry[cls] = handler
        return cls

    return onto


def find_handler(cls: Type[T]):
    handler = getattr(cls, "from_bytesio", None)
    if handler:
        return handler

    orig_type = getattr(cls, "__origin__", None)
    handler = registry.get(orig_type, None)
    if handler:
        return handler

    if is_dataclass(cls):
        decoders = tuple(
            (field.name, field.type, field.metadata.get("decoder", from_bytesio))
            for field in fields(cls)
        )

        def handler(cls: Type[T], io: BytesIO, scope=None):
            values = {}
            for name, type, decoder in decoders:
                values[name] = decoder(type, io, values)
            return cls(**values)

        return handler

    for sub_class in cls.__mro__[1:]:
        if sub_class in registry:
            return registry[sub_class]
    raise NotImplementedError()


def from_bytesio(cls: Type[T], io: BytesIO, scope=None) -> T:
    try:
        handler = registry[cls]
    except KeyError:
        handler = find_handler(cls)
        register(handler)(cls)
    return handler(cls, io, scope)


def from_bytes(cls: Type[T], s) -> T:
    data = BytesIO(s)
    decoded = from_bytesio(cls, data)
    if data.read(1):
        raise ValueError("Extra data at end")
    return decoded


def binaryfield(decoder=None, **kwargs):
    return dataclasses.field(**kwargs, metadata={"decoder": decoder})


def union(*args, **kwargs):
    return binaryfield(union_decoder(*args, **kwargs))


def union_decoder(source, union_map=None, **kwargs):
    def handler(cls: Type[T], io: BytesIO, scope):
        nonlocal union_map
        tag = scope[source]
        if union_map is None:
            union_map = dict(zip(tag.__class__, cls.__args__))
        subcls = union_map[tag]
        return from_bytesio(subcls, io, scope)

    return handler


def int_decoder(bits, signed=False, endianess="big"):
    if bits % 8 != 0:
        raise NotImplementedError()
    size = bits // 8

    def handler(cls: Type[T], io: BytesIO, scope=None):
        val = readbytes(io, size)
        return cls(int.from_bytes(val, endianess, signed=signed))

    return handler


def fixed_size(num_elements):
    def handler(cls: Type[T], io: BytesIO, scope=None):
        subtype = cls.__args__[0]
        return [from_bytesio(subtype, io, scope) for _ in range(num_elements)]

    return handler


def var_size(field_name):
    def handler(cls: Type[T], io: BytesIO, scope=None):
        subtype = cls.__args__[0]
        num_elements = scope[field_name]
        return [from_bytesio(subtype, io, scope) for _ in range(num_elements)]

    return handler


def readbytes(io, count):
    val = bytearray(count)
    read = io.readinto(val)
    if read != count:
        raise ValueError(f"Expected {count} bytes but only got {read}")
    return val


def octets(size):
    if isinstance(size, str):

        def handler(cls: Type[T], io: BytesIO, scope=None):
            return readbytes(io, scope[size])

    elif isinstance(size, int):

        def handler(cls: Type[T], io: BytesIO, scope=None):
            return readbytes(io, size)

    else:
        raise NotImplementedError()
    return handler


@register(int_decoder(bits=8))
class Uint8(int):
    pass


@register(int_decoder(bits=16))
class Uint16(int):
    pass


@register(int_decoder(bits=32))
class Uint32(int):
    pass


@register(int_decoder(bits=64))
class Uint64(int):
    pass


@register(int_decoder(bits=8, signed=True))
class Int8(int):
    pass


@register(int_decoder(bits=16, signed=True))
class Int16(int):
    pass


@register(int_decoder(bits=32, signed=True))
class Int32(int):
    pass


@register(int_decoder(bits=64, signed=True))
class Int64(int):
    pass
