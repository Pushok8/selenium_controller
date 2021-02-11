import os
import zipfile
import tarfile
from pathlib import Path
from sys import platform
from typing import NoReturn

import requests

from misc.annotations import StrName, StrFilePath
from misc.exceptions import WebDriverFileIsNotFoundException


AVAILABLE_BROWSERS = ('Chrome', 'Firefox')


def create_web_driver_folder() -> NoReturn:
    """
    Creates a web_drivers folder in the /tmp file, if the system is Linux or MacOS, or C:\Program Files\web_drivers if
    the system windows./Создаёт web_driver папку в /tmp файле, если система linux или MacOS или C:\Program Files\web_drivers
    если система windows.
    """
    if 'linux' in platform or platform == 'darwin':  # Linux or Mac OS
        os.mkdir('/tmp/web_drivers/')
    elif platform == 'win32':  # Windows
        os.mkdir(r'C:\Program Files\web_drivers')


def download_web_drivers() -> NoReturn:
    """
    Downloads the chrome web driver and Firefox web driver to the /tmp file, if the system is Linux or MacOS, or
    C:\Program Files\web_drivers if the system is windows./Скачивает веб-драйвер Chrome и Firefox в файл /tmp, если
    система Linux или MacOS, или C:\Program Files\web_drivers, если система windows

    Chrome web drivers 89 version:
        Linux -> https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
        MacOS -> https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_mac64.zip
        Windows -> https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_win32.zip

    Firefox web drivers 0.29 version:
        Linux -> https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
        MacOS -> https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-macos.tar.gz
        Windows -> https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-win64.zip
    """

    print(r'''
Chrome and Firefox web drivers are downloaded automatically, make sure the version of the automatically 
downloaded chrome and Firefox web drivers is not higher than your Chrome or Firefox browser.
Download web drivers for Chrome and Firefox using the links:
   ChromeDrivers -> https://chromedriver.chromium.org/downloads
   FirefoxDrivers -> https://github.com/mozilla/geckodriver/releases
   
Web drivers should be in /tmp/web_drivers, if your system is Linux or MacOS, or C:\Program Files\web_drivers if the system is windows.''')

    if 'linux' in platform:  # Linux
        chrome_web_driver = requests.get('https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip')
        firefox_web_driver = requests.get('https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz')
    elif platform == 'darwin':  # Mac OS
        chrome_web_driver = requests.get('https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_mac64.zip')
        firefox_web_driver = requests.get('https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-macos.tar.gz')
    elif platform == 'win32':  # Windows
        chrome_web_driver = requests.get('https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_win32.zip')
        firefox_web_driver = requests.get('https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-win64.zip')

    if 'linux' in platform or platform == 'darwin':  # Linux or Mac OS
        with open('/tmp/web_drivers/chromedriver.zip', 'wb') as chrome_web_driver_archive:
            chrome_web_driver_archive.write(chrome_web_driver.content)
        with open('/tmp/web_drivers/geckodriver.tar.gz', 'wb') as firefox_web_driver_archive:
            firefox_web_driver_archive.write(firefox_web_driver.content)

        with zipfile.ZipFile('/tmp/web_drivers/chromedriver.zip') as chrome_web_driver_archive:
            chrome_web_driver_archive.extractall('/tmp/web_drivers')
            os.remove('/tmp/web_drivers/chromedriver.zip')
        with tarfile.open('/tmp/web_drivers/geckodriver.tar.gz') as firefox_web_driver_archive:
            firefox_web_driver_archive.extractall('/tmp/web_drivers')
            os.remove('/tmp/web_drivers/geckodriver.tar.gz')

    elif platform == 'win32':  # Windows
        with open(r'C:\Program Files\web_drivers\chromedriver.zip', 'wb') as chrome_web_driver_archive:
            chrome_web_driver_archive.write(chrome_web_driver.content)
        with open(r'C:\Program Files\web_drivers\geckodriver.zip', 'wb') as firefox_web_driver_archive:
            firefox_web_driver_archive.write(firefox_web_driver.content)

        with zipfile.ZipFile(r'C:\Program Files\web_drivers\chromedriver.zip') as chrome_web_driver_archive:
            chrome_web_driver_archive.extractall(r'C:\Program Files\web_drivers')
            os.remove(r'C:\Program Files\web_drivers\chromedriver.zip')
        with zipfile.ZipFile(r'C:\Program Files\web_drivers\geckodriver.zip') as firefox_web_driver_archive:
            firefox_web_driver_archive.extractall(r'C:\Program Files\web_drivers')
            os.remove(r'C:\Program Files\web_drivers\geckodriver.zip')


def check_do_have_web_drivers() -> NoReturn:
    """
    Checks if there are web driver components for working with Firefox and Chrome browser. If they are not, download this./
    Проверяет наличие компонентов веб-драйвера для работы с браузером Firefox и Chrome. Если их нету, загружает их.
    """
    if 'linux' in platform or platform == 'darwin':  # Linux or Mac OS
        if not os.path.exists('/tmp/web_drivers'):
            create_web_driver_folder()
            download_web_drivers()

        if not os.listdir('/tmp/web_drivers'):
            download_web_drivers()

    elif platform == 'win32':  # Windows
        if not os.path.exists(r'C:\Program Files\web_drivers'):
            create_web_driver_folder()
            download_web_drivers()

        if not os.listdir(r'C:\Program Files\web_drivers'):
            download_web_drivers()


def get_path_to_web_driver_file(web_driver_filename: StrName) -> StrFilePath:
    """
    Get the path to the web driver file found by web_driver_filename in the /tmp/web_drivers file, if the system is Linux or MacOS,
    or C:\Program Files\web_drivers if the system windows./Получить путь к файлу веб-драйвера, который найден по имени
    web_driver_filename в папке /tmp/web_drivers, если систама Linux или MacOS, или в C:\Program Files\web_drivers если
    система windows.
    :param web_driver_filename: the name of the web driver by which to found the web driver./имя веб-драйвера, по
    которому нужно найти веб-драйвер.
    :return: path to the found web driver
    """
    if 'linux' in platform or platform == 'darwin':  # Linux or Mac OS
        folder_with_web_drivers: StrFilePath = '/tmp/web_drivers'
    elif platform == 'win32':  # Windows
        folder_with_web_drivers: StrFilePath = r'C:\Program Files\web_drivers'

    for filename in os.listdir('/tmp/web_drivers'):
        if web_driver_filename in filename:
            return Path(folder_with_web_drivers, filename)

    raise WebDriverFileIsNotFoundException(
        f'Web driver by name {web_driver_filename} is not found in {folder_with_web_drivers} folder!')