import re

def made_message_link(text):
    # Регулярное выражение для поиска ссылки с ID
    pattern = r"MessageWindow\.aspx\?ID=[A-F0-9]{32}"
    
    # Поиск ссылки в тексте
    match = re.search(pattern, text)
    
    # Возвращаем найденную ссылку или None, если она не найдена
    return f"https://old.bankrot.fedresurs.ru/{match.group(0) if match else None}&attempt=1"