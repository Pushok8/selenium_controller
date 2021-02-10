import os
from typing import Union, Optional, NoReturn

from selenium.webdriver import Firefox,FirefoxOptions, ChromeOptions, DesiredCapabilities
from seleniumwire.webdriver import Chrome, Remote, Firefox

from misc.proxy import Proxy
from misc.annotations import StrIPAddress
from misc.exceptions import SuchBrowserIsNotSupportedError


class BaseSeleniumController(object):
    def __init__(self,
                 browser_name: Union['Firefox', 'Chrome'] = 'Chrome',
                 options: Optional[Union[FirefoxOptions, ChromeOptions]] = None,
                 use_remote_server_address: Optional[StrIPAddress] = False,
                 proxy: Optional[Proxy] = None) -> NoReturn:
        """
        TODO
        :param browser_name:
        :param options:
        :param use_remote_server_address:
        :param proxy:
        """
        path_to_browser_driver = '/home/hunt/PycharmProjects/selenium_controller/for_development/chromedriver'

        if use_remote_server_address:
            self.driver = Remote
            if browser_name.strip().lower() == 'firefox':
                options = options if options else FirefoxOptions()
                options.add_argument('-headless')
            elif browser_name.strip().lower() == 'chrome':
                options = options if options else ChromeOptions()
                options.add_argument('disable-infobars')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')
                options.add_argument('--headless')
            else:
                raise SuchBrowserIsNotSupportedError(f'A browser such as {browser_name!r} does not support this controller.'
                                                     ' Please specify one of these browser: Chrome, Firefox}')
        else:
            if browser_name.strip().lower() == 'firefox':
                self.driver = Firefox
                options = options if options else FirefoxOptions()
            elif browser_name.strip().lower() == 'chrome':
                self.driver = Chrome
                options = options if options else ChromeOptions()
                options.add_argument('--start-maximized')
                options.add_argument('disable-infobars')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')
            else:
                raise SuchBrowserIsNotSupportedError(f'A browser such as {browser_name!r} does not support this controller.'
                                                     ' Please specify one of these browser: Chrome, Firefox}')
        desires_capabilities: dict = DesiredCapabilities.__dict__[browser_name.strip().upper()]

        if proxy:
            seleniumwire_options = {}
            if proxy.login and proxy.password:
                seleniumwire_options['proxy'] = {
                        'https': f'http://{proxy.login}:{proxy.password}@{proxy.ip_v4_address}:{proxy.port}'
                }
            else:
                if browser_name.strip().lower() == 'firefox':
                    options.set_preference('network.proxy.type', 1)
                    options.set_preference('network.proxy.http', proxy.ip_v4_address)
                    options.set_preference('network.proxy.http_port', proxy.port)
                    options.set_preference('network.proxy.https', proxy.ip_v4_address)
                    options.set_preference('network.proxy.https_port', proxy.port)
                    options.set_preference('network.proxy.ssl', proxy.ip_v4_address)
                    options.set_preference('network.proxy.ssl_port', proxy.port)
                elif browser_name.strip().lower() == 'chrome':
                    options.add_argument(f'--proxy-server={proxy.ip_v4_address}:{proxy.port}')

            if self.driver is Remote:
                seleniumwire_options['addr'] = use_remote_server_address
                self.driver = self.driver(command_executor=f'https://{use_remote_server_address}:4444/wd/hub',
                                          desired_capabilities=desires_capabilities,
                                          seleniumwire_options=seleniumwire_options,
                                          options=options)
                self.driver.set_window_size(2560, 1440)
            else:
                self.driver = self.driver(executable_path=path_to_browser_driver,
                                          desired_capabilities=desires_capabilities,
                                          seleniumwire_options=seleniumwire_options,
                                          options=options)
                self.driver.maximize_window()
        else:
            if self.driver is Remote:
                self.driver = self.driver(command_executor=f'http://{use_remote_server_address}:4444/wd/hub',
                                          desired_capabilities=desires_capabilities,
                                          seleniumwire_options={'addr': use_remote_server_address},
                                          options=options)
                self.driver.set_window_size(2560, 1440)
            else:
                if browser_name.strip().lower() == 'chrome':
                    self.driver = self.driver(executable_path=path_to_browser_driver,
                                              desired_capabilities=desires_capabilities,
                                              options=options)
                elif browser_name.strip().lower() == 'firefox':
                    self.driver = self.driver(executable_path=path_to_browser_driver,
                                              desired_capabilities=desires_capabilities,
                                              seleniumwire_options={'port': 8080},
                                              options=options)
                self.driver.maximize_window()

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()