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

list_of_num = ["15127894", "15136541"]

# Создание данных с номером сообщения о проведении торгов
for i in list_of_num:
    data_raw = made_raw_data_for_massage_number(i)
    response = requests.post(made_message_link(get_oll_mssege_page(cookie=cookie, data_raw=data_raw)))
    html_content = response.text

    # Выводим html_content для отладки
    # print("HTML Content:", html_content)

    soup = BeautifulSoup(html_content, "html.parser")

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
    else:
        # Обработка текста в div class="msg" для поиска лотов
        for div in soup.find_all("div", class_="msg"):
            text_content = div.get_text(" ", strip=True)
            # print("Text Content:", text_content)  # Для отладки

            # Извлекаем лоты на основе структурированных данных
            lot_items = div.find_all(text=re.compile(r"Лот\s*№\s*\d+"))  # Ищем текст, содержащий "Лот №"
            for item in lot_items:
                # Ищем ближайший элемент (например, <br>), чтобы получить название и цену
                lot_number_match = re.search(r"Лот\s*№\s*(\d+)", item)
                if lot_number_match:
                    lot_number = lot_number_match.group(1)
                    lot_details = item.split("–")  # Предполагаем, что цена идет после "–"
                    if len(lot_details) > 1:
                        lot_name = lot_details[0].strip()
                        lot_price_match = re.search(r"(\d[\d\s]*)", lot_details[1])
                        lot_price = lot_price_match.group(0).replace(" ", "") if lot_price_match else None
                        if lot_price:
                            lot_info.append({
                                "Номер лота": lot_number,
                                "Наименование": lot_name,
                                "Начальная цена": int(lot_price)
                            })

    # Добавляем информацию о лотах в data["Лоты"]
    data["Лоты"] = lot_info

    # Извлечение email, если он присутствует
    email = data.get("E-mail")
    if not email:
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html_content)
        if emails:
            email = emails[0]
            data["E-mail"] = email
        else:
            email = "Не найден"

    # Выводим email и лоты
    print(email, data["Лоты"])

    # Пауза между запросами
    time.sleep(random.uniform(1, 3))
