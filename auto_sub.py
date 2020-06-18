import time
import config
from datetime import timedelta, datetime
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSelectorException


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


links__ = []  # линки для ансаба
time_sub__ = []  # время для ансаба
rewrite_all_accs = []  # перезапись в csv


# читаем нашу базу
def read_base():
    f = open("base.txt", 'r')
    a = f.read()
    a = a[:-1]
    f.close()
    b = a.split(';')

    return b


def sub_and_like():
    stop = 0
    sub_sccs = 0  # ДОДЕЛАТЬ!
    need_sub = config.need_to_sub
    need_like = config.need_to_like_photo
    if need_sub or need_like == 1:
        if config.op == 1:  # подписка на закрытый акк
            stop, sub_sccs = sub_by_profile()
        elif config.op == 0:
            stop, sub_sccs = sub_by_photo(need_like)

    return stop, sub_sccs


def sub_by_photo(need_to_like):
    like = 0
    stop = 0
    sub_sccs = 0
    try:
        browser.find_element_by_class_name("_9AhH0").click()  # открываем фотку
        time.sleep(1.5)
    except:
        print("Невозможно открыть фотку")

    if need_to_like == 1:  # лайкать, если надо
        try:
            p = browser.find_element_by_class_name("fr66n").find_element_by_class_name("_8-yf5")
            if p.get_attribute("aria-label") == "Нравится":
                p.click()
                like += 1
            else:
                print("Уже поставлен лайк")
        except:
            print("лайк нельзя поставить")

    try:  # подписываться
        if browser.find_element_by_class_name("oW_lN").text == "Подписаться":
            browser.find_element_by_class_name("oW_lN").click()
            time.sleep(1.5)
            sub_sccs = 1
            try:
                if browser.find_element_by_class_name("_08v79").find_element_by_class_name("_7UhW9").text == "Действие заблокировано":
                    stop = 1
            except:
                pass

        else:
            print("Уже подписаны")
    except:
        Exception

    return stop, sub_sccs


def sub_by_profile():
    stop_by_sub = 0
    sub_sccs = 0
    try:
        if browser.find_element_by_class_name("BY3EC").text == "Подписаться":
            browser.find_element_by_class_name("BY3EC").click()
            time.sleep(1.5)
            sub_sccs = 1

            if browser.find_element_by_class_name("_08v79").find_element_by_class_name("_7UhW9").text == "Действие заблокировано":
                stop_by_sub = 1
        else:
            print("Уже подписаны")
    except:
        Exception

    return stop_by_sub, sub_sccs


def start_sub(urls):
    global rewrite_all_accs
    for i in range(len(urls)):
        browser.get(urls[i])
        time.sleep(2)
        good = check_user(config.op, config.followers, config.posts)
        name = urls[i]
        rewrite_all_accs.pop(i)  # избавляемся от акка который чекнули
        if good == 0:  # если акк подходит подписываемся и лайкаем
            stop_, sub_success = sub_and_like()
            if stop_ == 1:
                print("Подписки заблокированы ")
                break

            if sub_success == 1:
                print("Успешно подписаны на ", name)
                unsub_base(name)
                break


# функции проверки существования элемента на странице
def class_existece(url):
    try:
        browser.find_element_by_class_name(url)
        existence = 1
    except NoSuchElementException or InvalidSelectorException:
        existence = 0
    return existence


def check_user(op__, followers__, posts__):
    x = 0
    # 1 проверка на закрытый акк
    element = "rkEop"
    if class_existece(element) == 1:
        try:
            if browser.find_element_by_class_name(element).text == "This Account is Private" or "Это закрытый аккаунт":
                if op__ == 0:
                    x += 1
                    print("акк закрытый")
        except StaleElementReferenceException:
            print("Ошибка 1")

    # меню из 3: публикации подписчики подписки
    menu = 'g47SY'
    if class_existece(menu) == 0:
        print('ошибка 2')
        x = 3
        return x
    else:
        variables = browser.find_elements_by_class_name(menu)

        try:
            count_subs = variables[1].get_attribute("title")  # подписчики
            count_subs = re.sub(r'\s', '', count_subs)  # удаление пробелов из числа пописчиков
            if int(count_subs) > followers__:
                x += 1
                print("число подп. больше")
        except:
            x += 1
            print("ошибка титл")

        try:
            count_posts = variables[0].text  # кол-во постов
            count_posts = re.sub(r'\s', '', count_posts)  # удаление пробелов из числа пописчиков
            if int(count_posts) < posts__:
                x += 1
                print("число постов меньше")
        except:
            x += 1
            print("ошибка постов")
    return x


def unsub_base(link):  # база для ансаба
    a = datetime.now()
    t = a.strftime("%Y") + "-" + a.strftime("%m") + '-' + a.strftime("%d")
    global links__
    global time_sub__
    links__.append(link)
    time_sub__.append(t)


# перезаписываем в csv файл
def rewrite_good_base(links):
    f = open('base.txt', 'w')
    for i in range(len(links)):
        f.write(links[i] + ';')
    f.close()


def write_csv_need_to_unsub(link, timing):
    f = open("links_to_unsub.txt", 'a')
    for i in range(len(link)):
        f.write(link[i] + ';')
    f.close()

    f = open("time_sub.txt", 'a')
    for i in range(len(timing)):
        f.write(timing[i] + ';')
    f.close()


def main():
    all_accs = read_base()  # добавляем все акки из базы
    enter()  # заходим в аккаунт
    global rewrite_all_accs
    rewrite_all_accs = all_accs  # аккаунты для перезаписи в файл
    start_sub(all_accs)  # начинаем подписку
    write_csv_need_to_unsub(links__, time_sub__)  # записываем в csv ссылку и время подписки
    rewrite_good_base(rewrite_all_accs)  # удаляем из базы
    browser.quit()


if __name__ == '__main__':
    print("WtfMainSub")
    main()