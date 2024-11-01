from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_info_from_EFRSB import *
from find_mass_url import *
from data_raw import *
from bs4 import BeautifulSoup


# куки из ефрсб используя selenium
# cookie = get_cookie()
# куки из ЕФРСБ используя реквест
cookie = get_cookies_by_requests()


# создание raw data c номером сообщения о проведении торгов
data_raw = made_raw_data_for_massage_number("15686143")

html_content = (requests.post(made_message_link(get_oll_mssege_page(cookie=cookie,data_raw=data_raw))).text)

html_code = BeautifulSoup(html_content,'html.parser')

print(html_code)