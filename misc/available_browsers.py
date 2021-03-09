from enum import Enum
from misc.annotations import StrName


class AvailableBrowsers(str, Enum):
    """Set of supported browsers."""
    CHROME: StrName = 'CHROME'
    FIREFOX: StrName = 'FIREFOX'