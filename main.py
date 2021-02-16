from selenium_controllers.css_selenium_controller import SeleniumController


a = SeleniumController('Firefox')
a.driver.get('https://google.com/')

obj = a.wait('input', where_wait='div.FPdoLc.tfB0Bf')
print(obj.get_property('value'))
# a.find('.gb_D').click()
# a.driver.switch_to.frame(a.find('.gb_Zd > div:nth-child(3) > iframe:nth-child(1)'))
# input()
# obj = a.wait('div.qWuU9c>div.EHzcec', where_wait=a.find('div.kFwPee[jsname="qJTHM"]'))

