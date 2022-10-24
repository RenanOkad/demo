import os
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
firefox_driver = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
firefox_service = Service(firefox_driver)
firefox_options = Options()
firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
firefox_options.set_preference('general.useragent.override', user_agent)

# Launch firefox browser

browser = webdriver.Firefox(service=firefox_service, options=firefox_options)
browser.get('https://sig.ifc.edu.br/sigaa/verTelaLogin.do')

email_path = 'user.login'
password_path = 'user.senha'
submit_path = ".//input[@value='Entrar' and @type='submit']"

email_element = browser.find_element(By.NAME ,email_path)
password_element = browser.find_element(By.NAME ,password_path)
botao_element = browser.find_element(By.XPATH, submit_path)

email_element.send_keys('renan.okada')
password_element.send_keys('Fabiodinha2014')

botao_element.click()



