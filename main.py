import re
from get_info_from_EFRSB import *
from find_mass_url import *
from data_raw import *
from bs4 import BeautifulSoup
import requests
import time
import random

# Получение куков из ЕФРСБ
cookie = get_cookies_by_requests()

list_of_num = ["15921634"]

# Создание данных с номером сообщения о проведении торгов
for i in list_of_num:
    data_raw = made_raw_data_for_massage_number(i)
    response = requests.post(made_message_link(get_oll_mssege_page(cookie=cookie, data_raw=data_raw)))
    html_content = response.text

    # Выводим html_content для отладки
    # print("HTML Content:", html_content)

    soup = BeautifulSoup(html_content, "html.parser")
    # print(soup)
    
    # Инициализация пустого словаря для сохранения данных
    data = {}

    # Извлечение основных данных из таблиц
    for table in soup.find_all("table", class_="headInfo"):
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                data[key] = value

    # Извлечение данных из таблицы с лотом
    lot_info = []
    lot_table = soup.find("table", class_="lotInfo")
    if lot_table:
        headers = [th.get_text(strip=True) for th in lot_table.find_all("th")]
        for row in lot_table.find_all("tr")[1:]:
            lot_data = {}
            cells = row.find_all("td")
            for idx, cell in enumerate(cells):
                lot_data[headers[idx]] = cell.get_text(strip=True)
            lot_info.append(lot_data)
            #print("Lot data:", lot_data)  # Добавили отладочный вывод
    else:
        # Попытка извлечения данных из текстового списка лотов
        lots_dict = {}
        lot_lines = re.split(r'\s*\d+\.\s*', soup.get_text())
        lot_lines = [line.strip() for line in lot_lines if line.strip()]

        for line in lot_lines:
            # Используем регулярное выражение для извлечения количества и цены
            match = re.search(r'(.+?)\s(\d+ шт\.)\s([\d\s,]+ руб\.)', line)
            if match:
                name = match.group(1).strip()
                quantity = match.group(2).strip()
                price = match.group(3).strip()
                lot_number = f"Лот {len(lots_dict) + 1}"
                lots_dict[lot_number] = {"Описание": name, "Количество": quantity, "Начальная цена продажи": price}
    
    # Извлечение email, если он присутствует
    email = data.get("E-mail")
    if not email:
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html_content)
        if emails:
            email = emails[0]
            data["E-mail"] = email
        else:
            email = "Не найден"
    
    # Исключаем блокирующие запросы
    time.sleep(random.uniform(1, 3))

# Вывод данных о лотах
if lot_info:
    print("Данные лотов из таблицы:", lot_info)
else:
    print("Данные лотов из текста:", lots_dict)
print(data["E-mail"])