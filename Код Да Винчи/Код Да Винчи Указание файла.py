from tkinter import *
from random import sample, choice
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
import socket
import time
from re import findall
import sys

def Cesar(step, text):
    work_step = int((str(step)[0])) + int(str(step)[-1]) // 2
    shifr = []
    for i in list(text):
        shifr.append(chr(ord(i) + work_step))
    return ''.join(shifr)


def DeCesar(step, text):
    work_step = int((str(step)[0])) + int(str(step)[-1]) // 2
    shifr = []
    for i in list(text):
        shifr.append(chr(ord(i) - work_step))
    return ''.join(shifr)

print('''Запуск программы "Код Да Винчи". Пожалуйста, подождите...''')
popop = True
book = ''
work_file = ''
cod = 0
sh = ''
text = 0
step = 0
password = 0
root1 = 0
msg = ''
shifter = ''
root2 = 0
flag = True
step1 = 0
entry_password =''
entry_adress = ''
res = 26
save = []
flag1 = True
def regular(text):
    return findall(r"[0-9]+", text)


def encryptDecrypt(mode, message):
    global book
    final = ''
    if mode.upper() == 'E':
        for symbolMessage in message:
            listIndexKey = []
            for indexKey, symbolKey in enumerate(book):
                if symbolMessage == symbolKey:
                    listIndexKey.append(indexKey)
            try:
                final += str(choice(listIndexKey)) + '/'
            except IndexError:
                pass
    else:
        for numbers in regular(message):
            for indexKey, symbolKey in enumerate(book):
                if numbers == str(indexKey):
                    final += symbolKey
    return final



def entance():
    print('''Работа программы "Код Да Винчи" успешна завершена.''')
    time.sleep(1)
    sys.exit()

def desh1():
    global root, shifter, step1, code, flag, msg, work_file
    if flag:
        root.destroy()
    else:
        msg.destroy()
    root = Tk()  # создаём рабочее окно
    root.title("Дешифровка")  # называем его "Дешифровка"
    root.geometry('800x550')  # задаём его размер 800x800 пикселей
    root.configure(bg='blue')  # задаем основной цвет
    root.resizable(False, False)  # запрещаем изменять его размеры
    # надписи
    label_text2 = Label(root, bg='blue', fg='white', text='''* в поле "Располжение текста:" укажите путь к файлу для шифрования и его имя.''',font='times 14')
    label_text2.pack()
    label_text2.place(x=20, y=40)
    label_shifr = Label(root, bg='blue', fg='white', text='Введите шифр: ',font='times 26')  # сощдаём надпись на экране
    label_shifr.place(x=20, y=75)  # начало записи с координат (20;75)
    label_step = Label(root, bg='blue', fg='white', text='Введите шаг: ', font='times 26')  # сощдаём надпись на экране
    label_step.place(x=20, y=150)  # начало записи с координат (20;150)
    label_code = Label(root, bg='blue', fg='white', text='Введите серетный код: ',font='times 26')  # сощдаём надпись на экране
    label_code.place(x=20, y=225)  # начало записи с координат (20;225)
    label_file = Label(root, bg='blue', fg='white', text='Расположение текста: ', font='times 26')
    label_file.place(x=20, y=300)
    shifter = StringVar()
    step1 = StringVar()
    code = StringVar()
    work_file = StringVar()
    # поля ввода
    entry_file = Entry(root, bg='#00bfff', fg='red', font='times 26', textvariable=work_file)
    entry_file.place(x=400, y=300)
    entry_shift = Entry(root, bg='#00BFFF', fg='red', font='times 26', textvariable=shifter)
    entry_shift.place(x=400, y=75)
    entry_step = Entry(root, bg='#00BFFF', fg='red', font='times 26', textvariable=step1)
    entry_step.place(x=400, y=150)
    entry_code = Entry(root, bg='#00BFFF', fg='red', font='times 26', textvariable=code)
    entry_code.place(x=400, y=225)
    #  кнопки
    result = Button(root, bg='#00BFFF', fg='red', text='Дешифровать', font='times 34', activebackground='yellow',activeforeground='#FF8C00', command=deshifr)
    result.place(x=250, y=425)
    ex = Button(root, bg='#00BFFF', fg='red', text='Выход', font='times 16', activebackground='yellow',activeforeground='#FF8C00', command=entance)
    ex.place(x=685, y=475)

def gl():
    global root, root1, root2, save, res, flag, flag1
    flag = True
    flag1 = True
    save = []
    res = 26
    root2.destroy()
    root = Tk()
    root.title("Главная")  # называем его "Дешифровка"
    root.geometry('1100x650')  # задаём его размер 800x800 пикселей
    root.configure(bg='blue')  # задаем основной цвет
    root.resizable(False, False)  # запрещаем изменять его размеры
    lbl = Label(root, bg='blue', fg='white', font='times 16', text='Разработано Николаем Олеговичеи Немовым.')
    lbl.place(x=155, y=600)
    lbl1 = Label(root, bg='blue', fg='white', font='times 36', text='Код Давинчи')
    lbl1.place(x=405, y=130)
    lbl2 = Label(root, bg='blue', fg='white', font='times 30', text='Выберите дальнейше действие:')
    lbl2.place(x=280, y=280)
    button = Button(root, bg='#00BFFF', fg='red', text='Зашифровать', font='times 34', activebackground='yellow', activeforeground='#FF8C00', command=shifr)
    button.place(x=155, y=450)
    result = Button(root, bg='#00BFFF', fg='red', text='Дешифровать', font='times 34', activebackground='yellow', activeforeground='#FF8C00', command=desh1)
    result.place(x=640, y=450)
    ex = Button(root, bg='#00BFFF', fg='red', text='Выход', font='times 16', activebackground='yellow', activeforeground='#FF8C00', command=entance)
    ex.place(x=865, y=600)
    root.mainloop()


def send_mail(code):
    global adress_get1, step, root1
    try:
        entr_text = Label(root1, bg='blue', fg='red', font='times 26', text='Поле больше недоступно.')
        entr_text.place(x=650, y=75)
        ent2r_text = Label(root1, bg='blue', fg='red', font='times 26', text='Поле больше недоступно.')
        ent2r_text.place(x=650, y=150)
        ent3r_text = Label(root1, bg='blue', fg='red', font='times 26', text='Поле больше недоступно.')
        ent3r_text.place(x=650, y=375)
    except Exception:
        pass
    try:
        socket.gethostbyaddr('www.yandex.ru')
    except socket.gaierror:
        messagebox.showinfo("Шифрование", "Проверьте подключение к интернету.")
        return False
    login = 'shifrovalshchik@list.ru'
    work = 'Zxoiet123'
    qqq = "smtp.list.ru"
    to = adress_get1.get()
    msg = MIMEMultipart()
    msg['Subject'] = 'Данные для расшифровки'
    msg['From'] = login
    body = f'''Шаг: {step.get()}. Секретный код: {code}.'''
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP_SSL(qqq, 465)
    server.login(login, work)
    try :
        server.sendmail(login, to, msg.as_string())
    except Exception:
        messagebox.showinfo("Шифрование", "Проверьте корректность введённого адреса получателя шага, кода.")
        return False
    server.quit()
    return True

def send_mail_only(text):
    global adress_get2, root1
    try:
        entr15_text = Label(root1, bg='blue', fg='red', font='times 26', text='Поле больше недоступно.')
        entr15_text.place(x=650, y=225)
    except Exception:
        pass
    try:
        socket.gethostbyaddr('www.yandex.ru')
    except socket.gaierror:
        messagebox.showinfo("Шифрование", "Проверьте подключение к интернету.")
        return False
    login = 'shifrovalshchik@list.ru'
    work = "Zxoiet123"
    qqq = "smtp.list.ru"
    to = adress_get2.get()
    msg = MIMEMultipart()
    msg['Subject'] = 'Данные для расшифровки'
    msg['From'] = login
    body = f'''Шифр: {text}.'''
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP_SSL(qqq, 465)
    server.login(login, work)
    try:
        server.sendmail(login, to, msg.as_string())
    except Exception:
        messagebox.showinfo("Шифрование", "Проверьте корректность введённого адреса получателя шифра.")
        return False
    server.quit()
    try:
        entr5_text = Label(root1, bg='blue', fg='red', font='times 26', text='Поле больше недоступно.')
        entr5_text.place(x=650, y=300)
    except Exception:
        pass
    return True


def permittion():
    global root1, root, adress_get2, adress_get1, root2
    root1.destroy()
    root2 = Tk()
    root2.title("Подтверждение")  # называем его "Дешифровка"
    root2.geometry('1100x450')  # задаём его размер 800x800 пикселей
    root2.configure(bg='blue')
    root2.resizable(True, False)
    label_text = Label(root2, bg='blue', fg='white', text=f'Шифр отправлен на почту: {adress_get2.get()}', font='times 26')  # сощдаём надпись на экране
    label_text.place(x=20, y=75)  # начало записи с координат (20;75)
    label_text = Label(root2, bg='blue', fg='white', text=f'Шаг и секретный код отправлены на почту: {adress_get1.get()}',font='times 26')  # сощдаём надпись на экране
    label_text.place(x=20, y=150)  # начало записи с координат (20;75)
    button = Button(root2, bg='#00BFFF', fg='red', text='На главную', font='times 34', activebackground='yellow', activeforeground='#FF8C00', command=gl)
    button.place(x=420, y=325)
    ex = Button(root2, bg='#00BFFF', fg='red', text='Выход', font='times 16', activebackground='yellow', activeforeground='#FF8C00', command=entance)
    ex.place(x=1000, y=400)
    root2.mainloop()

def shh():
    global step, text, sh, adress, adress_get1, password, root1, entry_password, entry_adress, flag1
    tex = list(text.get())
    stepp = int(step.get())
    if len(str(stepp)) > 4:
        stepp = int(str(stepp)[:4])
    if stepp <= 0:
        stepp = abs(stepp)
    if stepp == 0:
        stepp = 7
    a = False
    rand = sample(range(219,1000), 1)[0]
    if flag1:
        tex.reverse()
        sh = encryptDecrypt('E', ''.join(tex))
        sh = (str((rand // stepp) + 2) + '/') + sh
        sh = sh + (str((rand + stepp) // 28) + '/')
        sh = Cesar(int(str(stepp)[0]) + int(str(rand)[-1]), sh)
        a = send_mail(rand)
        while not a:
            entry_adress = Entry(root1, bg='#00BFFF', fg='red', font='times 26', textvariable=adress_get1)
            entry_adress.pack()
            entry_adress.place(x=650, y=225)
            root1.mainloop()
            a = send_mail(rand)
    flag1 = False
    b = send_mail_only(sh)
    while not b:
        entry_password = Entry(root1, bg='#00BFFF', fg='red', font='times 26', textvariable=adress_get2)
        entry_password.pack()
        entry_password.place(x=650, y=300)
        root1.mainloop()
        b = send_mail_only(sh)
    permittion()



def check():
    global text, step, adress, adress_get1, adress_get2, password, cod, sh, root, work_file, book
    #проверка на пустоту
    if work_file.get() == '':
        messagebox.showinfo("Шифрование", "Введите путь к файлу для шифрования.")
        return False
    try:
        with open(rf"{work_file.get() + '.txt'}") as text_file:
            work_text = open(rf"{work_file.get() + '.txt'}")
        book = work_text.read()
    except Exception:
        messagebox.showinfo("Шифрование", f"Файл с расположением {work_file.get()} не найден или его формат не поддерживается программой.")
        return False
    if text.get() == '':
        messagebox.showinfo("Шифрование", "Введите текст.")
        return False
    if len(text.get()) > 240:
        messagebox.showinfo("Шифрование", f"Длина введённого текста: {len(text.get())}. Максимально допустимый объём текста: 240 символов.")
        return False
    if step.get() == '':
        messagebox.showinfo("Шифрование", "Введите шаг шифрования.")
        return False
    if adress_get1.get() == '':
        messagebox.showinfo("Шифрование", "Введите адрес почты получателя кода, шага.")
        return False
    if adress_get2.get() =='':
        messagebox.showinfo("Шифрование", "Введите адрес почты получателя шифра.")
        return False
    #условия
    if not step.get().isdigit():
        messagebox.showinfo("Шифрование", "Шаг должен состоять только из цифр.")
        return False
    if '@' not in adress_get1.get() or '.' not in adress_get1.get():
        messagebox.showinfo("Шифрование", "Введите корректный адрес почты получателя кода, шага.")
        return False
    if '@' not in adress_get2.get() or '.' not in adress_get2.get():
        messagebox.showinfo("Шифрование", "Введите корректный адрес почты получателя шифра.")
        return False
    shh()


def pl():
    global res, msg, save
    if res < 30:
        msg_label = Label(msg, bg='blue', fg='blue', text=f'''Расшифрованный текст: "{''.join(save)}"''', font=f'times {res}')
        msg_label.pack()
        msg_label.place(x=20, y=75)
        res += 1
        msg_label = Label(msg, bg='blue', fg='white', text=f'''Расшифрованный текст: "{''.join(save)}"''', font=f'times {res}')
        msg_label.pack()
        msg_label.place(x=20, y=75)
        return
    else:
        messagebox.showinfo("Расшифрованный текст", "Достигнут максимальный размер шрифта.")
        return

def mn():
    global res, msg, save
    if res > 12:
        msg_label = Label(msg, bg='blue', fg='blue', text=f'''Расшифрованный текст: "{''.join(save)}"''', font=f'times {res}')
        msg_label.pack()
        msg_label.place(x=20, y=75)
        res -= 1
        msg_label = Label(msg, bg='blue', fg='white', text=f'''Расшифрованный текст: "{''.join(save)}"''', font=f'times {res}')
        msg_label.pack()
        msg_label.place(x=20, y=75)
        return
    else:
        messagebox.showinfo("Расшифрованный текст", "Достигнут минимальный размер шрифта.")
        return


def deshifr():
    global shifrer, step1, code, root, msg, root2, save, work_file, book
    tex, ste, cod = shifter.get(), step1.get(), code.get()
    if tex == '':
        messagebox.showinfo("Дешифровка", "Заполните поле текста.")
        return
    if ste =='':
        messagebox.showinfo("Дешифровка", "Заполните поле шага.")
        return
    if cod == '':
        messagebox.showinfo("Дешифровка", "Заполните поле секретного кода.")
        return
    if not ste.isdigit():
        messagebox.showinfo("Дешифровка", "Шаг должен состоять только из чисел.")
        return
    if not cod.isdigit():
        messagebox.showinfo("Дешифровка", "Секретный код должен состоять только из чисел.")
        return
    if work_file.get() == '':
        messagebox.showinfo("Дешифровка", "Введите путь к файлу для дешифрования.")
        return
    try:
        with open(rf"{work_file.get() + '.txt'}") as text_file:
            work_text = open(rf"{work_file.get() + '.txt'}")
        book = work_text.read()
    except Exception:
        messagebox.showinfo("Дешифровка", f"Файл с расположением {work_file.get()} не найден или его формат не поддерживается программой.")
        return False
    step2 = int(ste)
    code2 = int(cod)

    if len(str(code2)) > 3:
        code2 = int(str(code2)[:3])
    elif code2 <= 0:
        code2 = 7
    save = []
    if len(str(step2)) > 4:
        step2 = int(str(step2)[:4])
    elif step2 <= 0:
        step2 = abs(step2)
    if step2 == 0:
        step2 = 7
    tex = DeCesar(int(str(step2)[0]) + int(str(code2)[-1]), tex)
    if str((code2 // step2) + 2) != tex.split('/')[0] or (str((code2 + step2) // 28)) != tex.split('/')[-2]:
        messagebox.showinfo("Дешифровка", "Секретный код или (и) шаг указан(ы) неверно.")
        return
    tex = tex.split('/')
    tex = tex[1:len(tex) - 2]
    tex = '/'.join(tex)
    save = list(encryptDecrypt('D', tex))
    save.reverse()
    root.destroy()
    msg = Tk()
    msg.title("Расшифрованный текст")
    msg.geometry("800x400")
    msg.resizable(True, False)
    msg.configure(bg='blue')
    msg_label = Label(msg, bg='blue', fg='white', text=f'''Расшифрованный текст: "{''.join(save)}"''',font=f'times {res}')
    msg_label.place(x=20, y=75)
    plus = Button(msg, bg='#00BFFF', fg='red', text='Увеличить', font='times 16', activebackground='yellow',activeforeground='#FF8C00', command=pl)
    plus.place(x=20, y=350)
    minus = Button(msg, bg='#00BFFF', fg='red', text='Уменьшить', font='times 16', activebackground='yellow', activeforeground='#FF8C00', command=mn)
    minus.place(x=160, y=350)
    sh_label = Label(msg, bg='blue', fg='white', text=f'Изменение размера шрифта', font=f'times 20')
    sh_label.place(x=20, y=280)
    button = Button(msg, bg='#00BFFF', fg='red', text='На главную', font='times 30', activebackground = 'yellow', activeforeground = '#FF8C00', command=gl)
    button.place(x=300, y=170)
    ex = Button(msg, bg='#00BFFF', fg='red', text='Выход', font='times 16', activebackground='yellow', activeforeground='#FF8C00', command=entance)
    ex.place(x=700, y=350)
    ex = Button(msg, bg='#00BFFF', fg='red', text='Выход', font='times 16', activebackground='yellow',activeforeground='#FF8C00', command=entance)
    ex.place(x=685, y=500)
    root2 = msg
    msg.mainloop()


def shifr():
    global text, step, adress, adress_get1, adress_get2, url, password, cod, sh, root, root1, entry_password, entry_adress, work_file
    root.destroy()
    root1 = Tk()
    root1.title("Шифрование")  # называем его "Дешифровка"
    root1.geometry('1100x550')  # задаём его размер 800x800 пикселей
    root1.configure(bg='blue')  # задаем основной цвет
    root1.resizable(False, False)  # запрещаем изменять его размеры
    text = StringVar()
    step = StringVar()
    work_file = StringVar()
    adress_get1 = StringVar()
    adress_get2 = StringVar()

    label_text = Label(root1, bg='blue', fg='white', text='Текст для шифрования: ', font='times 26')  # сощдаём надпись на экране
    label_text.pack()
    label_text.place(x=20, y=75)  # начало записи с координат (20;75)
    label_text1 = Label(root1, bg='blue', fg='white', text='* длина текста, который будет зашифрован, не должна превышать 240 символов.',font='times 14')  # сощдаём надпись на экране
    label_text1.pack()
    label_text1.place(x=20, y=40)
    label_text2 = Label(root1, bg='blue', fg='white', text='''* в поле "Располжение текста:" укажите путь к файлу для шифрования и его имя. Текст должен быть в формате txt.''' ,font='times 14')
    label_text2.pack()
    label_text2.place(x=20, y=15)
    label_step = Label(root1, bg='blue', fg='white', text='Шаг шифрования: ',
                       font='times 26')  # сощдаём надпись на экране
    label_step.pack()
    label_step.place(x=20, y=150)  # начало записи с координат (20;150)
    label_adress_get1 = Label(root1, bg='blue', fg='white', text='Адрес почты получателя кода, шага: ',
                              font='times 26')  # сощдаём надпись на экране
    label_adress_get1.pack()
    label_adress_get1.place(x=20, y=225)  # начало записи с координат (20;225)
    label_adress_get2 = Label(root1, bg='blue', fg='white', text='Адрес почты получателя шифра: ',
                              font='times 26')  # сощдаём надпись на экране
    label_adress_get2.pack()
    label_adress_get2.place(x=20, y=300)  # начало записи с координат (20;225)

    label_text = Label(root1, bg='blue', fg='white', text='Располжение текста: ', font='times 26')
    label_text.pack()
    label_text.place(x=20, y=375)
    entry_text = Entry(root1, bg='#00BFFF', fg='red', font='times 26', textvariable=text)
    entry_text.place(x=650, y=75)
    entry_step = Entry(root1, bg='#00BFFF', fg='red', font='times 26', textvariable=step)
    entry_step.place(x=650, y=150)
    entry_adress = Entry(root1, bg='#00BFFF', fg='red', font='times 26', textvariable=adress_get1)
    entry_adress.pack()
    entry_adress.place(x=650, y=225)
    entry_password = Entry(root1, bg='#00BFFF', fg='red', font='times 26', textvariable=adress_get2)
    entry_password.pack()
    entry_password.place(x=650, y=300)
    entry_way = Entry(root1, bg='#00BFFF', fg='red', font='times 26', textvariable=work_file)
    entry_way.pack()
    entry_way.place(x=650, y=375)
    button = Button(root1, bg='#00BFFF', fg='red', text='Зашифровать', font='times 34', activebackground='yellow', activeforeground='#FF8C00', command=check)
    ex = Button(root1, bg='#00BFFF', fg='red', text='Выход', font='times 16', activebackground='yellow', activeforeground='#FF8C00', command=entance)
    ex.place(x=935, y=495)
    button.place(x=420, y=445)
    root1.mainloop()



root = Tk()  # создаём рабочее окно
password = StringVar()
adress_get1 = StringVar()
adress_get2 = StringVar()
root.title("Главная")  # называем его "Дешифровка"
root.geometry('1100x650')  # задаём его размер 800x800 пикселей
root.configure(bg='blue')  # задаем основной цвет
root.resizable(False, False)  # запрещаем изменять его размеры
lbl = Label(root, bg='blue', fg='white', font='times 16', text='Разработано Николаем Олеговичеи Немовым.')
lbl.place(x=155, y=600)
lbl1 = Label(root, bg='blue', fg='white', font='times 36', text='Код Да Винчи')
lbl1.place(x=405, y=130)
lbl2 = Label(root, bg='blue', fg='white', font='times 30', text='Выберите дальнейше действие:')
lbl2.place(x=280, y=280)
button = Button(root, bg='#00BFFF', fg='red', text='Зашифровать', font='times 34', activebackground = 'yellow', activeforeground = '#FF8C00', command=shifr)
button.place(x=155, y=450)
result = Button(root, bg='#00BFFF', fg='red', text='Дешифровать', font='times 34', activebackground = 'yellow', activeforeground = '#FF8C00', command=desh1)
result.place(x=640, y=450)
ex = Button(root, bg='#00BFFF', fg='red', text='Выход', font='times 16', activebackground = 'yellow', activeforeground = '#FF8C00', command=entance)
ex.place(x=865, y=600)
print('''Программа "Код Да Винчи" успешно запущена.''')
root.mainloop()
