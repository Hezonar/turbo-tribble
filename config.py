from selenium.webdriver.chrome.options import Options

login = "lolkekboss"  # логин от аккаунта
password = "lolkekprikol"  # пароль от аккаунта

#login = "fhnneh@mail.ru"  # логин от аккаунта
#password = "15Vfz1978"  # пароль от аккаунта

API_TOKEN = "1201025788:AAHykRX4WGZK4rEst04ipUUSWN9t4HB1ti0"  # token для телеги

parse_from = "https://www.instagram.com/mikhail_litvin/"  # откуда парсить челов
#  parse_count_to_base_day = 20  # сколько в день парсить в базу  UPDATE 1.1

op = 0  # подписка на закрытый акк 1 - да 0 - нет
followers = 1500  # максимальное кол-во подписчиков для подписки
posts = 2  # минимум постов

need_to_like_photo = 1  # 1 - ставить 0 - нет
need_to_sub = 1  # 1 - подписываться 0 - нет
unsub = 1  # 1 - отписываться 0 - нет
unsub_time = 3  # кол-во дней для отписки

count_subs_per_day = 1  # кол-во подписок в день
count_likes_per_day = 1  # кол-во лайков в день

# задержки
time_wait_before_sub = 10  # задержка перед подпиской (в сек)  РЕКОМЕНДОВАННО 3-5 МИНУТ
time_wait_before_like = 1*60  # задержка перед лайком (в сек)
time_wait_before_unsub = 30  # задержка перед отпиской (в сек)
time_wait_before_parse_base = 30  # задержка между парсом базы (в сек)
time_wait_before_good_parse_base = 30  # задержка между хорошим парсом базы (в сек)


WINDOW_SIZE = "1920,1080"  # Браузер без
chrome_options = Options()  # открытия
chrome_options.add_argument("--headless")  # окон
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)  # и это тоже
exc_path = 'chromedriver.exe'

"""
from selenium import webdriver
browser = webdriver.Chrome(executable_path=config.exc_path,
                           options=config.chrome_options)
ЭТО ВСТАВИТЬ ВЕЗДЕ!!!!
"""

"""
Доделать:

браузер в режиме headless

"""