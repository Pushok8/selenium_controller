from typing import Any, Union, Optional, overload

import pyperclip
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from misc.annotations import StrCSSSelector, AnyWebDriver
from base.base_selenium_controller import BaseSeleniumController


class SeleniumController(BaseSeleniumController):
    """
    It is a Selenium Controller which sticks to using a css-selectors to interact with a web elements. In all method
    these class used css selector. This class implements a simplified interface for interaction with selenium web
    driver, limited to short function names and polymorphic behavior. But also if you need to use methods that are not
    implemented here, you can use self.driver.
    /
    Это Selenium Controller, который придерживается использования css-селектора для взаимодействия с веб-элементами.
    Во всех методах этот класс использует css-селектор. Этот класс реализует упрощенный интерфейс взаимодействия с веб
    драйвером selenium, ограниченный короткими именами функций и полиморфное поведение. Но также если понадобиться
    использовать методы, которые здесь не реализованы, можно использовать self.driver.
    """
    def _define_web_element(
            self,
            web_element: Union[AnyWebDriver, WebElement, StrCSSSelector]
    ) -> Union[AnyWebDriver, WebElement]:
        """
        Handles web_element. If web_element is None, return self.driver, if web_element is css-selector return founded
        web element, if web_element is something else, returns it.
        /
        Обрабатывает web_element. Если web_element равен None, возвращает self.driver, если web_element является
        css-селектором, возвращает найденный веб-элемент, если web_element является чем-то другим, возвращает его.
        """
        if isinstance(web_element, str):
            return self.find(web_element)
        elif not web_element:
            return self.driver
        else:
            return web_element

    def _whether_to_search_for_web_element(self,
                                           web_element: Union[WebElement, StrCSSSelector],
                                           where_get_web_element: Union[AnyWebDriver, WebElement]) -> WebElement:
        if not isinstance(web_element, WebElement):
            where_get_web_element: Union[AnyWebDriver, WebElement] = self._define_web_element(where_get_web_element)
            web_element: WebElement = self.find(web_element, where_get_web_element)

        return web_element

    @overload
    def find(self, css_selector: StrCSSSelector) -> WebElement:
        ...

    @overload
    def find(self,
             css_selector: StrCSSSelector,
             where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    def find(self,
             css_selector: StrCSSSelector,
             where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Finds web element by css_selector in where_get_web_element web element or web driver. If where_get_web_element
        is css-selector, find it automatically. By default, where_get_web_element is self.driver.
        /
        Находит веб-элемент по css_selector в where_get_web_element веб-элементе или веб драйвере. Если
        where_get_web_element является css-селектором, находит его автоматически. По умолчанию, where_get_web_element -
        это self.driver.


        :param css_selector: css selector by which we find web element./css-селектор, по которому мы находим
        веб-элемент.

        :param where_get_web_element: Optional. In which WebDriver or WebElement we will be search for web element by
        css_selector. In the argument where_get_web_element you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element. By default, where_get_web_element is self.driver./Необязательно. В каком WebDriver
        или WebElement мы будем искать веб элемент по css_selector. В аргумент where_get_web_element вы можете передать
        экземпляр подкласса selenium.webdriver.remote.webdriver.WebDriver класс или
        selenium.webdriver.remote.webelement.WebElement или css_selector к веб-элементу. По умолчанию,
        where_get_web_element - это self.driver.

        :return: web element we found./веб-элемент, который мы нашли.
        """
        where_get_web_element: Union[AnyWebDriver, WebElement] = self._define_web_element(where_get_web_element)
        return where_get_web_element.find_element_by_css_selector(css_selector)

    @overload
    def finds(self, css_selector: StrCSSSelector) -> list[WebElement, ...]:
        ...

    @overload
    def finds(self,
              css_selector: StrCSSSelector,
              where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None
              ) -> list[WebElement, ...]:
        ...

    def finds(self,
              css_selector: StrCSSSelector,
              where_get_web_elements: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None
              ) -> list[WebElement, ...]:
        """
        Finds web elements by css_selector in where_get_web_element web element or web driver. If where_get_web_element
        is css-selector, find it automatically. By default, where_get_web_element is self.driver.
        /
        Находит веб-элементы по css_selector в where_get_web_element веб-элементе или веб драйвере. Если
        where_get_web_element является css-селектором, находит его автоматически. По умолчанию, where_get_web_element -
        это self.driver.


        :param css_selector: css selector by which we find web elements./css-селектор, по которому мы находим
        веб-элементы.

        :param where_get_web_elements: Optional. In which WebDriver or WebElement we will be search for web elements by
        css_selector. In the argument where_get_web_elements you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element. By default, where_get_web_element is self.driver./Необязательно. В каком WebDriver
        или WebElement мы будем искать веб элементы по css_selector. В аргумент where_get_web_elements вы можете
        передать экземплярподкласса selenium.webdriver.remote.webdriver.WebDriver класс или
        selenium.webdriver.remote.webelement.WebElement или css_selector к веб-элементу. По умолчанию,
        where_get_web_element - это self.driver

        :return: list of web elements found by css_selector./список веб-элементов, найденных по css-селектору.
        """
        where_get_web_elements: Union[AnyWebDriver, WebElement] = self._define_web_element(where_get_web_elements)
        return where_get_web_elements.find_elements_by_css_selector(css_selector)

    @overload
    def wait(self, web_element: Union[WebElement, StrCSSSelector], wait_time: int = 30) -> WebElement:
        ...

    @overload
    def wait(self,
             web_element: Union[WebElement, StrCSSSelector],
             wait_time: int = 30,
             where_wait: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    def wait(self,
             web_element: Union[WebElement, StrCSSSelector],
             wait_time: int = 30,
             where_wait: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Waits for the web_element object in the where_wait(by default is self.driver) object to be visible. "Visible"
        means that the visible object has a height and width more than 0 and is displayed in the browser.
        /
        Ожидает, пока объект web_element в объекте where_wait(по умолчанию, self.driver) станет видимым. «Видимый»
        означает, что видимый объект имеет высоту и ширину больше 0 и отображается в браузере.


        :param web_element: WebElement or css selector for the web element we will be waiting for./WebElement или
        css-селектор к веб-элементу который мы будем ждать.

        :param wait_time: Optional. How long to wait for web_element. By default, 30./Необязательно. Сколько ждать
        web_element. По умолчанию, 30.

        :param where_wait: Optional. In which WebDriver or WebElement we will be wait for web_element. In the argument
        where_wait you can pass an instance of a subclass of the selenium.webdriver.remote.webdriver.WebDriver class or
        selenium.webdriver.remote.webelement.WebElement or css-selector to web element. By default, where_wait is
        self.driver./Необязательно. В каком WebDriver или WebElement мы будем ждать web_element. В аргументе where_wait
        вы можете передать экземпляр подкласса класса selenium.webdriver.remote.webdriver.WebDriver или
        selenium.webdriver.remote.webelement.WebElement или css-селектор к веб-элементу. По умолчанию where_wait - это
        self.driver.

        :return: the web element we've been waiting for./веб-элемент, который мы ждали.
        """
        where_wait = self._define_web_element(where_wait)
        if isinstance(web_element, WebElement):
            web_element: WebElement = WebDriverWait(where_wait, wait_time).until(EC.visibility_of(web_element))
        else:
            web_element: WebElement = WebDriverWait(where_wait, wait_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, web_element)))

        return web_element

    @overload
    def wait_clickable(self, web_element: Union[WebElement, StrCSSSelector], wait_time: int = 30) -> WebElement:
        ...

    @overload
    def wait_clickable(self,
                       web_element: Union[WebElement, StrCSSSelector],
                       wait_time: int = 30,
                       where_wait: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    def wait_clickable(self,
                       web_element: Union[WebElement, StrCSSSelector],
                       wait_time: int = 30,
                       where_wait: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Waits for the web_element object in the where_wait(by default is self.driver) object to be clickable.
        /
        Ожидает, что объект web_element в объекте where_wait(по умолчанию, self.driver) будет кликабельным.


        :param web_element: WebElement or css-selector for the web element we will be waiting for./WebElement или
        css-селектор к веб-элементу который мы будем ждать.

        :param wait_time: Optional. How long to wait for web_element. By default, 30./Необязательно. Сколько ждать
        web_element. По умолчанию, 30.

        :param where_wait: Optional. In which WebDriver or WebElement we will be wait for web_element. In the argument
        where_wait you can pass an instance of a subclass of the selenium.webdriver.remote.webdriver.WebDriver class or
        selenium.webdriver.remote.webelement.WebElement or css-selector to web element. By default, where_wait is
        self.driver./Необязательно. В каком WebDriver или WebElement мы будем ждать web_element. В аргументе where_wait
        вы можете передать экземпляр подкласса класса selenium.webdriver.remote.webdriver.WebDriver или
        selenium.webdriver.remote.webelement.WebElement или css-селектор к веб-элементу. По умолчанию, where_wait - это
        self.driver.

        :return: the web element we've been waiting for./веб-элемент, который мы ждали.
        """
        where_wait = self._define_web_element(where_wait)
        if isinstance(web_element, WebElement):
            web_element: WebElement = WebDriverWait(where_wait, wait_time).until(
                lambda driver: web_element if web_element.is_displayed() else False if not EC.invisibility_of_element_located(web_element)(driver) else False
            )
        else:
            web_element: WebElement = WebDriverWait(where_wait, wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, web_element))
            )

        return web_element

    @overload
    def wait_hide(self, web_element: Union[WebElement, StrCSSSelector], wait_time: int = 30) -> WebElement:
        ...

    @overload
    def wait_hide(self,
                  web_element: Union[WebElement, StrCSSSelector],
                  wait_time: int = 30,
                  where_wait: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    def wait_hide(self,
                  web_element: Union[WebElement, StrCSSSelector],
                  wait_time: int = 30,
                  where_wait: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Waits for hide the web_element object in where_wait(by default is self.driver) object.
        /
        Ожидает скрытия объекта web_element в объекте where_wait(по умолчанию, self.driver).


        :param web_element: WebElement or css-selector for the web element we will be waiting for./WebElement или
        css-селектор к веб-элементу который мы будем ждать.

        :param wait_time: Optional. How long to wait for web_element. By default, 30./Необязательно. Сколько ждать
        web_element. По умолчанию, 30.

        :param where_wait: Optional. In which WebDriver or WebElement we will be wait for web_element. In the argument
        where_wait you can pass an instance of a subclass of the selenium.webdriver.remote.webdriver.WebDriver class or
        selenium.webdriver.remote.webelement.WebElement or css-selector to web element. By default, where_wait is
        self.driver./Необязательно. в каком WebDriver или WebElement мы будем ждать web_element. В аргументе where_wait
        вы можете передать экземпляр подкласса класса selenium.webdriver.remote.webdriver.WebDriver или
        selenium.webdriver.remote.webelement.WebElement или css-селектор к веб-элементу. По умолчанию, where_wait - это
        self.driver.

        :return: the web element we've been waiting for./веб-элемент, который мы ждали.
        """
        where_wait = self._define_web_element(where_wait)
        if not isinstance(web_element, WebElement):
            web_element = (By.CSS_SELECTOR, web_element)

        web_element: WebElement = WebDriverWait(where_wait, wait_time).until(EC.invisibility_of_element(web_element))

        return web_element

    @overload
    def hover_mouse(self, web_element: Union[WebElement, StrCSSSelector]) -> ActionChains:
        ...

    @overload
    def hover_mouse(self,
                    web_element: Union[WebElement, StrCSSSelector],
                    where_do_it: Optional[AnyWebDriver] = None) -> ActionChains:
        ...

    @overload
    def hover_mouse(self,
                    web_element: Union[WebElement, StrCSSSelector],
                    where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> ActionChains:
        ...

    @overload
    def hover_mouse(self,
                    web_element: Union[WebElement, StrCSSSelector],
                    where_do_it: Optional[AnyWebDriver] = None,
                    where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> ActionChains:
        ...

    def hover_mouse(self,
                    web_element: Union[WebElement, StrCSSSelector],
                    where_do_it: Optional[AnyWebDriver] = None,
                    where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> ActionChains:
        """
        Hovers the mouse over web_element in where_do_it web driver(by default, is self.driver). If
        web_element is a css selector, find it in where_get_web_element(by default, is self.driver), which is passed to the
        function. Returns an instance of the ActionChains class in which we hovered over the web_element.
        /
        Наводит указатель мышки на web_element в веб драйвере where_do_it(по умолчанию, self.driver). Если web_element
        является css-селектором, находит его в where_get_web_element(по умолчанию, self.driver), который передается в
        функцию. Возвращает экземпляр класса ActionChains, в котором мы навелись на web_element.


        :param web_element: WebElement or css selector for the web element on which we will hovered./WebElement или
        css-селектор к веб-элементу на который мы будем наводить курсор.

        :param where_do_it: Optional. An instance of a subclass of the selenium.webdriver.remote.webdriver.WebDriver
        class in which the ActionChains are executed. By default, where_do_it is self.driver./Необязательный. Экземпляр
        подкласса selenium.webdriver.remote.webdriver.WebDriver класс, в котором выполняются ActionChains. По умолчанию,
        where_do_it - это self.driver.

        :param where_get_web_element: Optional. In which WebDriver or WebElement we will be search for web_element if he
        is css-selector. In the argument where_get_web_element you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element. By default, where_get_web_element is self.driver./Необязательно. В каком WebDriver
        или WebElement мы будем искать web_element если он css-селектор. В аргументе where_get_web_element вы можете
        передать экземпляр подкласса класса selenium.webdriver.remote.webdriver.WebDriver или
        selenium.webdriver.remote.webelement.WebElement или css-селектор. По умолчанию, where_get_web_element - это
        self.driver.

        :return: The ActionChains instance in which we hovered the mouse to web_element./Экземпляр ActionChains, в
        котором мы навели мышь на web_element.
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        action_for_move_mouse: ActionChains = ActionChains(where_do_it or self.driver)
        action_for_move_mouse.move_to_element(web_element).perform()

        return action_for_move_mouse

    @overload
    def click(self, web_element: Union[WebElement, StrCSSSelector]) -> WebElement:
        ...

    @overload
    def click(self,
              web_element: Union[WebElement, StrCSSSelector],
              where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    def click(self,
              web_element: Union[WebElement, StrCSSSelector],
              where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Clicks on web_element in where_get_web_element(by default, is self.driver) web driver or web element. If
        web_element is a css selector, find it in where_get_web_element(by default, is self.driver), which is passed to the
        function. Returns the web_element we clicked on.
        /
        Нажимает на web_element в веб-драйвере или веб-элементе where_get_web_element. Если web_element является
        css-селектором, находит его в where_get_web_element(по умолчанию, self.driver), который передается в функцию.
        Возвращает веб-элемент, на который мы щелкнули.


        :param web_element: WebElement or css selector for the web element on which we will click on./WebElement или
        css-селектор к веб-элементу на который мы будем кликать.

        :param where_get_web_element: Optional. In which WebDriver or WebElement we will be search for web_element, if
        he is css-selector. In the argument where_get_web_element you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element. By default, where_get_web_element is self.driver./Необязательно. В каком WebDriver
        или WebElement мы будем искать web_element, если он css-селектор. В аргументе where_get_web_element вы можете
        передать экземпляр подкласса класса selenium.webdriver.remote.webdriver.WebDriver или
        selenium.webdriver.remote.webelement.WebElement или css-селектор. По умолчанию, where_get_web_element - это
        self.driver.

        :return: the web element we clicked on./веб элемент, на который мы нажали
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        web_element.click()

        return web_element

    @overload
    def scroll_on_element(self, web_element: Union[WebElement, StrCSSSelector]) -> WebElement:
        ...

    @overload
    def scroll_on_element(self,
                          web_element: Union[WebElement, StrCSSSelector],
                          where_scroll_on_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    @overload
    def scroll_on_element(self,
                          web_element: Union[WebElement, StrCSSSelector],
                          where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    @overload
    def scroll_on_element(self,
                          web_element: Union[WebElement, StrCSSSelector],
                          where_scroll_on_web_element: Optional[AnyWebDriver] = None,
                          where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    def scroll_on_element(self,
                          web_element: Union[WebElement, StrCSSSelector],
                          where_scroll_on_web_element: Optional[AnyWebDriver] = None,
                          where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Scrolls to a web_element in the passed web driver where_scroll_on_web_element(by default, is self.driver). If
        web_element is a css-selector, find it in where_get_web_element(by default, is self.driver), which is passed to
        the function. Returns the web element that we have scrolled to.
        /
        Прокручивает к web_element в переданном веб драйвере where_scroll_on_web_element(по умолчанию, self.driver).
        Если web_element является css-селектором, находит его в where_get_web_element(по умолчанию, self.driver),
        который передается в функцию. Возвращает веб-элемент, на который мы прокрутили.


        :param web_element: WebElement or css selector for the web element on which we will scrolled on./WebElement или
        css-селектор к веб-элементу на который мы будем прокручивать.

        :param where_scroll_on_web_element: in which web driver are we scrolling to web_element./в каком веб драйвере
        мы прокручиваем на web_element.

        :param where_get_web_element: Optional. In which WebDriver or WebElement we will be search for web_element if he
        is css-selector. In the argument where_get_web_element you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element. By default where_get_web_element, self.driver./Необязательно. в каком WebDriver
        или WebElement мы будем искать web_element если он css-селектор. В аргументе where_get_web_element вы можете
        передать экземпляр подкласса класса selenium.webdriver.remote.webdriver.WebDriver или
        selenium.webdriver.remote.webelement.WebElement или css-селектор. По умолчанию, where_get_web_element - это
        self.driver.

        :return: the web element we scrolled to./веб-элемент, к которому мы прокрутили.
        """
        web_driver: WebDriver = where_scroll_on_web_element or self.driver
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        web_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web_element)

        return web_element

    @overload
    def clear(self, web_element: Union[WebElement, StrCSSSelector]) -> WebElement:
        ...

    @overload
    def clear(self,
              web_element: Union[WebElement, StrCSSSelector],
              where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    def clear(self,
              web_element: Union[WebElement, StrCSSSelector],
              where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Clears text in the web_element in the passed web driver where_scroll_on_web_element(by default, is self.driver). If
        web_element is a css-selector, find it in where_get_web_element(by default, is self.driver), which is passed to the
        function. Returns the web element in which we have cleared the text.
        /
        Очищает текст в web_element в переданном веб драйвере where_scroll_on_web_element(по умолчанию, self.driver).
        Если web_element является css-селектором, находит его в where_get_web_element(по умолчанию, self.driver),
        который передается в функцию. Возвращает веб элемент, в котором мы очистили текст.


        :param web_element: WebElement or css selector for the web element in which we will clear the text./WebElement
        или css-селектор к веб-элементу в котором мы очистим тескт.

        :param where_get_web_element: Optional. In which WebDriver or WebElement we will be search for web_element if he
        is css-selector. In the argument where_get_web_element you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element. By default where_get_web_element, self.driver./Необязательно. в каком WebDriver
        или WebElement мы будем искать web_element если он css-селектор. В аргументе where_get_web_element вы можете
        передать экземпляр подкласса класса selenium.webdriver.remote.webdriver.WebDriver или
        selenium.webdriver.remote.webelement.WebElement или css-селектор. По умолчанию, where_get_web_element - это
        self.driver.

        :return: web element from which all have been removed./веб-элемент из которого удалили всё.
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        web_element.clear()
        web_element.send_keys(Keys.CONTROL + 'a')
        web_element.send_keys(Keys.DELETE)

        return web_element

    @overload
    def send_keys_clean(self, web_element: Union[WebElement, StrCSSSelector], what_to_send: Any) -> WebElement:
        ...

    @overload
    def send_keys_clean(self,
                        web_element: Union[WebElement, StrCSSSelector],
                        what_to_send: Any,
                        where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    def send_keys_clean(self,
                        web_element: Union[WebElement, StrCSSSelector],
                        what_to_send: Any,
                        where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Presses the keyboard shortcut Ctrl + a into the web_element in the passed web driver where_scroll_on_web_element
        (by default, is self.driver), then deletes all in the web_element and finally sends the what_to_send object into
        the web_element. If web_element is a css-selector, find it in where_get_web_element(by default, is self.driver),
        which is passed to the function. Returns the web element in which we send keys(send_keys argument).
        /
        Нажимает сочетание клавиш Ctrl + a в web_element в переданном веб-драйвере where_scroll_on_web_element
        (по умолчанию, self.driver), затем удаляет все в web_element и, наконец, отправляет объект what_to_send в
        web_element. Если web_element является css-селектором, найдите его в where_get_web_element (по умолчанию,
        self.driver), который передается в функцию. Возвращает веб-элемент, в котором мы отправляем ключи(send_keys
        аргумент).


        :param web_element: WebElement or css selector for the web element in which we will send keys(send_keys
        argument)./WebElement или css-селектор к веб-элементу в который мы отправим ключи(what_to_send аргумент).

        :param what_to_send: any object you can pass to selenium.webdriver.remote.webelement.WebElement.send_keys
        method./любой объект, который вы можете передать в selenium.webdriver.remote.webelement.WebElement.send_keys
        метод.

        :param where_get_web_element: Optional. In which WebDriver or WebElement we will be search for web_element if he
        is css-selector. In the argument where_get_web_element you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element. By default where_get_web_element, self.driver./Необязательно. в каком WebDriver
        или WebElement мы будем искать web_element если он css-селектор. В аргументе where_get_web_element вы можете
        передать экземпляр подкласса класса selenium.webdriver.remote.webdriver.WebDriver или
        selenium.webdriver.remote.webelement.WebElement или css-селектор. По умолчанию, where_get_web_element - это
        self.driver.

        :return: the web element to which what_to_send was sent./веб-элемент в который отправили what_to_send.
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        web_element.send_keys(Keys.CONTROL + 'a')
        web_element.send_keys(Keys.DELETE)
        web_element.send_keys(what_to_send)

        return web_element

    @overload
    def paste(self, web_element: Union[WebElement, StrCSSSelector], what_to_paste: Any) -> WebElement:
        ...

    @overload
    def paste(self,
              web_element: Union[WebElement, StrCSSSelector],
              what_to_paste: Any,
              where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        ...

    def paste(self,
              web_element: Union[WebElement, StrCSSSelector],
              what_to_paste: Any,
              where_get_web_element: Optional[Union[AnyWebDriver, WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Inserts what_to_paste into the web_element in the passed web driver where_scroll_on_web_element(by default, is
        self.driver). If web_element is a css-selector, find it in where_get_web_element(by default, is self.driver),
        which is passed to the function. Returns the web element in which we paste what_to_paste.
        /
        Вставляет what_to_paste в web_element в переданном веб-драйвере where_scroll_on_web_element (по умолчанию,
        self.driver). Если web_element является css-селектором, найдите его в where_get_web_element (по умолчанию,
        self.driver), который передается в функцию. Возвращает веб-элемент, в который мы вставляем what_to_paste.


        :param web_element: WebElement or css selector for the web element in which we will paste what_to_paste./
        WebElement или css-селектор к веб-элементу в который мы вставили what_to_paste.

        :param what_to_paste: any object that can be copied via the keyboard shortcuts Ctrl + C./любой объект, который
        можно скопировать через сочетания клавишь Ctrl + C.

        :param where_get_web_element: Optional. In which WebDriver or WebElement we will be search for web_element if he
        is css-selector. In the argument where_get_web_element you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element. By default where_get_web_element, self.driver./Необязательно. в каком WebDriver
        или WebElement мы будем искать web_element если он css-селектор. В аргументе where_get_web_element вы можете
        передать экземпляр подкласса класса selenium.webdriver.remote.webdriver.WebDriver или
        selenium.webdriver.remote.webelement.WebElement или css-селектор. По умолчанию, where_get_web_element - это
        self.driver.

        :return: the web element in which the what_to_paste was inserted./веб-элемент в который вставили what_to_paste.
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        pyperclip.copy(str(what_to_paste))
        web_element.send_keys(Keys.CONTROL + 'v')

        return web_element