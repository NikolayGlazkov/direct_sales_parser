from datetime import datetime, timedelta

def calculate_price(start_price, start_date, end_date, step_percent, step_days):
    """
    Рассчитывает цену и дату окончания интервала по шагам снижения цены, по торгам по прямому договору
    
    :param start_price: float, начальная цена
    :param start_date: str, дата начала подачи заявок в формате "дд.мм.гггг чч:мм"
    :param end_date: str, дата окончания подачи заявок в формате "дд.мм.гггг чч:мм"
    :param step_percent: float, процент снижения за шаг (например, 10 для 10%)
    :param step_days: int, количество дней в шаге снижения цены
    :return: list of tuples, где каждый кортеж содержит дату конца интервала и текущую цену
    """
    # Преобразуем строки в datetime
    start_date = datetime.strptime(start_date, "%d.%m.%Y %H:%M")
    end_date = datetime.strptime(end_date, "%d.%m.%Y %H:%M")
    
    current_price = start_price  # Текущая цена
    intervals = []  # Список для хранения интервалов
    current_date = start_date  # Текущая дата

    # Цикл по интервалам
    while current_date < end_date:
        next_date = current_date + timedelta(days=step_days)  # Следующая дата
        if next_date > end_date:
            next_date = end_date  # Не превышаем дату окончания подачи заявок
        
        intervals.append((next_date.strftime("%d.%m.%Y %H:%M"), round(current_price, 2)))  # Сохраняем интервал
        current_price *= (1 - step_percent / 100)  # Уменьшаем цену на заданный процент
        current_date = next_date  # Переходим к следующему интервалу

    return intervals  # Возвращаем список интервалов

# Пример использования
start_price = 13500  # Начальная цена
start_date = "22.11.2024 00:01"
end_date = "27.12.2024 23:59"
step_percent = 10  # Шаг снижения в процентах
step_days = 5  # Шаг снижения в днях

price_intervals = calculate_price(start_price, start_date, end_date, step_percent, step_days)

# Выводим результат
for interval in price_intervals:
    print(f"Дата конца интервала: {interval[0]}, Текущая цена: {interval[1]}")
