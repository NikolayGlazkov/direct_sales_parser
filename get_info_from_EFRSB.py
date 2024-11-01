from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
from data_raw import *
#куки с сайти
def get_cookie():
    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver, 30)  # Увеличим время ожидания до 30 секунд
        
        driver.get('https://old.bankrot.fedresurs.ru/Default.aspx')
        
        
        all_cookies=driver.get_cookies()
        cookies_dict = {}
        for cookie in all_cookies:
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict


def get_cookies_by_requests():
    url = 'https://old.bankrot.fedresurs.ru/Default.aspx'
    
    # Создаем сессию
    session = requests.Session()
    
    # Отправляем запрос GET на страницу
    response = session.get(url)
    
    # Проверка на успешность запроса
    if response.status_code == 200:
        # Добавляем вручную недостающие cookies (если их значение известно)
        session.cookies.set('_ym_isad', '2')
        session.cookies.set('_ym_d', '1730479753')
        session.cookies.set('_ym_uid', '1730479753644317225')
        
        cookies_dict = session.cookies.get_dict()
        return cookies_dict
    else:
        print("Не удалось получить страницу, статус:", response.status_code)
        return None




# # ссылка со всесеми сообщениями
def get_oll_mssege_page(cookie,data_raw):
    url = 'https://old.bankrot.fedresurs.ru/Messages.aspx?attempt=1'


    headers = { 'Accept': '*/*', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://old.bankrot.fedresurs.ru',
    'Referer': 'https://old.bankrot.fedresurs.ru/PublisherListWindow.aspx?rwndrnd=0.25684540750068474',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-MicrosoftAjax': 'Delta=true',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': 'Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS"}
    x = requests.post(url, data=data_raw,headers = headers,cookies=cookie)
    # s = 
    # result = re.search(s, x.text)
    return x.text

