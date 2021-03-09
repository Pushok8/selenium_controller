from pathlib import Path
from typing import TypeVar

from selenium.webdriver.remote.webdriver import WebDriver

__all__ = [
    'StrIPAddress', 'StrOfNumbers', 'StrName', 'StrFilePath', 'StrSocket', 'StrLink', 'StrCSSSelector', 'StrXPath',
    'AnyWebDriver'
]


StrLink = TypeVar('StrLink', str, str)
StrName = TypeVar('StrName', str, str)
StrIPAddress = TypeVar('StrIPAddress', str, str)
StrOfNumbers = TypeVar('StrOfNumbers', str, str)
StrFilePath = TypeVar('StrFilePath', str, Path)
StrSocket = TypeVar('StrSocket', str, str)
StrCSSSelector = TypeVar('StrCSSSelector', str, str)
StrXPath = TypeVar('StrXPath', str, str)
AnyWebDriver = TypeVar('AnyWebDriver', bound=WebDriver)
