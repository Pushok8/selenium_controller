from typing import Any, Union, Optional

import pyperclip
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from base.base_selenium_controller import BaseSeleniumController
from misc.annotations import StrCSSSelector


class SeleniumController(BaseSeleniumController):
    """
    It is a Selenium Controller which sticks to using a css selector to find a web element. In all method these class
    used css selector. This class implements a simplified interface for interaction with selenium web driver, limited
    to short function names and polymorphic behavior. But also if you need to use methods that are not implemented here,
    you can use self.driver
    /
    Это Selenium Controller, который придерживается использования css-селектора для поиска веб-элемента. Во всех методах этот класс
    использовал css-selector. Этот класс реализует упрощенный интерфейс взаимодействия с веб драйвером селениума,
    ограниченный короткими именами функций и полиморфное поведение. Но также если понадобиться использовать методы,
    которые здесь не реализованы, можно использовать self.driver.
    """
    def _define_web_element(self, web_element: Union[type[WebDriver], WebElement, StrCSSSelector]) -> Union[type[WebDriver], WebElement]:
        """
        Handles web_element if web_element is None, return self.driver, if web_element is css selector return founded
        web element, if web_element is something else, returns it.
        /
        Обрабатывает web_element, если web_element равен None, возвращает self.driver, если web_element является
        css-селектором, возвращает найденный веб-элемент, если web_element является чем-то другим, возвращает его.
        """
        if isinstance(web_element, str):
            return self.find(web_element)
        elif not web_element:
            return self.driver
        else:
            return web_element

    def find(self,
             css_selector: StrCSSSelector,
             where_get_web_element: Optional[Union[type[WebDriver], WebElement, StrCSSSelector]] = None) -> WebElement:
        """
        Finds web element by css_selector in where_get_web_element, by default where_get_web_element is self.driver.
        /
        Находит веб-элемент по css_selector в where_get_web_element, по умолчанию where_get_web_element - это self.driver.


        :param css_selector: css selector by which we find web element./css-селектор, по которому мы находим веб-элемент.

        :param where_get_web_element: Optional. In which WebDriver or WebElement we will be search for web_element. In
        the argument where_get_web_element you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element. By default, where_get_web_element is self.driver./Необязательный. В каком WebDriver
        или WebElement мы будем искать web_element. В аргумент where_get_web_element вы можете передать экземпляр
        подкласса elenium.webdriver.remote.webdriver.WebDriver класс или selenium.webdriver.remote.webelement.WebElement
        или css_selector в веб-элемент. По умолчанию, where_get_web_element - это self.driver

        :return: web element we found./веб-элемент, который мы нашли.
        """
        where_get_web_element: Union[type[WebDriver], WebElement] = self._define_web_element(where_get_web_element)
        return where_get_web_element.find_element_by_css_selector(css_selector)

    def finds(self,
              css_selector: StrCSSSelector,
              where_get_web_element: Optional[Union[type[WebDriver], WebElement, StrCSSSelector]] = None) -> list[WebElement, ...]:
        """
        Finds web elements by css_selector in where_get_web_element, by default where_get_web_element is self.driver.
        /
        Находит веб-элементы по css_selector в where_get_web_element, по умолчанию where_get_web_element - это self.driver.


        :param css_selector: css selector by which we find web elements./css-селектор, по которому мы находим веб-элементы.

        :param where_get_web_element: Optional. In which WebDriver or WebElement we will be search for web_element. In
        the argument where_get_web_element you can pass an instance of a subclass of the
        selenium.webdriver.remote.webdriver.WebDriver class or selenium.webdriver.remote.webelement.WebElement or
        css_selector to web element.By default, where_get_web_element is self.driver./Необязательный. В каком WebDriver или WebElement мы будем искать web_element. В
        аргумент where_get_web_element вы можете передать экземпляр подкласса elenium.webdriver.remote.webdriver.WebDriver
        класс или selenium.webdriver.remote.webelement.WebElement или css_selector в веб-элемент. По умолчанию,
        where_get_web_element - это self.driver

        :return: list of web elements found by css_selector./список веб-элементов, найденных css_selector.
        """
        where_get_web_element: Union[type[WebDriver], WebElement] = self._define_web_element(where_get_web_element)
        return where_get_web_element.find_elements_by_css_selector(css_selector)

    def wait(self,
             web_element: Union[WebElement, StrCSSSelector],
             where_wait: Optional[Union[type[WebDriver], WebElement, StrCSSSelector]] = None,
             wait_time: int = 30) -> WebElement:
        """
        Waits for the web_element object in the where_wait object to be visible. "Visible" means that the visible
        object has a height and width more than 0 and is displayed in the browser.
        /
        Ожидает, пока объект web_element в объекте where_wait станет видимым. «Видимый» означает, что видимый объект
        имеет высоту и ширину больше 0 и отображается в браузере.


        :param web_element: it is may be WebElement or css_selector to web_element./это может быть WebElement или
        css_selector к web_element.

        :param where_wait: Optional. In which WebDriver or WebElement we will be wait for web_element. In the argument
        where_wait you can pass an instance of a subclass of the selenium.webdriver.remote.webdriver.WebDriver class or
        selenium.webdriver.remote.webelement.WebElement or css_selector to web element./Необязательно. в каком WebDriver
        или WebElement мы будем ждать web_element. В аргументе where_wait вы можете передать экземпляр подкласса класса
        selenium.webdriver.remote.webdriver.WebDriver или selenium.webdriver.remote.webelement.WebElement или
        css_selector в веб-элемент.

        :param wait_time: Optional. how long to wait for web_element. By default, 30./Необязательно. сколько ждать
        web_element. По умолчанию, 30.

        :return: the web element we've been waiting for./веб-элемент, который мы ждали.
        """
        where_wait = self._define_web_element(where_wait)
        if isinstance(web_element, WebElement):
            web_element: WebElement = WebDriverWait(where_wait, wait_time).until(EC.visibility_of(web_element))
        else:
            web_element: WebElement = WebDriverWait(where_wait, wait_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, web_element)))

        return web_element

    def wait_clickable(self,
                       web_element: Union[WebElement, StrCSSSelector],
                       where_wait: Optional[Union[type[WebDriver], WebElement, StrCSSSelector]] = None,
                       wait_time: int = 30) -> WebElement:
        """
        Waits for the web_element object in the where_wait object to be clickable.
        /
        Ожидает, что объект web_element в объекте where_wait будет кликабельным.


        :param web_element: it is may be WebElement or css_selector to web_element./это может быть WebElement или
        css_selector к web_element.

        :param where_wait: Optional. In which WebDriver or WebElement we will be wait for web_element. In the argument
        where_wait you can pass an instance of a subclass of the selenium.webdriver.remote.webdriver.WebDriver class or
        selenium.webdriver.remote.webelement.WebElement or css_selector to web element./Необязательно. в каком WebDriver
        или WebElement мы будем ждать web_element. В аргументе where_wait вы можете передать экземпляр подкласса класса
        selenium.webdriver.remote.webdriver.WebDriver или selenium.webdriver.remote.webelement.WebElement или
        css_selector в веб-элемент.

        :param wait_time: Optional. how long to wait for web_element. By default, 30./Необязательно. сколько ждать
        web_element. По умолчанию, 30.

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

    def wait_hide(self,
                  web_element: Union[WebElement, StrCSSSelector],
                  where_wait: Optional[Union[type[WebDriver], WebElement, StrCSSSelector]] = None,
                  wait_time: int = 30) -> WebElement:
        """
        Waits for hide the web_element object in where_wait object.
        /
        Ожидает скрытия объекта web_element в объекте where_wait


        :param web_element: it is may be WebElement or css_selector to web_element./это может быть WebElement или
        css_selector к web_element.

        :param where_wait: Optional. In which WebDriver or WebElement we will be wait for web_element. In the argument
        where_wait you can pass an instance of a subclass of the selenium.webdriver.remote.webdriver.WebDriver class or
        selenium.webdriver.remote.webelement.WebElement or css_selector to web element./Необязательно. в каком WebDriver
        или WebElement мы будем ждать web_element. В аргументе where_wait вы можете передать экземпляр подкласса класса
        selenium.webdriver.remote.webdriver.WebDriver или selenium.webdriver.remote.webelement.WebElement или
        css_selector в веб-элемент.

        :param wait_time: Optional. how long to wait for web_element. By default, 30./Необязательно. сколько ждать
        web_element. По умолчанию, 30.

        :return: the web element we've been waiting for./веб-элемент, который мы ждали.
        """
        where_wait = self._define_web_element(where_wait)
        if not isinstance(web_element, WebElement):
            web_element = (By.CSS_SELECTOR, web_element)
        web_element: WebElement = WebDriverWait(where_wait, wait_time).until(EC.invisibility_of_element(web_element))
        return web_element

    def hover_mouse(self,
                    web_element: Union[WebElement, StrCSSSelector],
                    where_do_it: Optional[type[WebDriver]] = None) -> ActionChains:
        """
        Hovers the mouse over web_element in where_do_it WebDriver.
        /
        Наводит указатель мышки на web_element в where_do_it WebDriver.


        :param web_element: it is may be WebElement or css_selector to web_element./это может быть WebElement или
        css_selector к web_element.

        :param where_do_it: Optional. An instance of a subclass of the selenium.webdriver.remote.webdriver.WebDriver
        class in which the ActionChains are executed./Необязательный. экземпляр подкласса
        selenium.webdriver.remote.webdriver.WebDriver класс, в котором выполняются ActionChains.

        :return: The ActionChains instance in which we hovered the mouse to web_element./Экземпляр ActionChains, в котором
        мы навели мышь на web_element
        """
        web_element: WebElement = self._define_web_element(web_element)
        action_for_move_mouse: ActionChains = ActionChains(where_do_it or self.driver)
        action_for_move_mouse.move_to_element(web_element).perform()
        return action_for_move_mouse

    def scroll_on_element(self, web_element: Union[WebElement, StrCSSSelector]) -> WebElement:
        """
        Scrolls to a web element.
        /
        Прокручивает к веб-элементу.


        :param web_element: it is may be WebElement or css_selector to web_element./это может быть WebElement или
        css_selector к web_element.

        :return: the web element we scrolled to./веб-элемент, к которому мы прокрутили.
        """
        web_element: WebElement = self._define_web_element(web_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web_element)
        return web_element

    def clear(self, web_element: Union[WebElement, StrCSSSelector]) -> WebElement:
        """
        Clears text in the web_element.
        /
        Удаляет текст в web_element.


        :param web_element: it is may be WebElement or css_selector to web_element./это может быть WebElement или
        css_selector к web_element.

        :return: web element from which all have been removed./веб-элемент из которого удалили всё.
        """
        web_element: WebElement = self._define_web_element(web_element)
        web_element.clear()
        web_element.send_keys(Keys.CONTROL + 'a')
        web_element.send_keys(Keys.DELETE)
        return web_element

    def send_keys_clean(self, web_element: Union[WebElement, StrCSSSelector], what_to_send: Any) -> WebElement:
        """
        Presses the keyboard shortcut Ctrl + a into the web_element object, then deletes all and finally sends the
        what_to_send object.
        /
        Нажимает сочетание клавиш Ctrl + a в объекте web_element, затем удаляет все и, наконец,
        отправляет объект what_to_send.


        :param web_element: it is may be WebElement or css_selector to web_element./это может быть WebElement или
        css_selector к web_element.

        :param what_to_send: any object you can pass to selenium.webdriver.remote.webelement.WebElement.send_keys method./
        любой объект, который вы можете передать в selenium.webdriver.remote.webelement.WebElement.send_keys метод

        :return: the web element to which what_to_send was sent./веб-элемент в который отправили what_to_send.
        """
        web_element: WebElement = self._define_web_element(web_element)
        web_element.send_keys(Keys.CONTROL + 'a')
        web_element.send_keys(Keys.DELETE)
        web_element.send_keys(what_to_send)
        return web_element

    def paste(self, web_element: Union[WebElement, StrCSSSelector], what_to_paste: Any) -> WebElement:
        """
        Inserts what_to_paste into web_element.
        /
        Вставляет what_to_paste в web_element.


        :param web_element: it is may be WebElement or css_selector to web_element./это может быть WebElement или
        css_selector к web_element.

        :param what_to_paste: any object that can be copied via the keyboard shortcuts Ctrl + C./любой объект, который
        можно скопировать через сочетания клавишь Ctrl + C

        :return: the web element in which the what_to_paste was inserted./веб-элемент в который вставили what_to_paste.
        """
        web_element: WebElement = self._define_web_element(web_element)
        pyperclip.copy(str(what_to_paste))
        web_element.send_keys(Keys.CONTROL + 'v')
        return web_element