import re
from get_info_from_EFRSB import *
from find_mass_url import *
from data_raw import *
from bs4 import BeautifulSoup
import requests



def made_info_data(list_of_num:list):
    """передаем список с одним либо несколькими номерами с ЕФРСБ и получаем 
    словарь с ключами и значениями для дальнейшего использвания"""
    cookie = get_cookies_by_requests()

    # Создание данных с номером сообщения о проведении торгов
    for i in list_of_num:
        data_raw = made_raw_data_for_massage_number(i)
        response = requests.post(made_message_link(get_oll_mssege_page(cookie=cookie, data_raw=data_raw)))
        html_content = response.text

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

        # Инициализация словаря для лотовa
        lots_dict = {}
        lot_table = soup.find("table", class_="lotInfo")

        # Обработка лотов в табличном формате
        if lot_table:
            for row in lot_table.find_all("tr")[1:]:  # Пропускаем заголовок
                cells = row.find_all("td")
                if len(cells) >= 2:  # Проверка на наличие хотя бы номера и описания
                    lot_number = cells[0].get_text(strip=True)
                    description = cells[1].get_text(strip=True)
                    # Добавляем лот в словарь
                    lots_dict[lot_number] = description

        # Если таблица с лотами отсутствует, обрабатываем текст
        else:
            lot_lines = re.split(r'\s*\d+\.\s*', soup.get_text())
            lot_lines = [line.strip() for line in lot_lines if line.strip()]

            for index, line in enumerate(lot_lines, start=1):
                match = re.search(r'(.+?)\s(\d+ шт\.)\s([\d\s,]+ руб\.)', line)
                if match:
                    description = match.group(1).strip()
                    lot_number = str(index)
                    lots_dict[lot_number] = description

        # Извлечение email, если он присутствует
        email = data.get("E-mail")

        if not email:
            # Ищем все email-адреса в html_content и сохраняем их в список
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html_content)
            
            if emails:
                # Если email-адреса найдены, сохраняем их список в data
                data["E-mail"] = emails
            else:
                # Если email-адреса не найдены, сохраняем сообщение "Не найден"
                data["E-mail"] = ["Не найден"]
        else:
            # Если email уже есть в data, делаем его списком для единообразия
            data["E-mail"] = [email]

    return data|lots_dict



