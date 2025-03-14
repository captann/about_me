from random import sample
from PIL import Image, ImageDraw
import time
import datetime as dt
import sys


def what_server():
    global spisok
    print(f"Для дальнейшего продолжения выберите сервер из списка:", end=' ')
    print(f"{', '.join(spisok)}")
    abc = input("Введите сервер: ")
    while abc not in spisok:
        print("Введите коррекный сервер.")
        print('Если Вы хотите вернуться на главную - нажмите 1,', end=' ')
        print('но ваш аккаунт не сохранится.')
        print("Иначе нажмите любую иную клавишу.")
        abc = input("Введите следующую команду: ")
        if abc == '1':
            first()
    return abc


def zapros(nick, *args):
    global start_commands, Nicknames_passwords, already, names_accounts, spisok
    print()
    count = 0
    if len(args) == 1:
        word = args[0]
    else:
        word = input("Введите следующую команду: ")
        print()
    while word.lower() not in start_commands:
        print()
        word = input("Введите корректную команду: ")
    while 2 < 9:
        if word.lower() == 'на главную':
            first()
            second(nick)
        elif word == 'помощь':
            names_accounts[nick].help()
            print()
            word = input("Введите следующую команду:  ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word == 'отправить':
            print(f"Допустимые сервера: {', '.join(spisok)}")
            print()
            server = input("Введите сервер получателя: ")
            while server not in spisok:
                count += 1
                if count % 5 == 0:
                    while not no_bot():
                        print("Попробуйте снова.")
                        print("Если вы хотите перейти на главную", end=' ')
                        print("-  введите 1.")
                        print("Иначе нажмите любую иную клавишу.")
                        print()
                        qwerty = input("Введите следующую команду: ")
                        print()
                        if qwerty == str(1):
                            first()
                            second(nick)
                print("Сервер не найден. Попробуйте еще раз.")
                print()
                server = input("Введите сервер получателя: ")
            name = input("Введите никнейм поучателя: ")
            while name not in Nicknames_passwords:
                print()
                print(f"Пользователь с никнеймом {name} не найден.")
                print('''Если Вы хотите вернуться на гланую - введите 1.''')
                print("Иначе введите корректное имя пользователя.")
                print()
                name = input('Введите следующую команду: ')
                if name == '1':
                    first()
            print()
            while names_accounts[name].server != server:
                print(f"Пользователь с никнеймом {name}", end=' ')
                print(f"на сервере {server} не найден.")
                print('''Если Вы хотите вернуться на гланую - введите 1.''')
                print("Иначе введите корректный сервер.")
                print()
                print('Если Вам нужно узнать сервер получателя, нажмите 2.')
                print()
                word = input("Введите следующую команду: ")
                if word != '1' and word != '2':
                    server = word
                if word.lower() == '1':
                    first()
                    second(nick)
                elif word.lower() == '2':
                    print(names_accounts[name].server)
                    continue
            text = input("Введите текст: ")
            while len(text) < 1:
                print()
                print("Пустое письмо не может быть отправлено.")
                print('''Если Вы хотите вернуться на гланую - введите 1.''')
                print("Иначе введите корректный сервер.")
                print()
                text = input("Введите следующую команду: ")
                if text.lower() == '1':
                    first()
                    second(nick)
            names_accounts[nick].send_mail(server, name, text)
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'сменить сервер':
            print(f"Список доступных серверов: {', '.join(spisok)}")
            print(f"Выберете сервер для смены.")
            change = input("Введите сервер: ")
            while change not in spisok:
                print("Сервер не найден.")
                print('''Если Вы хотите вернуться на гланую - введите 1.''')
                print("Иначе введите корректный сервер.")
                print()
                change = input("Введите следующую команду: ")
                if change.lower() == '1':
                    first()
                    second(nick)
            result = names_accounts[nick].change_server(change)
            while not result:
                result = names_accounts[nick].change_server(change)
                print('''Если Вы хотите вернуться на гланую - введите 1.''')
                print("Иначе введите корректный сервер.")
                print()
                change = input("Введите следующую команду: ")
                if change.lower() == '1':
                    first()
                    second(nick)
            word = input("Введите следующую команду: ")
            print()
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'входящие':
            if names_accounts[nick].messages != {}:
                res = names_accounts[nick].messages
                keys = list(res.keys())
                val = list(res.values())
                for i in range(len(keys)):
                    abc = keys[i].split()
                    print(f"Сообщение от пользователя: {val[i][0]}.")
                    print(f"Получено {abc[0]} в {abc[1]}.")
                    print(f"Текст сообщения: '{val[i][1]}'.")
                    print()
                if not names_accounts[nick].deletion:
                    names_accounts[nick].messages = {}
            else:
                print("Нет сообщений.")
                print()
            word = input("Введите следующую команду: ")
            print()
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == "удалить сообщение":
            if names_accounts[nick] != {}:
                data = input("Введите дату и время сообщения ЧЕРЕЗ ПРОБЕЛ: ")
                print()
                while data not in names_accounts[nick].messages:
                    print("Сообщение не найдено.")
                    print("Для выхода на главную - введите 1.")
                    print("Если Вам нужно узнать дату и время ", end=' ')
                    print("сообщения, нажмите 2 и выбирете нужную", end=' ')
                    print("дату и время в открывшемся списке Ваших сообщений.")
                    print("Иначе нажмите любую иную клавишу.")
                    zx = input("Введите следующую команду: ")
                    print()
                    if zx == '1':
                        first()
                        second(nick)
                    if zx == '2':
                        res = names_accounts[nick].messages
                        keys = list(res.keys())
                        val = list(res.values())
                        for i in range(len(keys)):
                            abc = keys[i].split()
                            print(f"Сообщение от пользователя: {val[i][0]}.")
                            print(f"Получено {abc[0]} в {abc[1]}.")
                            print(f"Текст сообщения: '{val[i][1]}'.")
                            print()
                    print("Введите дату и время сообщения ЧЕРЕЗ ПРОБЕЛ: ")
                    data = input("Введите дату и время: ")
                else:
                    print("Если вы передумали - введите 1.")
                    print("Иначе нажмите любую иную клавишу.")
                    print()
                    mma = input("Введите следующую команду: ")
                    if mma != '1':
                        names_accounts[nick].delete(data)
                    word = input("Введите следующую команду: ")
                while word.lower() not in start_commands:
                    word = input("Введите корректную команду: ")
                    print()
            else:
                print("Нет сообщений.")
                print()
                word = input("Введите следующую команду: ")
                while word.lower() not in start_commands:
                    word = input("Введите корректную команду: ")
                    print()
        if word.lower() == 'выход':
            stop_work()
        elif word.lower() == 'текущий сервер':
            names_accounts[nick].get_server()
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'удаление':
            if not names_accounts[nick].deletion:
                names_accounts[nick].deletion = True
                print("Теперь сообщения НЕ БУДУТ удаляться автоматически.")
            else:
                names_accounts[nick].deletion = False
                print("Теперь сообщения БУДУТ удаляться автоматически.")
                word = input("Введите следующую команду: ")
                while word.lower() not in start_commands:
                    word = input("Введите корректную команду: ")
                    print()
        elif word.lower() == 'изменить пароль':
            qqww = 0
            abm = no_bot()
            while not abm:
                print('Попробуйте снова.')
                abm = no_bot()
            print('Новый пароль должен быть не короче 6 символов,', end=' ')
            print("содержать буквы ВСЕХ РЕГИСТРОВ и ЦИФРЫ.")
            print('Наша платформа может сама сгенерировать надежный пароль.')
            print('Если вы передумали менять пароль, нажмите 1.')
            print('Если Вы хотите, чтобы наша платфора', end=' ')
            print('сгенерировала пароль, нажмите 2.')
            print('В других случаях введите новый пароль.')
            new_password = input('Введите седующую команду: ')
            if new_password == '1':
                first()
            elif new_password == '2':
                Nicknames_passwords[nick] = generate_password()
            else:
                abc = password_level(new_password)
                while abc != 'True':
                    qqww += 1
                    print(abc)
                    print('Если вы передумали менять пароль, нажмите 1.')
                    print("Иначе введите корректный пароль.")
                    abc = input("Введите следующую команду: ")
                    if abc == '1':
                        first()
                    else:
                        zz = abc
                        password = password_level(abc)
                        if password == 'True':
                            break
                        else:
                            print(password)
                if qqww == 0:
                    Nicknames_passwords[nick] = new_password
                    print(1)
                else:
                    Nicknames_passwords[nick] = zz
            print(f"Новый пароль: {Nicknames_passwords[nick]}.")
            time.sleep(3)
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'посмотреть пароль':
            print(Nicknames_passwords[nick])
            time.sleep(1)
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'посмотреть адрес':
            print(f"{nick}@sendandgo.com")
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
                print()
        else:
            help(nick, word)


def stop_work():
    print()
    print(f"До свидания. Будем рады Вас видеть снова!")
    print()
    print("пппп   о   к  к     а       !")
    print("п  п  о о  к к     а  а     !")
    print("п  п о   о к      а    а    !")
    print("п  п  о о  к к   ааааааааа   ")
    print("п  п   о   к  к а         а !")
    print()
    sys.exit()


def entrance():
    global Nicknames_passwords, name
    if len(list(names_accounts.keys())) >= 1:
        name_chek = input("Введите никнейм: ")
        if name_chek in Nicknames_passwords:
            print()
            password = input("Введите Ваш пароль: ")
            count = 0
            zx = True
            while Nicknames_passwords[name_chek] != password:
                if zx:
                    print("Неверный пароль. Попробйте снова.")
                    print()
                    zx = False
                    continue
                count += 1
                password = input("Введите Ваш пароль: ")
                if password != Nicknames_passwords[name_chek] != password:
                    if count % 5 == 0:
                        print()
                        while not no_bot():
                            print("Попробуйте снова.")
                            print()
                        print("Для перехода на входную страницу нажмите 1")
                        print("Иначе - любую иную клавишу.")
                        print()
                        qwerty = input("Введите следующую команду: ")
                        if qwerty == str(1):
                            return False, name_chek
                    print()
                    print("Неверный пароль. Попробйте снова.")
                    continue
            name = name_chek
            return True, name_chek
        else:
            print("Аккаунт не найден.")
            return False, name_chek
    else:
        print("Для функционирования системы нужен минимум 1 аккаунт.")
        print("Пожалуйста, создайте аккаунт.")
        print()
        registration()
        return False, ''


def registration():
    global already, names_accounts
    nick = input("Укажите желаемый никнейм (не менее 3х символов): ")
    while nick in Nicknames_passwords or len(nick) < 3:
        if nick in Nicknames_passwords:
            nick = input("Такой ник уже занят. Попробуйте другой никнейм: ")
        else:
            nick = input("Никнейм короче 3х символов. Попробуйте другой: ")
    print()
    print("Сейчас нужно будет указать пароль для аккаунта.")
    print('''Пароль должен сстоять из букв РАЗНЫХ регистров И ЦИФР.''')
    print('''Длина пароля должна быть НЕ МЕНЕЕ 6 СИМВОЛОВ.''')
    print('''Наша платформа может сгенерировать надежный пароль за Вас.''')
    print()
    print("Если Вы хотите, чтобы система сгенерировала пароль, нажмите 1.")
    print("В противном случае нажмите на любую иную клавишу.")
    print()
    time.sleep(1)
    abc = input("Введите следующую команду: ")
    print()
    if abc == '1':
        password = make_password()
    else:
        password = input("Введите пароль: ")
        print()
        while password_level(password) != 'True':
            print(password_level(password))
            print()
            password = input("Введите пароль: ")
            print()
    abc = no_bot()
    while not abc:
        print("Попробуйте снова.")
        print()
        abc = no_bot()
    print(f"Пароль: {password}.")
    print('''Если Вы хотите вернуться на главную, нажите 1,''', end=' ')
    print('''но ваш аккаунт не будет сохранён.''')
    print("Иначе нажмите любую иную клавишу.")
    ne = input("Введите следующую команду: ")
    if ne == '1':
        first()
    print()
    print()
    server = what_server()
    print(f"Ваш аккаунт {nick} с паролем: {password} успешно создан.")
    Nicknames_passwords[nick] = password
    mail = MailClient(server, nick)
    already.append(mail)
    names_accounts[nick] = mail
    return [mail, False, nick]


def password_level(password):
    if len(password) < 6:
        return "Пароль короче 6 символов."
    letters, numbers, up = False, False, False
    for i in password:
        if i.lower() == i and i.isalpha():
            letters = True
        if ord(i) in range(48, 58):
            numbers = True
        if i.upper() == i and ord(i) not in range(48, 58):
            up = True
    if letters and numbers and up:
        return 'True'
    elif letters and numbers and not up:
        return "Добавьте заглавных букв."
    elif letters and up and not numbers:
        return "Добавьте цифр."
    elif numbers and up and not letters:
        return "Добавьте строчных букв."
    elif numbers and not letters and not up:
        return "Добавьте букв разных регистров."
    elif letters and not numbers and not up:
        return "Добавьте цифр и заглавных букв."
    else:
        return "Добавьте прописных букв и цифр."


def greeting():
    print()
    print('''Если у Вас уже есть свой аккаунт, введите "вход".''')
    print('''Иначе введите "регистрация".''')
    print('''Если Вы хотите выйти из нашей платформы - введите "выход".''')
    print()


def hello_goodbuy():
    print("" * 28)
    print()
    print("пппп  рр   и  и  ввв   еее   ттттт  !")
    print("п  п  р р  и  и  в  в  е       т    !")
    print("п  п  рр   и ии  ввв   еее     т    !")
    print("п  п  р    ии и  в  в  е       т    !")
    print("п  п  р    и  и  ввв   еее     т    !")
    print()
    print()
    print('Приветствуем на нашей экспериментальной платформе Send & Go!')


def generate_password():
    m = sample(range(6, 13), 1)[0]
    global generation, Nicknames_passwords
    result = []
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9']
    letters_low = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm',
                   'n', 'p', ]
    letters_up = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
                  'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in range(m):
        if i == 0:
            for i in range(4):
                spisok = ['1', '2', '3']
                q = sample(spisok, 1)[0]
                if q == '1':
                    result.append(sample(numbers, 1)[0])
                elif q == '2':
                    result.append(sample(letters_up, 1)[0])
                elif q == '3':
                    result.append(sample(letters_low, 1)[0])
                del spisok[spisok.index(q[0])]
        else:
            result.append(sample(generation, 1)[0])
    return ''.join(result)


def make_password():
    global Nicknames_passwords
    abc = list(Nicknames_passwords.keys())
    q = generate_password()
    while q in abc:
        q = generate_password()
    return q


def no_bot():
    op = sample(["сложения", "умножения", "вычитания"], 1)[0]
    ch = ['#fff44f', '#ff9966', '#b784a7', '#7b917b', '#470027']
    choose_color = sample(ch, 2)
    print(f"Введите результат {op.upper()} двух чисел на картинке.")
    im = Image.new("RGB", (1200, 800), choose_color[0])
    drawer = ImageDraw.Draw(im)
    drawer.rectangle(((0, 0), (1200, 400)), choose_color[1])
    check_result = sample(range(10, 49), 2)
    work_number = list(str(sum(check_result)))
    if op == "сложения":
        result = int(work_number[0]) + int(work_number[1])
    elif op == "умножения":
        result = int(work_number[0]) * int(work_number[1])
    elif op == "вычитания":
        result = int(work_number[0]) - int(work_number[1])
    mma = [(0, 0, 0), 'red', 'blue', (234, 160, 249), (255, 255, 255)]
    what_color = sample(mma, 1)[0]
    if work_number[0] == '1':
        drawer.rectangle(((100, 0), (200, 800)), what_color)
    elif work_number[0] == '2':
        drawer.rectangle(((100, 0), (500, 100)), what_color)
        drawer.rectangle(((400, 0), (500, 400)), what_color)
        drawer.rectangle(((100, 400), (500, 500)), what_color)
        drawer.rectangle(((100, 500), (200, 800)), what_color)
        drawer.rectangle(((100, 700), (500, 800)), what_color)
    elif work_number[0] == '3':
        drawer.rectangle(((200, 0), (500, 100)), what_color)
        drawer.rectangle(((200, 350), (500, 450)), what_color)
        drawer.rectangle(((200, 700), (500, 800)), what_color)
        drawer.rectangle(((400, 100), (500, 800)), what_color)
    elif work_number[0] == '4':
        drawer.rectangle(((200, 0), (300, 400)), what_color)
        drawer.rectangle(((400, 0), (500, 800)), what_color)
        drawer.rectangle(((300, 300), (500, 400)), what_color)
    elif work_number[0] == '5':
        drawer.rectangle(((200, 0), (500, 100)), what_color)
        drawer.rectangle(((200, 0), (300, 400)), what_color)
        drawer.rectangle(((200, 350), (500, 450)), what_color)
        drawer.rectangle(((400, 350), (500, 800)), what_color)
        drawer.rectangle(((200, 700), (500, 800)), what_color)
    elif work_number[0] == '6':
        drawer.rectangle(((200, 0), (500, 100)), what_color)
        drawer.rectangle(((200, 0), (300, 800)), what_color)
        drawer.rectangle(((200, 700), (500, 800)), what_color)
        drawer.rectangle(((400, 350), (500, 800)), what_color)
        drawer.rectangle(((300, 350), (500, 450)), what_color)
    elif work_number[0] == '7':
        drawer.rectangle(((200, 0), (500, 100)), what_color)
        drawer.rectangle(((300, 350), (600, 450)), what_color)
        drawer.rectangle(((400, 0), (500, 800)), what_color)
    elif work_number[0] == '8':
        drawer.rectangle(((200, 0), (500, 100)), what_color)
        drawer.rectangle(((200, 700), (500, 800)), what_color)
        drawer.rectangle(((200, 0), (300, 800)), what_color)
        drawer.rectangle(((400, 0), (500, 800)), what_color)
        drawer.rectangle(((200, 350), (500, 450)), what_color)
    elif work_number[0] == '9':
        drawer.rectangle(((200, 0), (500, 100)), what_color)
        drawer.rectangle(((200, 350), (500, 450)), what_color)
        drawer.rectangle(((400, 0), (500, 800)), what_color)
        drawer.rectangle(((200, 0), (300, 400)), what_color)
        drawer.rectangle(((200, 700), (500, 800)), what_color)
    elif work_number[0] == '0':
        drawer.rectangle(((200, 0), (500, 100)), what_color)
        drawer.rectangle(((200, 700), (500, 800)), what_color)
        drawer.rectangle(((200, 0), (300, 800)), what_color)
        drawer.rectangle(((400, 0), (500, 800)), what_color)
    wery = [(0, 0, 0), 'red', 'blue', (234, 160, 249), (255, 255, 255)]
    what_color = sample(wery, 1)[0]
    if work_number[1] == '1':
        drawer.rectangle(((700, 0), (800, 800)), what_color)
    elif work_number[1] == '2':
        drawer.rectangle(((700, 0), (1000, 100)), what_color)
        drawer.rectangle(((900, 0), (1000, 400)), what_color)
        drawer.rectangle(((700, 400), (1000, 500)), what_color)
        drawer.rectangle(((700, 500), (800, 800)), what_color)
        drawer.rectangle(((700, 700), (1000, 800)), what_color)
    elif work_number[1] == '3':
        drawer.rectangle(((600, 0), (900, 100)), what_color)
        drawer.rectangle(((600, 350), (900, 450)), what_color)
        drawer.rectangle(((600, 700), (900, 800)), what_color)
        drawer.rectangle(((800, 100), (900, 800)), what_color)
    elif work_number[1] == '4':
        drawer.rectangle(((600, 0), (700, 400)), what_color)
        drawer.rectangle(((800, 0), (900, 800)), what_color)
        drawer.rectangle(((700, 300), (900, 400)), what_color)
    elif work_number[1] == '5':
        drawer.rectangle(((600, 0), (900, 100)), what_color)
        drawer.rectangle(((600, 0), (700, 400)), what_color)
        drawer.rectangle(((600, 350), (900, 450)), what_color)
        drawer.rectangle(((800, 350), (900, 800)), what_color)
        drawer.rectangle(((600, 700), (900, 800)), what_color)
    elif work_number[1] == '6':
        drawer.rectangle(((600, 0), (900, 100)), what_color)
        drawer.rectangle(((600, 0), (700, 800)), what_color)
        drawer.rectangle(((600, 700), (900, 800)), what_color)
        drawer.rectangle(((800, 350), (900, 800)), what_color)
        drawer.rectangle(((700, 350), (900, 450)), what_color)
    elif work_number[1] == '7':
        drawer.rectangle(((600, 0), (900, 100)), what_color)
        drawer.rectangle(((700, 350), (1000, 450)), what_color)
        drawer.rectangle(((800, 0), (900, 800)), what_color)
    elif work_number[1] == '8':
        drawer.rectangle(((600, 0), (900, 100)), what_color)
        drawer.rectangle(((600, 700), (900, 800)), what_color)
        drawer.rectangle(((600, 0), (700, 800)), what_color)
        drawer.rectangle(((800, 0), (900, 800)), what_color)
        drawer.rectangle(((600, 350), (900, 450)), what_color)
    elif work_number[1] == '9':
        drawer.rectangle(((600, 0), (900, 100)), what_color)
        drawer.rectangle(((600, 350), (900, 450)), what_color)
        drawer.rectangle(((800, 0), (900, 800)), what_color)
        drawer.rectangle(((600, 0), (700, 400)), what_color)
        drawer.rectangle(((600, 700), (900, 800)), what_color)
    elif work_number[1] == '0':
        drawer.rectangle(((600, 0), (900, 100)), what_color)
        drawer.rectangle(((600, 700), (900, 800)), what_color)
        drawer.rectangle(((600, 0), (700, 800)), what_color)
        drawer.rectangle(((800, 0), (900, 800)), what_color)
    time.sleep(3)
    im.show()
    print()
    res_inp = input("Введите результат:  ")
    if str(res_inp) == str(result):
        return True
    return False


def first():
    abc = False
    nick = ''
    global names_accounts
    while not abc:
        greeting()
        res = input("Введите следующую команду: ")
        print()
        if res.lower() == 'регистрация':
            work = registration()
            abc = work[1]
            nick = work[2]
        elif res.lower() == 'вход':
            ttq = entrance()
            abc = ttq[0]
            nick = ttq[1]
        elif res.lower() == 'выход':
            stop_work()
        else:
            print("Некорректный запрос.")
            abc = False
            time.sleep(3)
    else:
        print("Добро пожаловать в Ваш личный кабинет!")
        print()
        second(nick)
        zapros(nick)


save = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
        'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z', '2', '3', '4', '5', '6', '7', '8', '9']
generation = save * 4


class MailClient:
    def __init__(self, server, user):
        self.server = server
        self.user = user
        self.messages = {}
        self.servers = ["inbox", "gmail", "icloud", "mail", "list"]
        self.deletion = True
        self.nastroi = True

    def help(self):
        print()
        print("Здравствуйте! Я - Ваш помощник на платформе Send & Go.")
        print()
        print('''Если Вам потребуется помощь, введите "помощь".''')
        time.sleep(0.5)
        print('''Для выхода в стартовое меню введите "на главную".''')
        time.sleep(0.5)
        print('''Для выхода из нашей платформы, введите "выход".''')
        time.sleep(0.5)
        print('''Для написания письма введите "отправить".''')
        time.sleep(0.5)
        print('''Для просмотра входящих писем введите "входящие".''')
        time.sleep(0.5)
        print('''Для удаления сообщения введите "удалить сообщение".''')
        time.sleep(0.5)
        print('''Для смены сервера введите "сменить сервер".''')
        time.sleep(0.5)
        print('''Для просмотра сервера введите''', end=' ')
        print('''"текущий сервер".''')
        time.sleep(0.5)
        print('''Для просмотра пароля ввелите "посмотреть пароль".''')
        time.sleep(0.5)
        print('''Для изменения пароля введите "изменить пароль".''')
        time.sleep(0.5)
        print('''Для того, чтобы узнать полный адрес Вашей почты,''', end=' ')
        print(''' введите "посмотреть адрес".''')

    def change_server(self, new_server):
        if new_server.strip() in self.servers:
            print(f"Успешная замена сервера на {new_server}.")
            self.server = new_server
            return True
        else:
            print(f"В списке доступных северов нет сервера {new_server}.")
            print("Повторите попытку.")
            return False

    def send_mail(self, server, name, text):
        print(f"Письмо отправлено пользователю '{name}' на сервер '{server}'.")
        names_accounts[name].messages[str(dt.datetime.now())] = self.user, text

    def delete(self, date):
        del self.messages[str(date)]
        print("Сообщение удалено.")

    def get_server(self):
        print(self.server)


def help(nick, word):
    count = 0
    global start_commands, Nicknames_passwords, already, names_accounts, spisok
    print()
    while 2 < 9:
        if word.lower() == 'на главную':
            first()
            second(nick)
        elif word == 'помощь':
            names_accounts[nick].help()
            print()
            word = input("Введите следующую команду:  ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word == 'отправить':
            print(f"Допустимые сервера: {', '.join(spisok)}")
            print()
            server = input("Введите сервер получателя: ")
            while server not in spisok:
                count += 1
                if count % 5 == 0:
                    while not no_bot():
                        print("Попробуйте снова.")
                        print("Если вы хотите перейти на главную", end=' ')
                        print("-  введите 1.")
                        print("Иначе нажмите любую иную клавишу.")
                        print()
                        qwerty = input("Введите следующую команду: ")
                        print()
                        if qwerty == str(1):
                            first()
                            second(nick)
                print("Сервер не найден. Попробуйте еще раз.")
                print()
                server = input("Введите сервер получателя: ")
            name = input("Введите никнейм поучателя: ")
            while name not in Nicknames_passwords:
                print()
                print(f"Пользователь с никнеймом {name} не найден.")
                print('''Если Вы хотите вернуться на гланую - введите 1.''')
                print("Иначе введите корректное имя пользователя.")
                print()
                name = input('Введите следующую команду: ')
                if name == '1':
                    first()
            print()
            while names_accounts[name].server != server:
                print(f"Пользователь с никнеймом {name}", end=' ')
                print(f"на сервере {server} не найден.")
                print('''Если Вы хотите вернуться на главную - введите 1.''')
                print("Иначе введите корректный сервер.")
                print()
                print('Если Вам нужно узнать сервер получателя, нажмите 2.')
                print()
                word = input("Введите следующую команду: ")
                if word != '1' and word != '2':
                    server = word
                if word.lower() == '1':
                    first()
                    second(nick)
                elif word.lower() == '2':
                    print(names_accounts[name].server)
                    continue
            text = input("Введите текст: ")
            while len(text) < 1:
                print()
                print("Пустое письмо не может быть отправлено.")
                print('''Если Вы хотите вернуться на гланую - введите 1.''')
                print("Иначе введите корректный сервер.")
                print()
                text = input("Введите следующую команду: ")
                if text.lower() == '1':
                    first()
                    second(nick)
            names_accounts[nick].send_mail(server, name, text)
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'сменить сервер':
            print(f"Список доступных серверов: {', '.join(spisok)}")
            print(f"Выберете сервер для смены.")
            change = input("Введите сервер: ")
            while change not in spisok:
                print("Сервер не найден.")
                print('''Если Вы хотите вернуться на гланую - введите 1.''')
                print("Иначе введите корректный сервер.")
                print()
                change = input("Введите следующую команду: ")
                if change.lower() == '1':
                    first()
                    second(nick)
            result = names_accounts[nick].change_server(change)
            while not result:
                result = names_accounts[nick].change_server(change)
                print('''Если Вы хотите вернуться на гланую - введите 1.''')
                print("Иначе введите корректный сервер.")
                print()
                change = input("Введите следующую команду: ")
                if change.lower() == '1':
                    first()
                    second(nick)
            word = input("Введите следующую команду: ")
            print()
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'входящие':
            if names_accounts[nick].messages != {}:
                res = names_accounts[nick].messages
                keys = list(res.keys())
                val = list(res.values())
                for i in range(len(keys)):
                    abc = keys[i].split()
                    print(f"Сообщение от пользователя: {val[i][0]}.")
                    print(f"Получено {abc[0]} в {abc[1]}.")
                    print(f"Текст сообщения: '{val[i][1]}'.")
                    print()
                if not names_accounts[nick].deletion:
                    names_accounts[nick].messages = {}
            else:
                print("Нет сообщений.")
                print()
            word = input("Введите следующую команду: ")
            print()
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == "удалить сообщение":
            if names_accounts[nick] != {}:
                data = input("Введите дату и время сообщения ЧЕРЕЗ ПРОБЕЛ: ")
                print()
                while data not in names_accounts[nick].messages:
                    print("Сообщение не найдено.")
                    print("Для выхода на главную - введите 1.")
                    print("Если Вам нужно узнать дату и время", end=' ')
                    print("сообщения, нажмите 2 и выбирете нужную", end=' ')
                    print("дату и время в открывшемся списке Ваших сообщений.")
                    print("Иначе нажмите любую иную клавишу.")
                    zx = input("Введите следующую команду: ")
                    print()
                    if zx == '1':
                        first()
                        second(nick)
                    if zx == '2':
                        res = names_accounts[nick].messages
                        keys = list(res.keys())
                        val = list(res.values())
                        for i in range(len(keys)):
                            abc = keys[i].split()
                            print(f"Сообщение от пользователя: {val[i][0]}.")
                            print(f"Получено {abc[0]} в {abc[1]}.")
                            print(f"Текст сообщения: '{val[i][1]}'.")
                            print()
                    print("Введите дату и время сообщения ЧЕРЕЗ ПРОБЕЛ: ")
                    data = input("Введите дату и время: ")
                else:
                    print("Если вы передумали - введите 1.")
                    print("Иначе нажмите любую иную клавишу.")
                    print()
                    mma = input("Введите следующую команду: ")
                    if mma != '1':
                        names_accounts[nick].delete(data)
                    word = input("Введите следующую команду: ")
                while word.lower() not in start_commands:
                    word = input("Введите корректную команду: ")
                    print()
            else:
                print("Нет сообщений.")
                print()
                word = input("Введите следующую команду: ")
                while word.lower() not in start_commands:
                    word = input("Введите корректную команду: ")
                    print()
        if word.lower() == 'выход':
            stop_work()
        elif word.lower() == 'текущий сервер':
            names_accounts[nick].get_server()
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'удаление':
            if not names_accounts[nick].deletion:
                names_accounts[nick].deletion = True
                print("Теперь сообщения НЕ БУДУТ удаляться автоматически.")
            else:
                names_accounts[nick].deletion = False
                print("Теперь сообщения БУДУТ удаляться автоматически.")
                word = input("Введите следующую команду: ")
                while word.lower() not in start_commands:
                    word = input("Введите корректную команду: ")
                    print()
        elif word.lower() == 'изменить пароль':
            qqww = 0
            abm = no_bot()
            while not abm:
                print('Попробуйте снова.')
                abm = no_bot()
            print('Новый пароль должен быть не короче 6 символов,', end=' ')
            print("содержать буквы ВСЕХ РЕГИСТРОВ и ЦИФРЫ.")
            print('Наша платформа может сама сгенерировать надежный пароль.')
            print('Если вы передумали менять пароль, нажмите 1.')
            print('Если Вы хотите, чтобы наша платфора', end=' ')
            print('сгенерировала пароль, нажмите 2.')
            print('В других случаях введите новый пароль.')
            new_password = input('Введите седующую команду: ')
            if new_password == '1':
                first()
            elif new_password == '2':
                Nicknames_passwords[nick] = generate_password()
            else:
                abc = password_level(new_password)
                while abc != 'True':
                    qqww += 1
                    print(abc)
                    print('Если вы передумали менять пароль, нажмите 1.')
                    print("Иначе введите корректный пароль.")
                    abc = input("Введите следующую команду: ")
                    if abc == '1':
                        first()
                    else:
                        zz = abc
                        password = password_level(abc)
                        if password == 'True':
                            break
                        else:
                            print(password)
                if qqww == 0:
                    Nicknames_passwords[nick] = new_password
                    print(1)
                else:
                    Nicknames_passwords[nick] = zz
            print(f"Новый пароль: {Nicknames_passwords[nick]}.")
            time.sleep(3)
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'посмотреть пароль':
            print(Nicknames_passwords[nick])
            time.sleep(1)
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
        elif word.lower() == 'посмотреть адрес':
            print(f"{nick}@sendandgo.com")
            print()
            word = input("Введите следующую команду: ")
            while word.lower() not in start_commands:
                word = input("Введите корректную команду: ")
                print()
                print()
        else:
            zapros(nick, word)


def second(nick):
    global names_accounts
    if names_accounts[nick].nastroi:
        print("Пожалуйста, пройдите предстартовую настройку аккаунта.")
        time.sleep(0.5)
        print("Если вы хотите, чтобы письма удалялись после", end=' ')
        print("прочтения - введите 1, иначе любую другую клавишу.")
        time.sleep(0.5)
        moving = input("Введите следующую команду: ")
        if moving == '1':
            names_accounts[nick].delete = False
        print('''Поменять эту настройку Вы всегда сможете''', end=' ')
        print('''вызвав команду "удаление".''')
        print()
        names_accounts[nick].nastroi = False
        time.sleep(0.5)
    print('''Тепер Вы можете использовать все возможности нашей платформы.''')
    time.sleep(0.5)
    print('''Если Вам потребуется помощь, введите "помощь".''')
    time.sleep(0.5)
    print('''Для выхода в стартовое меню введите "на главную".''')
    time.sleep(0.5)
    print('''Для выхода из нашей платформы, введите "выход".''')
    time.sleep(0.5)
    print('''Для написания письма введите "отправить".''')
    time.sleep(0.5)
    print('''Для просмотра входящих писем введите "входящие".''')
    time.sleep(0.5)
    print('''Для удаления сообщения введите "удалить сообщение".''')
    time.sleep(0.5)
    print('''Для смены сервера введите "сменить сервер".''')
    time.sleep(0.5)
    print('''Для просмотра сервера введите''', end=' ')
    print('''"текущий сервер".''')
    time.sleep(0.5)
    print('''Для просмотра пароля ввелите "посмотреть пароль".''')
    time.sleep(0.5)
    print('''Для изменения пароля введите "изменить пароль".''')
    time.sleep(0.5)
    print('''Для того, чтобы узнать полный адрес Вашей почты,''', end=' ')
    print('''введите "посмотреть адрес".''')


start_commands = ["помощь", "на главную", "отправить"]
a = ["входящие", "удалить сообщение", "выход"]
bb = ["сменить сервер", "текущий сервер", "удаление"]
for i in range(3):
    if i == 0:
        start_commands.append('изменить пароль')
        start_commands.append('посмотреть пароль')
        start_commands.append('посмотреть адрес')
    start_commands.append(a[i])
    start_commands.append(bb[i])
already = []
spisok = ["inbox", "gmail", "icloud", "mail", "list"]
name = ''
Nicknames_passwords = {}
names_accounts = {}
hello_goodbuy()
first()
