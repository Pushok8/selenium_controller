from typing import Union
from dataclasses import dataclass, field

from misc.annotations import StrIPAddress, StrOfNumbers


@dataclass
class Proxy(object):
    ip_v4_address: StrIPAddress
    port: Union[StrOfNumbers, int]
    login: str = field(default_factory=str)
    password: str = field(default_factory=str)
