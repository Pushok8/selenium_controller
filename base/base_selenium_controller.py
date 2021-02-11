import os
from sys import platform
from typing import Union, Optional, NoReturn

from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver import FirefoxOptions, ChromeOptions, DesiredCapabilities
from seleniumwire.webdriver import Chrome, Remote, Firefox

from misc.proxy import Proxy
from misc.utils import check_do_have_web_drivers, get_path_to_web_driver_file, AVAILABLE_BROWSERS
from misc.annotations import StrFilePath, StrSocket
from misc.exceptions import SuchBrowserIsNotSupportedError


class BaseSeleniumController(object):
    def __init__(self,
                 browser_name: str = 'Chrome',
                 options: Optional[Union[FirefoxOptions, ChromeOptions]] = None,
                 use_remote_server_socket: Optional[Union[StrSocket, bool]] = False,
                 proxy: Optional[Proxy] = None) -> NoReturn:
        """
        Defines by the passed arguments which driver should be created and with which options.

        If you pass in a FirefoxOptions or ChromeOptions object, it will be used to create the driver object, but
        additional arguments will be added to FirefoxOptions or ChromeOptions anyway.

        If you pass in a use_remote_server_socket remote server socket, will be create Remote driver with headless
        mode(without GUI remotely). Socket these are IP address and port separated by colon(IP_ADDRESS:PORT).
        For example: socket it is 127.0.0.1:4444

        If you pass in a proxy Proxy object, a proxy with the specified parameters will be used. Proxy can be with
        authorization and without this.
        /
        По переданным аргументам определяет, какой драйвер должен быть создан и с какими параметрами.

        Если вы передадите объект FirefoxOptions или ChromeOptions, он будет использоваться для создания объекта драйвера,
        но в любом случае дополнительные аргументы будут добавлены в FirefoxOptions или ChromeOptions.

        Если вы передадите удаленный серверный сокет use_remote_server_socket, будет создан удаленный драйвер в headless
        режиме(без GUI удаленно). Сокет - это IP-адрес и порт, разделенные двоеточием (IP_ADDRESS: PORT).
        Например: сокет 127.0.0.1:4444

        Если вы передаете прокси-объект Прокси-объект, будет использоваться прокси с указанными параметрами. Прокси
        может быть с авторизация и без.

        :param browser_name: the name of the browser to be used. browser_name must be specified in
        selenium_controller.misc.utils.AVAILABLE_BROWSER. By default is Chrome. Optional/название используемого браузера.
        browser_name должен быть указан в AVAILABLE_BROWSER. По умолчанию Chrome. Необязательно.
        :param options: FirefoxOptions or ChromeOptions depending on which browser you are using. It will be used to
        create the driver object, but additional arguments will be added to FirefoxOptions or ChromeOptions anyway.
        Optional./FirefoxOptions или ChromeOptions в зависимости от того, какой браузер вы используете. Это будет
        использоваться для создания объекта драйвера, но в любом случае дополнительные аргументы будут добавлены в
        FirefoxOptions или ChromeOptions. Необязательно.
        :param use_remote_server_socket: bool value or server socket. If bool value is True - will be used
        127.0.0.1:4444 socket. Socket these are IP address and port separated by colon(IP_ADDRESS:PORT).
        For example: socket it is 127.0.0.1:4444. Optional/значение bool или серверный сокет. Если значение bool равно
        True - будет использоваться 127.0.0.1:4444 сокет. Сокет - это IP-адрес и порт, разделенные двоеточием (IP_ADDRESS: PORT).
        Например: сокет 127.0.0.1:4444. Необязательно
        :param proxy: Proxy object with the specified IP and port(and login and password if the proxy is with
        authorization). This proxy info is used to connect to the proxy server. If you need authorization in your proxy,
        specify login and password in Proxy object. You can get Proxy object from the selenium_controller.misc.proxy
        module. Optional./Прокси-объект с указанными IP и port (и логином и паролем, если прокси с авторизацией). Эти
        данные о прокси используются для подключения к прокси-серверу. Если вам нужна  авторизация в вашем прокси,
        укажите логин и пароль в объекте Proxy. Вы можете получить объект Proxy из модуля selenium_controller.misc.proxy.
        """
        if browser_name.strip().lower() not in (available_browser.lower() for available_browser in AVAILABLE_BROWSERS):
            raise SuchBrowserIsNotSupportedError(f'A browser such as {browser_name!r} does not support this controller.'
                                                 f' Please specify one of these browser: {str(AVAILABLE_BROWSERS)[1:-1]}')

        check_do_have_web_drivers()
        if browser_name.strip().lower() == 'firefox':
            path_to_browser_driver: StrFilePath = get_path_to_web_driver_file('geckodriver')
        elif browser_name.strip().lower() == 'chrome':
            path_to_browser_driver: StrFilePath = get_path_to_web_driver_file('chromedriver')
        if 'linux' in platform or platform == 'darwin':  # Linux or MacOS
            os.chmod(path_to_browser_driver, 755)

        if use_remote_server_socket:
            if use_remote_server_socket is True:
                use_remote_server_socket = '127.0.0.1:4444'
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
            if browser_name.strip().lower() == 'firefox':
                self.driver = Firefox
                options = options if options else FirefoxOptions()
            elif browser_name.strip().lower() == 'chrome':
                self.driver = Chrome
                options = options if options else ChromeOptions()
                options.add_argument('disable-infobars')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')

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
                seleniumwire_options['addr'] = use_remote_server_socket.strip(':')[0]
                self.driver = self.driver(command_executor=f'https://{use_remote_server_socket}/wd/hub',
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
                self.driver = self.driver(command_executor=f'http://{use_remote_server_socket}/wd/hub',
                                          desired_capabilities=desires_capabilities,
                                          seleniumwire_options={'addr': use_remote_server_socket.split(':')[0]},
                                          options=options)
                self.driver.set_window_size(2560, 1440)
            else:
                if browser_name.strip().lower() == 'chrome':
                    try:
                        self.driver = self.driver(executable_path=path_to_browser_driver,
                                                  desired_capabilities=desires_capabilities,
                                                  options=options)
                    except SessionNotCreatedException:
                        raise SessionNotCreatedException('Your chrome browser is older than the web driver. Please update your browser or change'
                                                         ' the web driver to your version or lower. Download chrome web drivers here -> https://chromedriver.chromium.org/downloads')
                elif browser_name.strip().lower() == 'firefox':
                    self.driver = self.driver(executable_path=path_to_browser_driver,
                                              desired_capabilities=desires_capabilities,
                                              seleniumwire_options={'port': 8080},
                                              options=options)

                self.driver.maximize_window()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()