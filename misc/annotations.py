from typing import NewType

__all__ = [
    'StrIPAddress', 'StrOfNumbers'
]

StrIPAddress = NewType('StrIPAddress', str)
StrOfNumbers = NewType('StrOfNumbers', str)