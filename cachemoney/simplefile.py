"""
Ref: https://chromium.googlesource.com/chromium/src/net/+/refs/heads/main/disk_cache/simple/simple_entry_format.h
"""

import binascii
import struct
from typing import BinaryIO, Tuple

FINAL_MAGIC = binascii.unhexlify("f4fa6f45970d41d8")[::-1]
INITIAL_MAGIC = binascii.unhexlify("fcfb6d1ba7725c30")[::-1]


def parse_simplefile(fs: BinaryIO) -> Tuple[str, bytes]:
    header = fs.read(8)
    assert header == INITIAL_MAGIC
    version, key_length, key_hash, dummy = struct.unpack("<IIII", fs.read(16))
    key = fs.read(key_length).decode("UTF-8").split(' ')[-1]
    data_with_trailer = fs.read()  # hardly optimal
    data, _, trailer = data_with_trailer.partition(FINAL_MAGIC)
    assert trailer
    return (key, data)
