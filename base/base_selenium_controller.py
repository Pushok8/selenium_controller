from functools import wraps
from typing import Union, Optional, ClassVar

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException
from seleniumwire.webdriver import Chrome, Remote, Firefox

from misc.proxy import Proxy
from misc.annotations import StrFilePath, StrLink, StrName, StrSocket, AnyWebDriver
from misc.exceptions import SuchBrowserIsNotSupportedError


class BaseSeleniumController:
    CHROME: ClassVar[str] = 'CHROME'
    FIREFOX: ClassVar[str] = 'FIREFOX'
    _web_driver_name: ClassVar[dict[StrName, StrName]] = {
        'CHROME': 'chromedriver',
        'FIREFOX': 'geckodriver'
    }

    def __init__(self,
                 web_driver: StrFilePath = None,
                 browser_name: str = 'CHROME',
                 options: Optional[Union[FirefoxOptions, ChromeOptions]] = None,
                 headless: bool = False,
                 use_remote_server: Optional[Union[StrSocket, bool]] = None,
                 proxy: Optional[Proxy] = None) -> None:
        """
        Defines by the passed arguments which driver should be created and with which options.

        If you pass in a FirefoxOptions or ChromeOptions object, it will be used to create the driver object, but
        additional arguments will be added to FirefoxOptions or ChromeOptions anyway.

        If you pass in a use_remote_server remote server socket, will be create Remote driver. Socket these are
        IP address and port separated by colon(IP_ADDRESS:PORT). For example: socket it is 127.0.0.1:4444

        If you pass in a proxy Proxy object, a proxy with the specified parameters will be used. Proxy can be with
        authorization and without this.
        /
        По переданным аргументам определяет, какой драйвер должен быть создан и с какими параметрами.

        Если вы передадите объект FirefoxOptions или ChromeOptions, он будет использоваться для создания объекта драйвера,
        но в любом случае дополнительные аргументы будут добавлены в FirefoxOptions или ChromeOptions.

        Если вы передадите удаленный серверный сокет use_remote_server, будет создан Remote драйвер. Сокет - это
        IP-адрес и порт, разделенные двоеточием (IP_ADDRESS:PORT). Например: сокет - это 127.0.0.1:4444

        Если вы передаете прокси-объект Прокси-объект, будет использоваться прокси с указанными параметрами. Прокси
        может быть с авторизация и без.


        :param web_driver: Absolute path to the browser driver. Driver can be obtained from the links:
          For Chrome: https://chromedriver.chromium.org/downloads
          For FireFox: https://github.com/mozilla/geckodriver/releases

        :param browser_name: By default - 'CHROME', can be 'CHROME' or 'FIREFOX'./По умолчанию - 'CHROME', может быть
          'CHROME' или 'FIREFOX'.

        :param options: Optional. FirefoxOptions or ChromeOptions depending on which browser you are using. It will be
          used to create the driver object, but additional arguments will be added to FirefoxOptions or ChromeOptions
          anyway./Необязательно. FirefoxOptions или ChromeOptions в зависимости от того, какой браузер вы используете.
          Это будет использоваться для создания объекта драйвера, но в любом случае дополнительные аргументы будут
          добавлены в FirefoxOptions или ChromeOptions.

        :param headless: Determines whether the browser will work with or without displaying the interface. If True
          without interface, if False with interface. By default - False./Определение будет ли работать браузер с
          отображением интерфейса или без. Если True без интерфейса, если False с интерфейсом. По умолчанию - False.

        :param use_remote_server: Optional. Bool value or server socket. If bool value is True - will be used
          127.0.0.1:4444./Необязательно. Значение bool или серверный сокет. Если значение bool равно True - будет
          использоваться 127.0.0.1:4444.

        :param proxy: Optional. Proxy object with the specified IP and port(and login and password if the proxy is with
          authorization). If you need authorization in your proxy, specify login and password in Proxy object. You can
          get Proxy object from the selenium_controller.misc.proxy module./Необязательно. Прокси-объект с указанными IP
          и port (и логином и паролем, если прокси с авторизацией). Если вам нужна  авторизация в вашем прокси, укажите
          логин и пароль в объекте Proxy. Вы можете получить объект Proxy из модуля selenium_controller.misc.proxy.
        """
        self.browser_name: StrName = browser_name

        if self.browser_name not in (self.CHROME, self.FIREFOX):
            raise SuchBrowserIsNotSupportedError(
                f"A browser such as {self.browser_name!r} does not support this controller. "
                f"Please specify one of these browser: "
                f"'{BaseSeleniumController.CHROME}', '{BaseSeleniumController.FIREFOX}'."
            )

        self.path_to_browser_driver: StrFilePath = web_driver

        desires_capabilities: dict = getattr(DesiredCapabilities, self.browser_name)

        self.driver: Union[Remote, Chrome, Firefox]
        self.options: Union[ChromeOptions, FirefoxOptions]
        if use_remote_server:
            self.driver = Remote

            if use_remote_server is True:
                self.remote_server: StrSocket = '127.0.0.1:4444'
            else:
                self.remote_server = use_remote_server

            if self.browser_name == BaseSeleniumController.FIREFOX:
                self.options = options or FirefoxOptions()
            elif self.browser_name == BaseSeleniumController.CHROME:
                self.options = options or ChromeOptions()
                self.options.add_argument('--disable-gpu')
                self.options.add_argument('--disable-dev-shm-usage')
                self.options.add_argument('--no-sandbox')
        else:
            if self.browser_name == BaseSeleniumController.FIREFOX:
                self.driver = Firefox
                self.options = options or FirefoxOptions()
            elif self.browser_name == BaseSeleniumController.CHROME:
                self.driver = Chrome
                self.options = options or ChromeOptions()
                self.options.add_argument('--disable-gpu')
                self.options.add_argument('--disable-dev-shm-usage')
                self.options.add_argument('--no-sandbox')

        self.options.headless = headless

        self.proxy = proxy
        if self.proxy:
            seleniumwire_options = {}

            proxy_address: str
            if self.proxy.login and self.proxy.password:
                proxy_address = (
                    f'https://{self.proxy.login}:{self.proxy.password}@{self.proxy.ip_v4_address}:{self.proxy.port}'
                )
                seleniumwire_options['proxy'] = {
                        'http': proxy_address,
                        'https': proxy_address
                }
            else:
                proxy_address = f'http://{self.proxy.ip_v4_address}:{self.proxy.port}'
                seleniumwire_options['proxy'] = {
                    'http': proxy_address,
                    'https': proxy_address
                }

            if self.driver is Remote:
                seleniumwire_options['addr'] = self.remote_server.split(':')[0]  # 127.0.0.1:4444 -> 127.0.0.1
                self.driver = self.driver(command_executor=f'http://{self.remote_server}/wd/hub',
                                          desired_capabilities=desires_capabilities,
                                          seleniumwire_options=seleniumwire_options,
                                          options=self.options)
            else:
                self.driver = self.driver(executable_path=self.path_to_browser_driver,
                                          desired_capabilities=desires_capabilities,
                                          seleniumwire_options=seleniumwire_options,
                                          options=self.options)
        else:
            if self.driver is Remote:
                self.driver = self.driver(command_executor=f'http://{self.remote_server}/wd/hub',
                                          desired_capabilities=desires_capabilities,
                                          seleniumwire_options={'addr': self.remote_server.split(':')[0]},
                                          options=self.options)
            else:
                if self.browser_name == BaseSeleniumController.CHROME:
                    try:
                        self.driver = self.driver(executable_path=self.path_to_browser_driver,
                                                  desired_capabilities=desires_capabilities,
                                                  options=self.options)
                    except SessionNotCreatedException:
                        raise SessionNotCreatedException(
                            'Your chrome browser is older than the web driver. Please update your browser or change'
                            ' the web driver to your version or lower. Download chrome web drivers here -> '
                            'https://chromedriver.chromium.org/downloads'
                        )
                elif self.browser_name == BaseSeleniumController.FIREFOX:
                    self.driver = self.driver(executable_path=self.path_to_browser_driver,
                                              desired_capabilities=desires_capabilities,
                                              seleniumwire_options={'port': 8080},
                                              options=self.options)
        self.driver.maximize_window()

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

    def wait_url_contains(self, url_part: str, where_wait: Optional[AnyWebDriver] = None, wait_time: int = 30) -> None:
        """
        Waits for url_part to be in url./Ждет когда url_part будет в url.


        :param url_part: The part of the url that is expected in the current url./Часть URL-адреса, которая ожидается в
        текущем URL-адресе.

        :param where_wait: Optional. Subclasses WebDriver from selenium.webdriver.remote.webdriver.WebDriver. In this
        object will wait when url_part to appear in url. By default, where wait is a self.driver object./Необязательно.
        Подклассы WebDriver из selenium.webdriver.remote.webdriver.WebDriver. В этом объекте будет ждать, когда url_part
        появится в url. По умолчанию where_wait это объект self.driver.

        :param wait_time: Optional. How long to wait in seconds. By default, 30./Необязательно. Сколько ждать в
        секундах. По умолчанию - 30.
        """
        where_wait = where_wait or self.driver
        WebDriverWait(where_wait, wait_time).until(EC.url_contains(url_part))

    @wraps(WebDriver.__repr__)
    def __repr__(self):
        return self.driver.__repr__()

    @wraps(WebDriver.__str__)
    def __str__(self):
        return self.driver.__str__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.driver.quit()
