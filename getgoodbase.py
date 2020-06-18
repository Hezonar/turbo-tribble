import csv
import config
import time
import re
import enter

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSelectorException

op = config.op  # подписка на закрытый акк 1 - да 0 - нет
followers = config.followers  # максимальное кол-во подписчиков для подписки
posts = config.posts  # минимум постов
browser = enter.browser


# функции проверки существования элемента на странице
def class_existece(url):
    try:
        browser.find_element_by_class_name(url)
        existence = 1
    except NoSuchElementException or InvalidSelectorException:
        existence = 0
    return existence


# читаем нашу базу
def read_base():
    links = []
    with open("base.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            links.append(row)
    # преобразуем в нормальный вид
    x = str(links[0]).replace("[", '').replace("]", '').replace("'", '').replace(' ', '').split(",")
    return x


# проверяем аккаунт на "хороший"
def get_good_accs(link, op_, followers_, posts_):
    good_accs = []
    if len(link) >= 30:
        for a in range(len(link) // 30):
            for i in range(30):
                browser.get(link[30*a+i])
                try:
                    if browser.find_element_by_class_name("MCXLF").text == "К сожалению, эта страница недоступна.":
                        print(30*a+i, "недоступна страница")
                        continue
                except:
                    Exception

                time.sleep(1)
                good = check_user(i, op_, followers_, posts_)  # проверка пользователя по критериям
                if good > 0:
                    print(30*a+i, "Не подходит")
                else:
                    good_accs.append(link[30*a+i])
            time.sleep(config.time_wait_before_good_parse_base)  # задержка между парсингом хорошей базы

    else:
        for i in range(len(link)):
            browser.get(link[i])
            try:
                if browser.find_element_by_class_name("MCXLF").text == "К сожалению, эта страница недоступна.":
                    print(i, "недоступна страница")
                    continue
            except:
                Exception
            time.sleep(1)
            good = check_user(i, op_, followers_, posts_)
            if good > 0:
                print(i, "Не подходит")
            else:
                good_accs.append(link[i])

    return good_accs


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


# записываем в csv файл
def save_to_scv(data):
    with open('great_base.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow(data)  # записывает все в одну строчку
    f.close()


# удаляем нашу сгенерированную базу
def clear_base():
    with open('base.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow('')
    f.close()


def main():

    base = read_base()  # получаем массив ссылок
    enter.enter()
    need_to_sub_accs = get_good_accs(base, op, followers, posts)  # получаем нужные акки
    #browser.close()
    save_to_scv(need_to_sub_accs)  # сохраняем "хорошую базу"
    clear_base()  # чистим базу


if __name__ == '__main__':
    print("GetGoodWtf")