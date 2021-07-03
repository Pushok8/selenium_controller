from typing import Any, Union, Optional, overload

import pyperclip
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from base.base_selenium_controller import BaseSeleniumController
from misc.annotations import StrXPath, AnyWebDriver


class SeleniumController(BaseSeleniumController):
    """
    It is a Selenium Controller which sticks to using a xpath to interact with a web elements. In all method
    these class used xpath. This class implements a simplified interface for interaction with selenium web driver,
    limited to short function names and polymorphic behavior. But also if you need to use methods that are not
    implemented here, you can use self.driver.
    /
    Это Selenium Controller, который придерживается использования xpath для взаимодействия с веб-элементами. Во всех
    методах этот класс использует xpath. Этот класс реализует упрощенный интерфейс взаимодействия с веб драйвером
    selenium, ограниченный короткими именами функций и полиморфное поведение. Но также если понадобиться использовать
    методы, которые здесь не реализованы, можно использовать self.driver.
    """
    def _whether_to_search_for_web_element(self,
                                           web_element: Union[WebElement, StrXPath],
                                           where_get_web_element: AnyWebDriver) -> WebElement:
        """
        Determines whether to look for web_element in the where_get_web_element web driver.
        /
        Определяет, искать ли web_element в where_get_web_element веб драйвере.
        """
        if not isinstance(web_element, WebElement):
            web_element: WebElement = self.find(web_element, where_get_web_element or self.driver)
        return web_element

    @overload
    def find(self, xpath: StrXPath) -> WebElement:
        ...

    @overload
    def find(self, xpath: StrXPath, where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    def find(self, xpath: StrXPath, where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        """
        Finds web element by xpath in where_get_web_element web driver(by default is self.driver).
        /
        Находит веб-элемент по xpath в веб-драйвере where_get_web_element(по умолчанию, self.driver).


        :param xpath: xpath by which we find web element./xpath, по которому мы находим веб-элемент.

        :param where_get_web_element: Optional. In which WebDriver we will be search for web element by xpath. By
        default, where_get_web_element is self.driver./Необязательно. В каком WebDriver мы будем искать веб элемент по
        xpath. По умолчанию, where_get_web_element - это self.driver.

        :return: web element we found./веб-элемент, который мы нашли.
        """
        where_get_web_element: AnyWebDriver = where_get_web_element or self.driver
        return where_get_web_element.find_element_by_xpath(xpath)

    @overload
    def finds(self, xpath: StrXPath) -> list[WebElement, ...]:
        ...

    @overload
    def finds(self, xpath: StrXPath, where_get_web_element: Optional[AnyWebDriver] = None) -> list[WebElement, ...]:
        ...

    def finds(self, xpath: StrXPath, where_get_web_element: Optional[AnyWebDriver] = None) -> list[WebElement, ...]:
        """
        Finds web elements by xpath in where_get_web_element web driver(by default is self.driver).
        /
        Находит веб-элементы по xpath в веб-драйвере where_get_web_element(по умолчанию, self.driver).


        :param xpath: xpath by which we find web elements./xpath, по которому мы находим веб-элементы.

        :param where_get_web_element: Optional. In which WebDriver we will be search for web elements by xpath. By
        default, where_get_web_element, self.driver./Необязательно. В каком WebDriver мы будем искать веб элементы по
        xpath. По умолчанию, where_get_web_element - это self.driver.

        :return: list of web elements found by xpath./список веб-элементов, найденных по xpath.
        """
        where_get_web_element: AnyWebDriver = where_get_web_element or self.driver
        return where_get_web_element.find_elements_by_xpath(xpath)

    @overload
    def wait(self,
             web_element: Union[WebElement, StrXPath],
             wait_time: int = 30) -> WebElement:
        ...

    @overload
    def wait(self,
             web_element: Union[WebElement, StrXPath],
             wait_time: int = 30,
             where_wait: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    def wait(self,
             web_element: Union[WebElement, StrXPath],
             wait_time: int = 30,
             where_wait: Optional[AnyWebDriver] = None) -> WebElement:
        """
        Waits for the web_element object in the where_wait(by default is self.driver) object to be visible. "Visible"
        means that the visible object has a height and width more than 0 and is displayed in the browser.
        /
        Ожидает, пока объект web_element в объекте where_wait(по умолчанию, self.driver) станет видимым. «Видимый»
        означает, что видимый объект имеет высоту и ширину больше 0 и отображается в браузере.


        :param web_element: WebElement or xpath for the web element we will be waiting for./WebElement или xpath к
        веб-элементу который мы будем ждать.

        :param wait_time: Optional. How long to wait for web_element. By default, 30./Необязательно. Сколько ждать
        web_element. По умолчанию, 30.

        :param where_wait: Optional. An instance of a subclass(or the class itself) of the
        selenium.webdriver.remote.webdriver.WebDriver class in which we wait web_element. By default where_wait,
        self.driver./Необязательный. Экземпляр подкласса(или самого класса)
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором мы ждём web_element. По умолчанию, where_wait -
        это self.drive.

        :return: the web element we've been waiting for./веб-элемент, который мы ждали.
        """
        if isinstance(web_element, WebElement):
            web_element: WebElement = WebDriverWait(where_wait or self.driver, wait_time).until(
                EC.visibility_of(web_element)
            )
        else:
            web_element: WebElement = WebDriverWait(where_wait or self.driver, wait_time).until(
                EC.visibility_of_element_located((By.XPATH, web_element)))

        return web_element

    @overload
    def wait_clickable(self,
                       web_element: Union[WebElement, StrXPath],
                       wait_time: int = 30) -> WebElement:
        ...

    @overload
    def wait_clickable(self,
                       web_element: Union[WebElement, StrXPath],
                       wait_time: int = 30,
                       where_wait: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    def wait_clickable(self,
                       web_element: Union[WebElement, StrXPath],
                       wait_time: int = 30,
                       where_wait: Optional[AnyWebDriver] = None) -> WebElement:
        """
        Waits for the web_element object in the where_wait(by default is self.driver) object to be clickable.
        /
        Ожидает, что объект web_element в объекте where_wait(по умолчанию, self.driver) будет кликабельным.


        :param web_element: WebElement or xpath for the web element we will be waiting for./WebElement или xpath к
        веб-элементу который мы будем ждать.

        :param wait_time: Optional. how long to wait for web_element. By default, 30./Необязательно. сколько ждать
        web_element. По умолчанию, 30.

        :param where_wait: Optional. An instance of a subclass(or the class itself) of the
        selenium.webdriver.remote.webdriver.WebDriver class in which we wait web_element. By default where_wait,
        self.driver./Необязательный. Экземпляр подкласса(или самого класса)
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором мы ждём web_element. По умолчанию, where_wait -
        это self.drive.

        :return: the web element we've been waiting for./веб-элемент, который мы ждали.
        """
        if isinstance(web_element, WebElement):
            web_element: WebElement = WebDriverWait(where_wait or self.driver, wait_time).until(
                self._get_element_if_displayed(web_element)
            )
        else:
            web_element: WebElement = WebDriverWait(where_wait or self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, web_element))
            )

        return web_element

    @overload
    def wait_hide(self,
                  web_element: Union[WebElement, StrXPath],
                  wait_time: int = 30) -> WebElement:
        ...

    @overload
    def wait_hide(self,
                  web_element: Union[WebElement, StrXPath],
                  wait_time: int = 30,
                  where_wait: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    def wait_hide(self,
                  web_element: Union[WebElement, StrXPath],
                  wait_time: int = 30,
                  where_wait: Optional[AnyWebDriver] = None) -> WebElement:
        """
        Waits for hide the web_element object in where_wait(by default is self.driver) object.
        /
        Ожидает скрытия объекта web_element в объекте where_wait(по умолчанию, self.driver).


        :param web_element: WebElement or xpath for the web element we will be waiting for./WebElement или xpath к
        веб-элементу который мы будем ждать.

        :param wait_time: Optional. how long to wait for web_element. By default, 30./Необязательно. сколько ждать
        web_element. По умолчанию, 30.

        :param where_wait: Optional. An instance of a subclass(or the class itself) of the
        selenium.webdriver.remote.webdriver.WebDriver class in which we wait web_element. By default where_wait,
        self.driver./Необязательный. Экземпляр подкласса(или самого класса)
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором мы ждём web_element. По умолчанию, where_wait -
        это self.drive.

        :return: the web element we've been waiting for./веб-элемент, который мы ждали.
        """
        if not isinstance(web_element, WebElement):
            web_element: tuple[str, WebElement] = (By.XPATH, web_element)

        web_element: WebElement = WebDriverWait(where_wait or self.driver, wait_time).until(
            EC.invisibility_of_element(web_element)
        )

        return web_element

    @overload
    def hover_mouse(self, web_element: Union[WebElement, StrXPath]) -> ActionChains:
        ...

    @overload
    def hover_mouse(self,
                    web_element: Union[WebElement, StrXPath],
                    where_do_it: Optional[AnyWebDriver] = None) -> ActionChains:
        ...

    @overload
    def hover_mouse(self,
                    web_element: Union[WebElement, StrXPath],
                    where_get_web_element: Optional[AnyWebDriver] = None) -> ActionChains:
        ...

    @overload
    def hover_mouse(self,
                    web_element: Union[WebElement, StrXPath],
                    where_do_it: Optional[AnyWebDriver] = None,
                    where_get_web_element: Optional[AnyWebDriver] = None) -> ActionChains:
        ...

    def hover_mouse(self,
                    web_element: Union[WebElement, StrXPath],
                    where_do_it: Optional[AnyWebDriver] = None,
                    where_get_web_element: Optional[AnyWebDriver] = None) -> ActionChains:
        """
        Hovers the mouse over web_element in where_do_it web driver(by default, is self.driver). If
        web_element is a xpath, find it in where_get_web_element(by default, self.driver), which is passed to the
        function. Returns an instance of the ActionChains class in which we hovered over the web_element.
        /
        Наводит указатель мышки на web_element в веб драйвере where_do_it(по умолчанию self.driver). Если web_element
        является xpath, находит его в where_get_web_element(по умолчанию, self.driver), который передается в
        функцию. Возвращает экземпляр класса ActionChains, в котором мы навелись на web_element.


        :param web_element: WebElement or xpath for the web element on which we will hovered./WebElement или
        xpath к веб-элементу на который мы будем наводить курсор.

        :param where_do_it: Optional. An instance of a subclass of the selenium.webdriver.remote.webdriver.WebDriver
        class in which the ActionChains are executed. By default where_do_it, self.driver./Необязательный. экземпляр
        подкласса selenium.webdriver.remote.webdriver.WebDriver класс, в котором выполняются ActionChains. По умолчанию,
        where_do_it - это self.drive.

        :param where_get_web_element: Optional. An instance of a subclass of a class
        selenium.webdriver.remote.webdriver.WebDriver in which we are looking for web_element. Default
        where_get_web_element, self.driver./Необязательный. экземпляр подкласса
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором мы ищем web_element. По умолчанию,
        where_get_web_element - это self.driver.

        :return: The ActionChains instance in which we hovered the mouse to web_element./Экземпляр ActionChains, в
        котором мы навели мышь на web_element
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        action_for_move_mouse: ActionChains = ActionChains(where_do_it or self.driver)
        action_for_move_mouse.move_to_element(web_element).perform()

        return action_for_move_mouse

    @overload
    def click(self, web_element: Union[WebElement, StrXPath]) -> WebElement:
        ...

    @overload
    def click(self,
              web_element: Union[WebElement, StrXPath],
              where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    def click(self,
              web_element: Union[WebElement, StrXPath],
              where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        """
        Clicks on web_element in where_click web driver. If web_element is a xpath, find it in where_get_web_element
        (by default, self.driver), which is passed to the function. Returns the web_element we clicked on.
        /
        Нажимает на web_element в веб-драйвере where_click. Если веб элемент xpath, найдет его в where_get_web_element
        (по умолчанию, self.driver), которая передается в функцию. Возвращает веб-элемент, на который мы щелкнули.


        :param web_element: WebElement or xpath for the web element on which we will click on./WebElement или xpath к
        веб-элементу на который мы будем кликать.

        :param where_get_web_element: Optional. An instance of a subclass of a class
        selenium.webdriver.remote.webdriver.WebDriver in which we are looking for web_element. Default
        where_get_web_element, self.driver./Необязательный. экземпляр подкласса
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором мы ищем web_element. По умолчанию,
        where_get_web_element - это self.driver.

        :return: the web element we clicked on./веб элемент, на который мы нажали.
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        web_element.click()

        return web_element

    @overload
    def scroll_on_element(self, web_element: Union[WebElement, StrXPath]) -> WebElement:
        ...

    @overload
    def scroll_on_element(self,
                          web_element: Union[WebElement, StrXPath],
                          where_scroll_on_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    @overload
    def scroll_on_element(self,
                          web_element: Union[WebElement, StrXPath],
                          where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    @overload
    def scroll_on_element(self,
                          web_element: Union[WebElement, StrXPath],
                          where_scroll_on_web_element: Optional[AnyWebDriver] = None,
                          where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    def scroll_on_element(self,
                          web_element: Union[WebElement, StrXPath],
                          where_scroll_on_web_element: Optional[AnyWebDriver] = None,
                          where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        """
        Scrolls to a web_element in the passed web driver where_scroll_on_web_element(by default, is self.driver). If
        web_element is a xpath, find it in where_get_web_element(by default, is self.driver), which is passed to the
        function. Returns the web element that we have scrolled to.
        /
        Прокручивает к web_element в переданном веб драйвере where_scroll_on_web_element(по умолчанию, self.driver).
        Если web_element является xpath, находит его в where_get_web_element(по умолчанию, self.driver), который
        передается в функцию. Возвращает веб-элемент, на который мы прокрутили.


        :param web_element: WebElement or xpath for the web element on which we will scrolled on./WebElement или xpath к
        веб-элементу на который мы будем прокручивать.

        :param where_scroll_on_web_element: in which web driver are we scrolling to web_element./в каком веб драйвере
        мы прокручиваем на web_element.

        :param where_get_web_element: Optional. An instance of a subclass of a class
        selenium.webdriver.remote.webdriver.WebDriver in which we are looking for web_element. Default
        where_get_web_element, self.driver./Необязательный. экземпляр подкласса
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором мы ищем web_element. По умолчанию,
        where_get_web_element - это self.driver.

        :return: the web element we scrolled to./веб-элемент, к которому мы прокрутили.
        """
        web_driver: WebDriver = where_scroll_on_web_element or self.driver
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        web_driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web_element)

        return web_element

    @overload
    def clear(self, web_element: Union[WebElement, StrXPath]) -> WebElement:
        ...

    @overload
    def clear(self,
              web_element: Union[WebElement, StrXPath],
              where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    def clear(self,
              web_element: Union[WebElement, StrXPath],
              where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        """
        Clears text in the web_element in the passed web driver where_scroll_on_web_element(by default, is self.driver).
        If web_element is a xpath, find it in where_get_web_element(by default, is self.driver), which is passed to the
        function. Returns the web element in which we have cleared the text.
        /
        Очищает текст в web_element в переданном веб драйвере where_scroll_on_web_element(по умолчанию, self.driver).
        Если web_element является xpath, находит его в where_get_web_element(по умолчанию, self.driver),
        который передается в функцию. Возвращает веб элемент, в котором мы очистили текст.


        :param web_element: WebElement or xpath for the web element in which we will clear the text./WebElement или
        xpath к веб-элементу в котором мы очистим текст.

        :param where_get_web_element: Optional. An instance of a subclass of a class
        selenium.webdriver.remote.webdriver.WebDriver in which we are looking for web_element. Default
        where_get_web_element, self.driver./Необязательный. экземпляр подкласса
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором мы ищем web_element. По умолчанию,
        where_get_web_element - это self.driver.

        :return: web element from which all have been removed./веб-элемент из которого удалили всё.
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        web_element.clear()
        web_element.send_keys(Keys.CONTROL + 'a')
        web_element.send_keys(Keys.DELETE)

        return web_element

    @overload
    def send_keys_clean(self, web_element: Union[WebElement, StrXPath], what_to_send: Any) -> WebElement:
        ...

    @overload
    def send_keys_clean(self,
                        web_element: Union[WebElement, StrXPath],
                        what_to_send: Any,
                        where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    def send_keys_clean(self,
                        web_element: Union[WebElement, StrXPath],
                        what_to_send: Any,
                        where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        """
        Presses the keyboard shortcut Ctrl + a into the web_element in the passed web driver where_scroll_on_web_element
        (by default, is self.driver), then deletes all in the web_element and finally sends the what_to_send object into
        the web_element. If web_element is a xpath, find it in where_get_web_element(by default, is self.driver),
        which is passed to the function. Returns the web element in which we send keys(send_keys argument).
        /
        Нажимает сочетание клавиш Ctrl + a в web_element в переданном веб-драйвере where_scroll_on_web_element
        (по умолчанию, self.driver), затем удаляет все в web_element и, наконец, отправляет объект what_to_send в
        web_element. Если web_element является xpath, найдите его в where_get_web_element (по умолчанию,
        self.driver), который передается в функцию. Возвращает веб-элемент, в котором мы отправляем ключи(send_keys
        аргумент).


        :param web_element: WebElement or css selector for the web element in which we will send keys(send_keys
        argument)./WebElement или xpath к веб-элементу в который мы отправим ключи(what_to_send аргумент).

        :param what_to_send: any object you can pass to selenium.webdriver.remote.webelement.WebElement.send_keys
        method./любой объект, который вы можете передать в selenium.webdriver.remote.webelement.WebElement.send_keys
        метод.

        :param where_get_web_element: Optional. An instance of a subclass of a class
        selenium.webdriver.remote.webdriver.WebDriver in which we are looking for web_element. Default
        where_get_web_element, self.driver./Необязательный. экземпляр подкласса
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором мы ищем web_element. По умолчанию,
        where_get_web_element - это self.driver.

        :return: the web element to which what_to_send was sent./веб-элемент в который отправили what_to_send.
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        web_element.send_keys(Keys.CONTROL + 'a')
        web_element.send_keys(Keys.DELETE)
        web_element.send_keys(what_to_send)

        return web_element

    @overload
    def paste(self, web_element: Union[WebElement, StrXPath], what_to_paste: Any) -> WebElement:
        ...

    @overload
    def paste(self,
              web_element: Union[WebElement, StrXPath],
              what_to_paste: Any,
              where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        ...

    def paste(self,
              web_element: Union[WebElement, StrXPath],
              what_to_paste: Any,
              where_get_web_element: Optional[AnyWebDriver] = None) -> WebElement:
        """
        Inserts what_to_paste into the web_element in the passed web driver where_scroll_on_web_element(by default, is
        self.driver). If web_element is a xpath, find it in where_get_web_element(by default, is self.driver),
        which is passed to the function. Returns the web element in which we paste what_to_paste.
        /
        Вставляет what_to_paste в web_element в переданном веб-драйвере where_scroll_on_web_element (по умолчанию,
        self.driver). Если web_element является xpath, найдите его в where_get_web_element (по умолчанию,
        self.driver), который передается в функцию. Возвращает веб-элемент, в который мы вставляем what_to_paste.


        :param web_element: WebElement or xpath for the web element in which we will paste what_to_paste./
        WebElement или xpath к веб-элементу в который мы вставили what_to_paste.

        :param what_to_paste: any object that can be copied via the keyboard shortcuts Ctrl + C./любой объект, который
        можно скопировать через сочетания клавиш Ctrl + C.

        :param where_get_web_element: Optional. An instance of a subclass of a class
        selenium.webdriver.remote.webdriver.WebDriver in which we are looking for web_element. Default
        where_get_web_element, self.driver./Необязательный. экземпляр подкласса
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором мы ищем web_element. По умолчанию,
        where_get_web_element - это self.driver.

        :return: the web element in which the what_to_paste was inserted./веб-элемент в который вставили what_to_paste.
        """
        web_element: WebElement = self._whether_to_search_for_web_element(web_element, where_get_web_element)

        pyperclip.copy(str(what_to_paste))
        web_element.send_keys(Keys.CONTROL + 'v')

        return web_element
