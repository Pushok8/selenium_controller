from pathlib import Path
from typing import TypeVar, NewType

from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.firefox.options import Options as FOptions

__all__ = [
    'StrIPAddress', 'StrOfNumbers', 'StrName', 'StrFilePath', 'StrSocket', 'ChromeOptions', 'FirefoxOptions', 'StrLink',
    'StrCSSSelector', 'StrXPath'
]


# The Options object in selenium for firefox and chrome is just called "Options", here I renamed it
class ChromeOptions(COptions):
    ...


class FirefoxOptions(FOptions):
    ...


StrLink = NewType('StrLink', str)
StrName = NewType('StrSocket', str)
StrIPAddress = NewType('StrIPAddress', str)
StrOfNumbers = NewType('StrSocket', str)
StrFilePath = TypeVar('StrFilePath', str, Path)
StrSocket = NewType('StrSocket', str)
StrCSSSelector = NewType('StrCSSSelector', str)
StrXPath = NewType('StrXPath', str)
