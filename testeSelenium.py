from multiprocessing.connection import wait
import os
import selenium.webdriver as webdriver
import mysql.connector
from mysql.connector import Error

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

browser = webdriver.Firefox(service=firefox_service, options=firefox_options)
browser.get('https://www.amazon.com.br/')

#CONSTNATES
contas_path = '#nav-link-accountList > span:nth-child(2)'
email_path = '#ap_email'
password_path = '#ap_password'
continue_email_path = '.a-button-input'
login_path = '#signInSubmit'
pesquisa_path = '#twotabsearchtextbox'
botaoPesquisa_path = '#nav-search-submit-button'

#CONSTANTES DA PESQUISA
itemUm = '.widgetId\=search-results_1 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1) > div:nth-child(1) > img:nth-child(1)'
itemDois = '.widgetId\=search-results_2 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1) > div:nth-child(1)'

htmlLocalASIM ="<th class=a-color-secondary a-size-base prodDetSectionEntry> ASIN </th>"
localizou = False

#SEÇÃO DE LOGIN
contas_element = browser.find_element(By.CSS_SELECTOR, contas_path).click()
email_element = browser.find_element(By.CSS_SELECTOR, email_path).send_keys('renanokada2000@gmail.com')
continue_element = browser.find_element(By.CSS_SELECTOR, continue_email_path).click()
password_elemnt = browser.find_element(By.CSS_SELECTOR, password_path).send_keys('Fabiodinha@2014')
login_element = browser.find_element(By.CSS_SELECTOR, login_path).click()


#SEÇÃO DE PROCURA 
pesquisa_element = browser.find_element(By.CSS_SELECTOR, pesquisa_path).send_keys('Hot Wheels')
botaoPesquisa_element = browser.find_element(By.CSS_SELECTOR, botaoPesquisa_path).click()


#----- Armazenar no banco essas informações

try:
     con = mysql.connector.connect(host='localhost', database='delivery_laravel', user ='root', password = '12345678')
     cursorDelete = con.cursor()

     cursorDelete.execute('DELETE FROM amazons where id >0;')

     for x in range(4):
          itemSelect_element = browser.find_element(By.CSS_SELECTOR,
          '.widgetId\=search-results_'+str(x+1)+' > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1) > div:nth-child(1)').click()

          #Pegar URL atual
          urlASIM = browser.current_url

          #Pegar o ID do produto
          indx = 0
          for index, j in enumerate(urlASIM.split('/')):
               if j == 'dp':
                indx = index

          urlSeparada = urlASIM.split('/')

          #Produto Código
          urlSeparada[indx+1]
          #TituloProduto
          titulo_produto = browser.find_element(By.CSS_SELECTOR, '#productTitle').text
          #PreçoProduto
          preco_produto = browser.find_element(By.CSS_SELECTOR, 'div.a-spacing-micro:nth-child(1) > span:nth-child(1) > span:nth-child(2) > span:nth-child(2)').text
          #----- Até aqui

          inserir_produtos = ' INSERT INTO `amazons` (`titulo`, `preco`, `link`, `produto_codigo`) VALUES (\''+str(titulo_produto)+'\',\''+str(preco_produto)+'\',\''+str(urlASIM)+'\',\''+str(urlSeparada[indx+1])+'\')'

          cursor = con.cursor()
          cursor.execute(inserir_produtos)
          con.commit()
          print(cursor.rowcount, "registros inseridos na tabela!")
          cursor.close()

          print('URL Atual: '+urlASIM)
          print('ID do Produto: '+ urlSeparada[indx+1])
          print('Titulo: '+titulo_produto)
          print('Preço:'+preco_produto)

          browser.back()

except Error as erro:
     print("Falha ao inserir dados no Mysql: {}".format(erro))
finally:
     if(con.is_connected()):
          cursor.close()
          con.close()
          print("Conexão ao MYSQL finalizada")

