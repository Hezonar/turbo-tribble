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
        print("Выполнен вход в аккаунт")
    except Exception as err:
        print("Ошибка со входом", err)
        if try_count <= 3:
            print("Попытка перезайти №", try_count)
            time.sleep(5)
            enter()
        else:
            print("Зайти в аккаунт не удалось")


def parsing():
    # открыть подписчиков
    time.sleep(2)
    browser.find_element_by_xpath("//section/main/div/header/section/ul/li[2]/a"). \
        click()
    time.sleep(config.time_wait_before_parse_base)  # задержка перед парсом
    all_accs = base()  # все найденные акки
    print("В базу добавлено ", len(all_accs), " аккаунтов")
    return all_accs


# получаем ссылки на юзеров
def base():
    all_links = browser.find_elements_by_class_name("FPmhX")
    for i in range(len(all_links)):
        all_links[i] = all_links[i].get_attribute('href')
    return all_links


# записываем в csv файл
def save_to_scv(data):
    f = open("base.txt", 'a')
    for i in range(len(data)):
        f.write(data[i] + ';')
    f.close()


def main():

    enter()  # входим
    time.sleep(2)  # задержка
    parse_from = config.parse_from  # откуда парсим
    browser.get(parse_from)  # откуда парсим
    time.sleep(4)  # задержка
    # count = config.parse_count_to_base_day  # необходимое количество  UPDATE 1.1
    links_followers = parsing()  # массив из ссылок
    save_to_scv(links_followers)  # сохраняем в csv
    browser.quit()


if __name__ == '__main__':
    main()
