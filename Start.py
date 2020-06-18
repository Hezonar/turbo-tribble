import time
import config
import get_base
import auto_sub
import auto_unsub
import os.path
from datetime import timedelta, datetime

# СДЕЛАТЬ БРАУЗЕР В РЕЖИМЕ HEADLESS!!!!
# ПОМЕНЯТЬ ВЕЗДЕ БРАУЗЕР НА БРАУЗЕР С ПАРАМЕТРАМИ!!!!

# ВАЖНО В ЗБТ ВЕЗДЕ УБРАНО ЗАКРЫТИЕ И ОТКРЫТИЕ БРАУЗЕРА!!!

# СУПЕР ВАЖНО!!!!!!! В КАЖДОМ СКРИПТЕ СДЕЛАТЬ АВТОВХОД ОТДЕЛЬНО!!!!


def main(day):
    stop = 0
    while stop != 1 and day > 0:
        try:
            alham = check_last_circle_time()  # чекаем на время послднего запуска  проги

            if alham == 1:  # если прошло больше 1 дня запускаем скрипт

                write_last_circle_time()  # запоминаем время последнего запуска
                day -= 1  # уменьшаем время работы скрипта на один

                clear_total_subs_and_like()  # чистим кол-во подписок и лайков
                print("Успешно очищен список лайков и подписок")

                stop_ = parse_base()  # проверяем базу на наличие нужного кол-ва
                if stop_ == 1:  # Если проблема с базами, остановить цикл
                    break

                stop_ = sub()  # запускаем скрипт с подпиской
                if stop_ == 1:  # Если проблема с базами, остановить цикл
                    break
                print("Успешно подписаны на сегодняшний день")

                print("Ждем час перед отписками")
                time.sleep(3600)  # ждем час перед отписками

                stop_ = unsub()  # запускаем скрипт с автоотпиской
                if stop_ == 1:
                    break
                print("Успешно отписаны на сегодняшний день")

                print("Скрипт успешно выполнен. Перезапуск скрипта будет на следующий день...")

            else:
                if day == 0:
                    print("Подписка закончилась")
                    break
                time.sleep(18000)  # ждем 5 часов и проверяем

        except Exception as err:
            print("Ошибка в цикле", err)
            stop = 1


def check_last_circle_time():

    if os.path.exists("check_last_circle.txt"):
        f = open("check_last_circle.txt", 'r')
        a = f.read()
        b = a.split('-')
        year = int(b[0])
        month = int(b[1])
        day = int(b[2])
        date_of_circle = datetime(year, month, day)
        period = datetime.now() - date_of_circle
        if period.days >= 1:
            dulilyah = 1
        else:
            dulilyah = 0

    else:
        f = open("check_last_circle.txt", 'w')
        f.close()
        dulilyah = 1

    return dulilyah


def write_last_circle_time():
    a = datetime.now()
    t = a.strftime("%Y") + "-" + a.strftime("%m") + '-' + a.strftime("%d")
    f = open("check_last_circle.txt", 'w')
    f.write(t)
    f.close()


def unsub():
    stop = 0
    try:
        auto_unsub.main()
    except Exception as err:
        print(err)
        stop = 1
    return stop


def sub():
    stop = 0
    try:
        likes, subs = get_likes_and_subs_today()
        count_subs = config.count_subs_per_day
        count_likes = config.count_likes_per_day
        count_subs -= subs  # сколько осталось подписок в день сделать
        count_likes -= likes  # сколько осталось лайков в день сделать
        count = max(count_subs, count_likes)
        print("Осталось подписок на сегодня: ", count)
        while count > 0:

            auto_sub.main()
            time.sleep(config.time_wait_before_sub)
            count -= 1
            if count != 1 or count != 0:
                print("Осталось подписок на сегодня: ", count-1)

    except Exception as err:
        print(err)
        stop = 1

    return stop


def get_likes_and_subs_today():  # получаем на сколько челов подписались сегодня
    f = open("allready_likes.txt")
    like___ = f.read()
    if like___ == '':
        like___ = 0
    f.close()
    f = open("allready_subs.txt")
    sub___ = f.read()
    if sub___ == '':
        sub___ = 0
    f.close()
    return int(like___), int(sub___)


def clear_total_subs_and_like():
    f = open("allready_likes.txt", 'w')
    f.write("0")
    f.close()

    f = open("allready_subs.txt", 'w')
    f.write("0")
    f.close()


def parse_base():
    stop = 0
    try:
        count_base = check_base()
        if len(count_base) > config.count_subs_per_day*10:
            print("В базе хватает людей для подписки, кол-во людей в базе: ", len(count_base))
        else:
            print("Начинаю сбор базы")
            get_base.main()
    except Exception as err:
        print("ОШибка", err)
        stop = 1
    return stop


def check_base():  # чекаем кол-во человек в базе
    if os.path.exists('base.txt'):
        f = open("base.txt", 'r')
        a = f.read()
        a = a[:-1]
        b = a.split(';')
    else:
        f = open("base.txt", 'w')
        f.close()
        b = []
    return b


if __name__ == '__main__':
    count_days = 1  # кол-во выполнений скрипта (в днях)
    main(count_days)