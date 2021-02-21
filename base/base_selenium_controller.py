import os
from pathlib import Path
from sys import platform
from functools import wraps
from typing import Union, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire.webdriver import Chrome, Remote, Firefox

from misc.proxy import Proxy
from misc.utils import check_do_have_web_drivers, get_path_to_web_driver_file, AVAILABLE_BROWSERS
from misc.annotations import StrFilePath, StrLink, StrName, StrSocket,  FirefoxOptions, ChromeOptions  # import renamed Options object for Firefox and Chrome
from misc.exceptions import SuchBrowserIsNotSupportedError


class BaseSeleniumController(object):
    def __init__(self,
                 browser_name: StrName = 'Chrome',
                 options: Optional[Union[FirefoxOptions, ChromeOptions]] = None,
                 use_remote_server_socket: Optional[Union[StrSocket, bool]] = None,
                 proxy: Optional[Proxy] = None,
                 custom_path_to_web_drivers: Optional[StrFilePath] = None) -> None:
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


        :param browser_name: Optional. the name of the browser to be used. browser_name must be specified in
        selenium_controller.misc.utils.AVAILABLE_BROWSER. By default is Chrome/Необязательно. название
        используемого браузера. browser_name должен быть указан в AVAILABLE_BROWSER. По умолчанию Chrome.

        :param options: Optional. FirefoxOptions or ChromeOptions depending on which browser you are using. It will be
        used to create the driver object, but additional arguments will be added to FirefoxOptions or ChromeOptions
        anyway./Необязательно. FirefoxOptions или ChromeOptions в зависимости от того, какой браузер вы используете.
        Это будет использоваться для создания объекта драйвера, но в любом случае дополнительные аргументы будут
        добавлены в FirefoxOptions или ChromeOptions.

        :param use_remote_server_socket: Optional. bool value or server socket. If bool value is True - will be used
        127.0.0.1:4444 socket. Socket these are IP address and port separated by colon(IP_ADDRESS:PORT).
        For example: socket it is 127.0.0.1:4444./Необязательно. значение bool или серверный сокет. Если значение bool
        равно True - будет использоваться 127.0.0.1:4444 сокет. Сокет - это IP-адрес и порт, разделенные двоеточием
        (IP_ADDRESS: PORT). Например: сокет 127.0.0.1:4444.

        :param proxy: Optional. Proxy object with the specified IP and port(and login and password if the proxy is with
        authorization). This proxy info is used to connect to the proxy server. If you need authorization in your proxy,
        specify login and password in Proxy object. You can get Proxy object from the selenium_controller.misc.proxy
        module./Необязательно. Прокси-объект с указанными IP и port (и логином и паролем, если прокси с авторизацией).
        Эти данные о прокси используются для подключения к прокси-серверу. Если вам нужна  авторизация в вашем прокси,
        укажите логин и пароль в объекте Proxy. Вы можете получить объект Proxy из модуля selenium_controller.misc.proxy.

        :param custom_path_to_web_drivers: Optional. The path to the folder where the Chrome and Firefox web drivers are
        stored./Необязательно. Путь к папке, где хранятся веб-драйверы Chrome и Firefox.
        """
        if browser_name.strip().lower() not in (available_browser.lower() for available_browser in AVAILABLE_BROWSERS):
            raise SuchBrowserIsNotSupportedError(f'A browser such as {browser_name!r} does not support this controller.'
                                                 f' Please specify one of these browser: {str(AVAILABLE_BROWSERS)[1:-1]}')

        if browser_name.strip().lower() == 'firefox':
            web_driver_name: StrName = 'geckodriver'
        elif browser_name.strip().lower() == 'chrome':
            web_driver_name: StrName = 'chromedriver'

        if custom_path_to_web_drivers:
            path_to_browser_driver: StrFilePath = Path(custom_path_to_web_drivers, web_driver_name)
        else:
            check_do_have_web_drivers()
            path_to_browser_driver: StrFilePath = get_path_to_web_driver_file(web_driver_name)
        if 'linux' in platform or platform == 'darwin':  # Linux or MacOS
            os.chmod(path_to_browser_driver, 755)

        del web_driver_name  # Now we don't need this variable

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
                self.driver.set_window_size(2560, 1440)  # the bigger, the better. We not have limit in screen size
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

        driver: type[WebDriver]

    @wraps(WebDriver.get)
    def get(self, url: StrLink) -> None:
        self.driver.get(url=url)

    @wraps(WebDriver.refresh)
    def refresh(self):
        self.driver.refresh()

    @wraps(WebDriver.forward)
    def forward(self):
        self.driver.forward()

    @wraps(WebDriver.back)
    def back(self):
        self.driver.back()

    @wraps(WebDriver.quit)
    def quit(self):
        self.driver.quit()

    @wraps(WebDriver.close)
    def close(self):
        self.driver.close()

    @wraps(WebDriver.current_url)
    def current_url(self) -> StrLink:
        return self.driver.current_url

    @property
    @wraps(WebDriver.page_source)
    def page_source(self) -> str:
        return self.driver.page_source

    def wait_url_contains(self, url_part: str, where_wait: Optional[type[WebDriver]] = None, wait_time: int = 30) -> None:
        """
        Waits for url_part to be in url./Ждет когда url_part будет в url.


        :param url_part: the part of the url that is expected in the current url./часть URL-адреса, которая ожидается в
        текущем URL-адресе

        :param where_wait: Optional. subclasses WebDriver from selenium.webdriver.remote.webdriver.WebDriver. In this
        object will wait when url_part to appear in url. By default, where wait is a self.driver object./Необязательно.
        подклассы WebDriver из selenium.webdriver.remote.webdriver.WebDriver. В этом объекте будет ждать, когда url_part
        появится в url. По умолчанию where_wait это объект self.driver.

        :param wait_time: Optional. how long to wait in seconds. By default, 30/Необязательно. сколько ждать в секундах.
        По умолчанию, 30.
        """
        if not where_wait:
            where_wait = self.driver
        WebDriverWait(where_wait, wait_time).until(EC.url_contains(url_part))

    @wraps(WebDriver.__repr__)
    def __repr__(self):
        return self.driver.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.driver.quit()