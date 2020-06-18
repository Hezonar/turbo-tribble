import time
from selenium import webdriver
import config

try_count = 0

browser = webdriver.Chrome(executable_path=config.exc_path,
                           options=config.chrome_options)


def enter():  # вход в инсту
    try:
        global try_count
        try_count += 1
        browser.get("https://www.instagram.com/")
        time.sleep(3)
    # логин
        browser.find_element_by_xpath("//section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input").\
            send_keys(config.login)
    # пароль
        browser.find_element_by_xpath("//section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input").\
            send_keys(config.password)

        time.sleep(0.5)
    # кнопка войти
        browser.find_element_by_xpath("//section/main/article/div[2]/div[1]/div/form/div[4]/button/div").\
            click()
        time.sleep(8)
        print("Успешно зашел в аккаунт")
    except Exception as err:
        print("Ошибка со входом", err)
        if try_count <= 3:
            print("Попытка перезайти №", try_count)
            time.sleep(5)
            enter()
        else:
            print("Зайти в аккаунт не удалось")


