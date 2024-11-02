from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import random
import re
from data_raw import *

# Получение куки через Selenium
def get_cookie():
    """Получение куки для ЕФРСБ с использованием Selenium."""
    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver, 30)
        driver.get('https://old.bankrot.fedresurs.ru/Default.aspx')
        all_cookies = driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in all_cookies}
        return cookies_dict

# Получение куки через requests
def get_cookies_by_requests():
    """Получение куки для ЕФРСБ без использования Selenium."""
    url = 'https://old.bankrot.fedresurs.ru/Default.aspx'
    session = requests.Session()
    response = session.get(url)
    
    if response.status_code == 200:
        # Дополняем куки вручную (если это необходимо и известно значение)
        session.cookies.set('_ym_isad', '2')
        session.cookies.set('_ym_d', '1730479753')
        session.cookies.set('_ym_uid', '1730479753644317225')
        cookies_dict = session.cookies.get_dict()
        return cookies_dict
    else:
        print("Не удалось получить страницу, статус:", response.status_code)
        return None

# Получение страницы с сообщениями
def get_oll_mssege_page(cookie, data_raw, session=None, retries=3):
    """Переход на страницу поиска и ввод запроса для получения страницы с результатом."""
    url = 'https://old.bankrot.fedresurs.ru/Messages.aspx?attempt=1'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
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
        'sec-ch-ua-platform': "macOS"
    }
    
    # Используем сессию, если она передана, иначе создаем новую
    if session is None:
        session = requests.Session()
    
    for attempt in range(retries):
        try:
            # Отправляем POST-запрос
            response = session.post(url, data=data_raw, headers=headers, cookies=cookie)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}. Попытка {attempt + 1} из {retries}")
            # Пауза перед повторной попыткой (увеличивается при каждой попытке)
            time.sleep(5 * (attempt + 1))
    
    # Возвращаем None, если все попытки не удались
    print("Все попытки запроса исчерпаны. Проверьте соединение и куки.")
    return None

# # Основной цикл для получения страниц
# def main():
#     cookie = get_cookies_by_requests()
    
#     if not cookie:
#         print("Не удалось получить куки. Проверьте соединение.")
#         return
    
#     # Пример данных
#     list_of_num = ["15901584", "15127894", "15136541"]
    
#     session = requests.Session()  # Создаем сессию для сохранения куки
    
#     for num in list_of_num:
#         data_raw = made_raw_data_for_massage_number(num)
#         page_content = get_oll_mssege_page(cookie, data_raw, session=session)
        
#         if page_content:
#             print(f"Контент для {num} получен.")
#             # Дополнительная обработка страницы...
#         else:
#             print(f"Не удалось получить контент для {num}.")
        
#         # Пауза между запросами
#         time.sleep(random.uniform(1, 3))  # Случайная пауза для уменьшения риска бана

# if __name__ == "__main__":
#     main()
