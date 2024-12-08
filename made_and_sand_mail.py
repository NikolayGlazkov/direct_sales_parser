import combain_info
import os 
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def generate_email_text(data, lot_nums):
    # Извлечение данных для обращения
    manager_name = (str(data.get('Арбитражный управляющий')).split("(")[0].rstrip()
                    if data.get('Арбитражный управляющий') else data.get('Организатор торгов'))
    
    # Формирование текста для каждого лота
    lots_text = "\n".join([f"Лот№ {lot_num}: {data.get(lot_num, 'Информация о лоте отсутствует')}"+"\n" for lot_num in lot_nums])

    # Формирование полного текста письма
    email_text = f"""Здравствуйте уважаемый(ая) {manager_name},
    
Прошу вас предоставить мне информацию по лотам, опубликованным на сайте ЕФРСБ.
№ сообщения: {data.get("№ сообщения")}
Должник: {(data.get("Наименование должника") if data.get("Наименование должника") else data.get("ФИО должника"))}
ИНН: {data.get("ИНН")}

А именно:

{lots_text}

У вас есть фото имущества? Где и по каким дням проходит осмотр?, контактные номера.
Можете также предоставить все имеющиеся документы по этим лотам?
Сканы документов о регистрации.

С уважением Глазков Николай Александрович 89377419582
Вторая почта для связи vanohaker@yandex.ru
"""

    return email_text

def send_email(message, obligor_name, recipient):
    sender = "gn9377419582@gmail.com"
    password = os.getenv("PASSWORD")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = f"Торги должника {obligor_name}"
        msg["From"] = sender
        msg["To"] = recipient
        server.sendmail(sender, recipient, msg.as_string())

        return "Email sent successfully"
    except Exception as ex:
        return f"{ex}\nCheck your login or password"

from email.mime.text import MIMEText
from email.header import Header

def send_email(message, obligor_name, recipient):
    sender = "gn9377419582@gmail.com"
    password = os.getenv("PASSWORD") or "ваш_пароль"

    try:
        # Устанавливаем соединение с сервером
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)

            # Создаем письмо с указанием кодировки
            msg = MIMEText(message, "plain", "utf-8")
            msg["Subject"] = Header(f"Торги должника {obligor_name}", "utf-8")
            msg["From"] = sender
            msg["To"] = recipient

            # Отправляем письмо
            server.sendmail(sender, recipient, msg.as_string())
            print("Письмо успешно отправлено!")
            return "Email sent successfully"
    except Exception as ex:
        print(f"Ошибка отправки: {ex}")
        return f"Ошибка отправки письма: {ex}"


def main(list_of_num,lot_nums):
    # Получаем данные
    data = combain_info.made_info_data(list_of_num)
    
    # Извлекаем имя должника
    obligor_name = data.get("Наименование должника") or data.get("ФИО должника")
    
    # Извлекаем email получателя
    recipient_email = ",".join(data.get("E-mail"))
    # recipient_email = "vanohaker@yandex.ru"
    email_text = generate_email_text(data, lot_nums)
    
    # Отправляем email
    if recipient_email:
        print(send_email(message=email_text, obligor_name=obligor_name, recipient=recipient_email))
    else:
        print("Email address not found in data")

if __name__ == "__main__":
    main(["16078612"],sorted(['1']))
# data = combain_info.made_info_data(['15707596'])
# print(generate_email_text(data=data,lot_nums=['1']))

# message = "Тестовое сообщение. Проверка отправки письма с кириллицей."
# obligor_name = "Тестовый должник"
# recipient = "vanohaker@yandex.ru"

# result = send_email(message, obligor_name, recipient)
# print(result)