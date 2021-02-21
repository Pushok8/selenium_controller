import os
import zipfile
import tarfile
import warnings
from typing import Text
from pathlib import Path
from sys import platform

import requests

from misc.annotations import StrName, StrFilePath
from misc.exceptions import WebDriverFileIsNotFoundException, WebDriversDownloadedAutomaticallyWarning
from misc.exceptions import WebDriversDownloadedInTMPFileWarning


AVAILABLE_BROWSERS: tuple[str] = ('Chrome', 'Firefox')


def create_web_driver_folder() -> None:
    r"""
    Creates a web_drivers folder in the /tmp file, if the system is Linux or MacOS, or C:\Program Files if
    the system windows.
    /
    Создаёт web_driver папку в /tmp файле, если система linux или MacOS или в C:\Program Files
    если система windows.
    """
    if 'linux' in platform or platform == 'darwin':  # Linux or Mac OS
        os.mkdir('/tmp/web_drivers/')
    elif platform == 'win32':  # Windows
        os.mkdir(r'C:\Program Files\web_drivers')


def download_firefox_web_driver() -> None:
    r"""
    Downloads Firefox web driver to the /tmp/web_drivers file, if the system is Linux or MacOS, or
    C:\Program Files\web_drivers if the system is windows.
    /
    Скачивает веб-драйвер Firefox в файл /tmp/web_drivers, если система Linux или MacOS, или C:\Program Files\web_drivers,
    если система windows

    Firefox web drivers 0.29 version:
        Linux -> https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
        MacOS -> https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-macos.tar.gz
        Windows -> https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-win64.zip
    """
    if 'linux' in platform:  # Linux
        firefox_web_driver = requests.get('https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz')
    elif platform == 'darwin':  # Mac OS
        firefox_web_driver = requests.get('https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-macos.tar.gz')
    elif platform == 'win32':  # Windows
        firefox_web_driver = requests.get('https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-win64.zip')

    if 'linux' in platform or platform == 'darwin':  # Linux or Mac OS
        with open('/tmp/web_drivers/geckodriver.tar.gz', 'wb') as firefox_web_driver_archive:
            firefox_web_driver_archive.write(firefox_web_driver.content)

        with tarfile.open('/tmp/web_drivers/geckodriver.tar.gz') as firefox_web_driver_archive:
            firefox_web_driver_archive.extractall('/tmp/web_drivers')
            os.remove('/tmp/web_drivers/geckodriver.tar.gz')

    elif platform == 'win32':  # Windows
        with open(r'C:\Program Files\web_drivers\geckodriver.zip', 'wb') as firefox_web_driver_archive:
            firefox_web_driver_archive.write(firefox_web_driver.content)

        with zipfile.ZipFile(r'C:\Program Files\web_drivers\geckodriver.zip') as firefox_web_driver_archive:
            firefox_web_driver_archive.extractall(r'C:\Program Files\web_drivers')
            os.remove(r'C:\Program Files\web_drivers\geckodriver.zip')


def download_chrome_web_driver() -> None:
    r"""
    Downloads the chrome web driver and Firefox web driver to the /tmp/web_drivers file, if the system is Linux or MacOS,
    or C:\Program Files\web_drivers if the system is windows.
    /
    Скачивает веб-драйвер Chrome в файл /tmp/web_drivers, если
    система Linux или MacOS, или C:\Program Files\web_drivers, если система windows

    Chrome web drivers 89 version:
        Linux -> https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
        MacOS -> https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_mac64.zip
        Windows -> https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_win32.zip

    """
    if 'linux' in platform:  # Linux
        chrome_web_driver = requests.get('https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip')
    elif platform == 'darwin':  # Mac OS
        chrome_web_driver = requests.get('https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_mac64.zip')
    elif platform == 'win32':  # Windows
        chrome_web_driver = requests.get('https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_win32.zip')

    if 'linux' in platform or platform == 'darwin':  # Linux or Mac OS
        path_to_web_drivers: StrFilePath = '/tmp/web_drivers'
    elif platform == 'win32':  # Windows
        path_to_web_drivers: StrFilePath = r'C:\Program Files\web_drivers'

    with open(Path(path_to_web_drivers, 'chromedriver.zip'), 'wb') as chrome_web_driver_archive:
        chrome_web_driver_archive.write(chrome_web_driver.content)

    with zipfile.ZipFile(Path(path_to_web_drivers, 'chromedriver.zip')) as chrome_web_driver_archive:
        chrome_web_driver_archive.extractall(path_to_web_drivers)
        os.remove(Path(path_to_web_drivers, 'chromedriver.zip'))


def check_do_have_web_drivers() -> None:
    """
    Checks if there are web driver components for working with Firefox and Chrome browser. If they are not, download this.
    /
    Проверяет наличие компонентов веб-драйвера для работы с браузером Firefox и Chrome. Если их нету, загружает их.
    """
    warning_message_for_all_web_drivers: Text = r''' WebDriversDownloadedAutomaticallyWarning:
Chrome and Firefox web drivers are downloaded automatically, make sure the version of the automatically downloaded Chrome 
and Firefox web drivers is not higher than your Chrome or Firefox browser.
Download web drivers for Chrome and Firefox using the links:
   ChromeDrivers -> https://chromedriver.chromium.org/downloads
   FirefoxDrivers -> https://github.com/mozilla/geckodriver/releases

Web drivers should be in /usr/local/bin or /tmp/web_drivers(not recommended, web drivers will be removed after system reboot), 
if your system is Linux or MacOS, or C:\Program Files\web_drivers if the system is windows.

IMPORTANT: the downloaded Chrome web driver must be named only "chromedrivers" and nothing else and the Firefox web 
driver must be named "geckodriver" and nothing else.'''
    warning_message_for_chrome_web_driver: Text = r''' WebDriversDownloadedAutomaticallyWarning:
Chrome web driver are downloaded automatically, make sure the version of the automatically downloaded Chrome web driver 
is not higher than your Chrome browser. Download web drivers for Chrome and Firefox using the links:
   ChromeDrivers -> https://chromedriver.chromium.org/downloads

Chrome driver should be in /usr/local/bin or /tmp/web_drivers(not recommended, web drivers will be removed after system reboot), 
if your system is Linux or MacOS, or C:\Program Files\web_drivers if the system is windows.

IMPORTANT: the downloaded Chrome web driver must be named only "chromedrivers" and nothing else.'''
    warning_message_for_firefox_web_driver: Text = r''' WebDriversDownloadedAutomaticallyWarning:
Firefox web driver are downloaded automatically, make sure the version of the automatically downloaded Firefox web driver 
is not higher than your Firefox browser. Download web drivers for Firefox using the links:
   FirefoxDrivers -> https://github.com/mozilla/geckodriver/releases

Web driver should be in /usr/local/bin or /tmp/web_drivers(not recommended, web drivers will be removed after system reboot), 
if your system is Linux or MacOS, or C:\Program Files\web_drivers if the system is windows.

IMPORTANT: the Firefox web driver must be named "geckodriver" and nothing else.'''
    warning_message_for_downloaded_web_drivers_in_tmp_file: Text = ''' WebDriversDownloadedInTMPFileWarning:
Your web drivers downloaded into the /tmp/web_drivers file, it means that after a system reboot web driver will be removed. 
Please, download web drivers in /usr/local/bin folder.

Download web drivers for Chrome and Firefox using the links:
   ChromeDrivers -> https://chromedriver.chromium.org/downloads
   FirefoxDrivers -> https://github.com/mozilla/geckodriver/releases

IMPORTANT: the downloaded Chrome web driver must be named only "chromedrivers" and nothing else and the Firefox web 
driver must be named "geckodriver" and nothing else.'''

    if 'linux' in platform or platform == 'darwin':  # Linux or Mac OS
        path_to_web_drivers: StrFilePath = '/usr/local/bin'
        filenames_in_path_to_web_drivers_folder: list[StrName] = [filename.lower() for filename in os.listdir(path_to_web_drivers)]
        if 'chromedriver' not in filenames_in_path_to_web_drivers_folder and 'geckodriver' not in filenames_in_path_to_web_drivers_folder:
            warnings.warn(warning_message_for_all_web_drivers, WebDriversDownloadedAutomaticallyWarning)
            warnings.warn(warning_message_for_downloaded_web_drivers_in_tmp_file, WebDriversDownloadedInTMPFileWarning)
            if not os.path.exists('/tmp/web_drivers'):
                create_web_driver_folder()
            if 'chromedriver' not in [filename.lower() for filename in os.listdir('/tmp/web_drivers')]:
                download_chrome_web_driver()
            if 'geckodriver' not in [filename.lower() for filename in os.listdir('/tmp/web_drivers')]:
                download_firefox_web_driver()

        elif 'chromedriver' not in filenames_in_path_to_web_drivers_folder:
            warnings.warn(warning_message_for_chrome_web_driver, WebDriversDownloadedAutomaticallyWarning)
            warnings.warn(warning_message_for_downloaded_web_drivers_in_tmp_file, WebDriversDownloadedInTMPFileWarning)
            if not os.path.exists('/tmp/web_drivers'):
                create_web_driver_folder()
            if 'chromedriver' not in [filename.lower() for filename in os.listdir('/tmp/web_drivers')]:
                download_chrome_web_driver()

        elif 'geckodriver' not in filenames_in_path_to_web_drivers_folder:
            warnings.warn(warning_message_for_firefox_web_driver, WebDriversDownloadedAutomaticallyWarning)
            warnings.warn(warning_message_for_downloaded_web_drivers_in_tmp_file, WebDriversDownloadedInTMPFileWarning)
            if not os.path.exists('/tmp/web_drivers'):
                create_web_driver_folder()
            if 'geckodriver' not in [filename.lower() for filename in os.listdir('/tmp/web_drivers')]:
                download_firefox_web_driver()
    elif platform == 'win32':  # Windows
        path_to_web_drivers: StrFilePath = r'C:\Program Files\web_drivers'
        if not os.path.exists(path_to_web_drivers):
            warnings.warn(warning_message_for_all_web_drivers, WebDriversDownloadedAutomaticallyWarning)
            create_web_driver_folder()
            download_chrome_web_driver()
            download_firefox_web_driver()
        if 'chromedriver' not in [filename.lower() for filename in os.listdir(path_to_web_drivers)]:
            warnings.warn(warning_message_for_chrome_web_driver, WebDriversDownloadedAutomaticallyWarning)
            download_chrome_web_driver()
        if 'geckodriver' not in [filename.lower() for filename in os.listdir(path_to_web_drivers)]:
            warnings.warn(warning_message_for_firefox_web_driver, WebDriversDownloadedAutomaticallyWarning)
            download_firefox_web_driver()


def get_path_to_web_driver_file(web_driver_filename: StrName) -> StrFilePath:
    r"""
    Get the path to the web driver file found by web_driver_filename in the /usr/local/bin or /tmp/web_drivers file, if
    the system is Linux or MacOS, or C:\Program Files\web_drivers if the system windows.
    /
    Получить путь к файлу веб-драйвера, который найден по имени web_driver_filename в папке /usr/local/bin or
    /tmp/web_drivers, если систама Linux или MacOS, или в C:\Program Files\web_drivers если система windows.
    
    
    :param web_driver_filename: the name of the web driver by which to found the web driver./имя веб-драйвера, по
    которому нужно найти веб-драйвер.
    
    :return: path to the found web driver
    """
    if 'linux' in platform or platform == 'darwin':  # Linux or Mac OS
        folder_with_web_drivers: StrFilePath = '/usr/local/bin'
        for filename in os.listdir(folder_with_web_drivers):
            if web_driver_filename == filename.lower():
                return Path(folder_with_web_drivers, filename)
        # If we not fond in /usr/local/bin directory.

        folder_with_web_drivers = '/tmp/web_drivers'
        for filename in os.listdir(folder_with_web_drivers):
            if web_driver_filename == filename.lower():
                return Path(folder_with_web_drivers, filename)
    elif platform == 'win32':  # Windows
        folder_with_web_drivers: StrFilePath = r'C:\Program Files\web_drivers'
        for filename in os.listdir(folder_with_web_drivers):
            if web_driver_filename == filename.lower():
                return Path(folder_with_web_drivers, filename)

    raise WebDriverFileIsNotFoundException(
        f'Web driver by name {web_driver_filename} is not found in {folder_with_web_drivers} folder!')