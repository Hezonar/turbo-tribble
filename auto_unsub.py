import config
from datetime import timedelta, datetime
import time

from selenium import webdriver


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


links = []
time_sub = []


def read_base_unsub():
    global links
    global time_sub
    f = open("links_to_unsub.txt", 'r')
    x = f.read()
    x = x[:-1]
    links = (x.split(';'))
    f.close()

    f = open("time_sub.txt", 'r')
    x = f.read()
    x = x[:-1]
    time_sub = (x.split(';'))
    f.close()

    return links, time_sub


def check_time(link, time_subs):
    now = datetime.now()
    delay = config.unsub_time
    unsub_base_ready = []
    for i in range(len(link)):
        time_ = time_subs[i].split('-')
        year = int(time_[0])
        month = int(time_[1])
        day = int(time_[2])
        date_sub = datetime(year, month, day)
        check_delay = now - date_sub
        if check_delay.days >= delay:
            unsub_base_ready.append(link[i])
    if len(unsub_base_ready) != 0:
        enter()
        unsub(unsub_base_ready)


def unsub(urls):
    global links
    global time_sub
    for i in range(len(urls)):
        unsub_success = 0
        browser.get(urls[i])
        time.sleep(1.5)
        try:
            try:
                if browser.find_element_by_class_name("zwlfE").find_element_by_class_name("_5f5mN").text != "Подписаться":
                    browser.find_element_by_class_name("zwlfE").find_element_by_class_name("_5f5mN").click()
                    time.sleep(0.8)
                    browser.find_element_by_class_name("mt3GC").find_element_by_class_name("aOOlW").click()
                    time.sleep(0.5)
                    links.pop(i)
                    time_sub.pop(i)
                    unsub_success = 1
            except:
                pass
            try:
                if browser.find_element_by_class_name("BY3EC").text == "Запрос отправлен":
                    browser.find_element_by_class_name("BY3EC").click()
                    time.sleep(0.8)
                    browser.find_element_by_class_name("mt3GC").find_element_by_class_name("aOOlW").click()
                    time.sleep(0.5)
                    links.pop(i)
                    time_sub.pop(i)
                    unsub_success = 1
            except:
                pass
        except:
            print("Отписаться не удалось", urls[i])

        if unsub_success == 1:
            print("Упешно отписаны от: ", urls[i])
            time.sleep(config.time_wait_before_unsub)  # задержка перед отпиской


def write_csv_need_to_unsub():
    global links
    global time_sub
    f = open("links_to_unsub.txt", 'w')
    for i in range(len(links)):
        f.write(links[i] + ';')
    f.close()

    f = open("time_sub.txt", 'w')
    for i in range(len(time_sub)):
        f.write(time_sub[i] + ';')
    f.close()


def main():
    global links, time_sub
    links, time_sub = read_base_unsub()  # читаем нашу базу для ансаба
    time.sleep(5)
    check_time(links, time_sub)  # чекаем время подписки
    write_csv_need_to_unsub()  # перезаписываем файл unsub_base
    browser.quit()


if __name__ == '__main__':
    print("WtfAutoUnsub")
    main()