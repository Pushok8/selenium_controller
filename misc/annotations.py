from pathlib import Path
from typing import NewType

__all__ = [
    'StrIPAddress', 'StrOfNumbers', 'StrName', 'StrFilePath', 'StrSocket'
]

StrName = NewType('StrName', str)
StrIPAddress = NewType('StrIPAddress', str)
StrOfNumbers = NewType('StrOfNumbers', str)
StrFilePath = NewType('StrFilePath', (str, Path))
StrSocket = NewType('StrSocket', str)