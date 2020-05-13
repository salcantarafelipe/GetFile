from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import datetime
import pandas as pd
from pandas.tseries.offsets import BDay

now = datetime.datetime.now()
mes = now.month
today = pd.datetime.today()

Feriado = {datetime.date(now.year, 6, 11)} # you can add more here
DiaUtil = 0
for a in range(1, 32):
    try:
        thisdate = datetime.date(now.year, now.month, a)
    except(ValueError):
        break
    if thisdate.weekday() < 5 and thisdate not in Feriado:
        DiaUtil += 1

dias_com_arquivo = []
for dia in range(DiaUtil):
    d = str((today - BDay(dia)).day)
    m = str((today - BDay(dia)).month)
    a = str((today - BDay(dia)).year)
    
    if len(m) == 1:
        m = '0' + m
    if len(d) == 1:
        d = '0' + d
    if (today - BDay(dia)).month == mes:
        dias_com_arquivo.append(d + '/' + m + '/' + a)


for x in range(len(dias_com_arquivo)):
    chromedriver = 'chromedriver.exe'
    browser = webdriver.Chrome(chromedriver)
    time.sleep(5)
    browser.get('http://www.bmf.com.br/arquivos1/lum-arquivos_ipn.asp?idioma=pt-BR&status=ativo')
    time.sleep(5)


    item = browser.find_element_by_xpath("//input[@class='Mercado de Ações - Prêmio de Referência para Opções sobre Ações']")
    browser.execute_script("arguments[0].click();", item)
    time.sleep(10)
    data = browser.find_element_by_xpath("//*[@id='txtDataDownload14_ativo']")
    browser.execute_script("arguments[0].click();", data)
    data.send_keys(dias_com_arquivo[x])

    browser.find_element_by_xpath("//input[@id='imgSubmeter_ativo']").click()
    time.sleep(20)
 
    if os.path.exists(r'c:\Users\{}\Downloads\Download.ex_'.format(os.getlogin())):
        os.rename(r'c:\Users\{}\Downloads\Download.ex_'.format(os.getlogin()), r'c:\Users\{}\Downloads\arquivo_{}.ex_'.format(os.getlogin(), str(dias_com_arquivo[x].replace('/', '-'))))
        print('nome alterado')
    else:
        print('Não tem arquivo para esse dia')


    browser.close()
