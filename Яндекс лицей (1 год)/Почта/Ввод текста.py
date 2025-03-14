from tkinter import filedialog
import shutil, mimetypes
import os
from email.mime.base import MIMEBase
from email import encoders
import smtplib, string, socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import sample
from tkinter import *
from tkinter import messagebox
from ctypes import *
import random


def get_file(*args):
    root = Tk()
    root.focus()
    root.withdraw()
    # messagebox.showinfo("Ввод текста", 'Выберите файл для записи текста.')
    file = filedialog.askopenfilename(title="Выбор файла для записи",
                                      filetypes=(("txt files", "*.txt"), ("txt files", "*.txt")))
    while not os.path.isfile(file):
        messagebox.showerror("Ввод текста",
                                 "Файл для записи не был выбран." + '\n' + 'Для выхода из программы закройте это сообщение и в появившемся окне нажмите No.' + '\n' + "Иначе нажмите Yes и выберите файл для записи.")
        answer = messagebox.askyesno(title="Ввод текста", message="Выбрать файл для записи?")
        if not answer:
            sys.exit()
        file = filedialog.askopenfilename(title="Выбор файла для записи",
                                              filetypes=(("txt files", "*.txt"), ("txt files", "*.txt")))
    root.after(1, root.destroy)
    root.mainloop()
    return file


class WindAutorization:
    def __init__(self,programm_name, email_from, password, domen, port ):
        L_porgramm = windll.user32.GetSystemMetrics(0)
        H_programm = windll.user32.GetSystemMetrics(1)
        sixteen =(int((L_porgramm * H_programm) / 129600))
        self.PROGRAMM_NAME = programm_name
        self.EMAIL_FROM = email_from
        self.PASSWORD = password
        self.DOMEN = domen
        self.PORT = port
        ## цвета
        self.color_back = '#0000ff'
        self.color_text = '#ffffff'
        self.color_button = '#42aaff'
        self.color_text_button = '#ffffff'
        ## шрифтni
        self.font = "arial"
        ## само окно
        self.root = Tk()
        self.root.title("Авторизация")
        self.root.bind("<Return>", self.generatePasswordandsendit)
        self.root.protocol("WM_DELETE_WINDOW", self.ok)
        self.root.resizable(False, False)
        self.root.geometry(f"{int(L_porgramm * 0.25)}x{int(H_programm * 0.15)}")
        self.root.configure(bg=self.color_back)
        self.root.focus_force()
        self.exit = Button(self.root, bg=self.color_button, fg=self.color_text_button, text="Выйти", font=f"{self.font} {sixteen}", command=sys.exit, activebackground='yellow', activeforeground='#FF8C00')
        self.exit.place(x=int(L_porgramm * H_programm / 5604.324), y=int(L_porgramm * H_programm / 21827.3684))
        self.next = Button(self.root, bg=self.color_button, fg=self.color_text_button, text="Войти", font=f"{self.font} {sixteen}", command=self.generatePasswordandsendit, activebackground='yellow', activeforeground='#FF8C00')
        self.next.place(x=int(L_porgramm * H_programm / 5604.324), y=int(L_porgramm * H_programm / 82944))
        self.adress = StringVar()
        self.pas = StringVar()
        self.email = Entry(self.root, bg=self.color_button, fg=self.color_text, font=f"{self.font} {sixteen}", textvariable=self.adress)
        self.email.place(x=int(L_porgramm * H_programm / 31901.5384), y=int(L_porgramm * H_programm / 25920))
        self.email.focus_set()
        self.label = Label(self.root, bg=self.color_back, fg=self.color_text, font=f'{self.font} {sixteen}', text='Введите адрес электронной почты')
        self.label.place(x=int(L_porgramm * H_programm / 207360), y=int(L_porgramm * H_programm / 103680))
        self.root.mainloop()

    def password(self, *args):
        L_porgramm = windll.user32.GetSystemMetrics(0)
        H_programm = windll.user32.GetSystemMetrics(1)
        self.label["text"] = "Введите пароль"
        self.exit["text"] = "Назад"
        self.pas = StringVar()
        self.next["command"] = self.check_pasword
        self.root.bind("<Return>", self.check_pasword)
        self.exit["command"] = self.back
        self.email["textvariable"] = self.pas
        self.info0 = Label(self.root, bg=self.color_back, fg=self.color_text, font=f"{self.font} {int(L_porgramm * H_programm / 172800)}", text=f'   Пароль отправлен на адрес:')
        self.info1 = Label(self.root, bg=self.color_back, fg=self.color_text,
                           font=f"{self.font} {int(L_porgramm * H_programm / 172800)}",
                           text=f'   {self.adress.get()}')
        self.info1.pack(side=BOTTOM, anchor=SW)
        self.info0.pack(side=BOTTOM, anchor=SW)

    def back(self, *args):
        self.root.bind("<Return>", self.generatePasswordandsendit)
        self.exit["text"] = "Выйти"
        self.exit["command"] = sys.exit
        self.label["text"] = "Введите адрес электронной почты"
        self.next["command"] = self.generatePasswordandsendit
        self.adress = StringVar()
        self.email["textvariable"] = self.adress
        try:
            self.info0.destroy()
            self.info1.destroy()
        except Exception:
            pass

    def generatePasswordandsendit(self, *args):
        if self.adress.get() == '':
            messagebox.showinfo("Авторизация", "Введите адрес электронной почты.")
            return
        lenth = sample(range(6, 12), 1)[0]
        letters_up = [list(string.ascii_uppercase)]
        letters_down = [list(string.ascii_lowercase)]
        numbers = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']]
        total_list = [list(string.ascii_lowercase)] + [list(string.ascii_uppercase)] + numbers
        count = 0
        final_list = []
        work_min = [0, 1, 2]
        work_max = [0, 1, 2]
        for i in range(lenth):
            count += 1
            if count <= 3:
                group_of_symbols = sample(work_min, 1)[0]
                work_min.remove(group_of_symbols)
                final_list.append(sample(total_list[group_of_symbols], 1)[0])
            else:
                group_of_symbols = sample(work_max, 1)[0]
                final_list.append(sample(total_list[group_of_symbols], 1)[0])
        random.shuffle(final_list)
        final_list.reverse()
        self.passwor = final_list
        message = MIMEMultipart()
        message["Subject"] = "Пароль"
        message["From"] = self.EMAIL_FROM
        body = f'''Пароль для программы {self.PROGRAMM_NAME}: {''.join(self.passwor)}'''
        message.attach(MIMEText(body, 'plain'))
        try:
            server = smtplib.SMTP_SSL(self.DOMEN, self.PORT)
            server.login(self.EMAIL_FROM, self.PASSWORD)
        except Exception as e:
            #SEND_ERR.action(460,  str(e.args), "SEND_MAIL")
            messagebox.showerror("Авторизация", "Проверьте подключение к интернету.")
            self.back()
            return
        try:
            server.sendmail(self.EMAIL_FROM, f"{self.adress.get()}", message.as_string())
            server.quit()
            self.password()
        except Exception:
            try:
                socket.gethostbyaddr("www.yandex.ru")
            except Exception:
                messagebox.showerror("Авторизация", "Проверьте подключение к интернету.")
                self.back()
                return
            messagebox.showerror("Авторизация", "Пароль не может быть отправлен на указанный адрес." + '\n' + "Введите корректный адрес.")
            self.back()
            return


    def check_pasword(self, *args):
        if ''.join(self.passwor) == self.pas.get():
            self.root.destroy()
            self.ok()
        elif self.pas.get() == '':
            messagebox.showinfo("Авторизация", "Введите пароль.")
        else:
            messagebox.showerror("Авторизация", "Указан неверный пароль.")
            self.back()
            return


    def ok(self, *args):
        pass


#a = WindAutorization("Ввод текста", "shifrovalshchik@list.ru", "Zxoiet123", "smtp.mail.ru", 465)

class Savedatas:
    def __init__(self, file, *colors):
        colors = colors[0]
        self.L_porgramm = windll.user32.GetSystemMetrics(0)
        self.H_programm = windll.user32.GetSystemMetrics(1)
        self.start_posittion = os.getcwd()
        root = Tk()
        root.withdraw()
        ## проверка указанных данных
        if not os.path.isfile(file):
            messagebox.showerror("Запуск прогаммы", f"Файл с расположением {file} не найден.")
            sys.exit()
        v = colors['v']
        if not v.isdigit():
            messagebox.showerror("Запуск прогаммы",
                                 f"Введено некорректное значение частоты отправки копий.")
            sys.exit()
        root.after(1, root.destroy)
        root.mainloop()
        self.file = str(file)
        self.v = int(v)
        try:
            self.window_color = colors['window_color']
        except KeyError:
            self.window_color = "blue"
        try:
            self.button_color = colors['button_color']
        except KeyError:
            self.button_color = "#42aaff"
        try:
            self.active_button_color = colors['active_button_color']
        except KeyError:
            self.active_button_color = "yellow"
        try:
            self.active_button_color_text = colors['active_button_color_text']
        except KeyError:
            self.active_button_color_text = "orange"
        try:
            self.main_text_color = colors['main_text_color']
        except KeyError:
            self.main_text_color = "white"
        try:
            self.button_text_color = colors['button_text_color']
        except KeyError:
            self.button_text_color = "while"
        try:
            self.font = colors["font"]
        except KeyError:
            self.font = "Arial"
        try:
            self.sing = colors['sing']
        except KeyError:
            self.sing = ""
        try:
            self.copies = colors["copies"]
            if self.copies == 'True':
                self.copies = True
            else:
                self.copies = False
        except Exception:
            self.copies = False
        try:
            self.period = int(colors['period'])
        except KeyError:
            self.period = 10
        except TypeError:
            self.period = 10
        a = open("Fastfile.txt", "r")
        self.b = a.read()
        a.close(

        )
        self.create_window()

    def create_window(self):
        self.root = Tk()
        self.root.focus()
        self.root.configure(bg=self.window_color)
        self.root.geometry(f"{int(self.L_porgramm * 0.4)}x{int(self.H_programm * 0.5)}")
        self.root.title("Ввод текста")
        sx, sy = Scrollbar(self.root, orient=HORIZONTAL), Scrollbar(self.root)
        sx.pack(side=BOTTOM, fill=X)
        sy.pack(side=RIGHT, fill=Y)
        self.text = Text(self.root, width=int(int(self.L_porgramm * 0.4) * 2.5), height=int(self.H_programm * 0.5), bg=self.window_color, fg=self.main_text_color,
                          font=f'{self.font} {int(self.H_programm * self.L_porgramm / 138240)}', yscrollcommand=sy.set, xscrollcommand=sx.set, wrap=NONE)
        self.btn1 = Button(text="Сохранить", background=self.button_color, foreground=self.button_text_color,
                      padx="15", pady="4", font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}", activebackground=self.active_button_color, activeforeground=self.active_button_color_text, command=self.save)
        if not self.sing:
            self.btn2 = Button(text="Добавить подпись", background=self.button_color, foreground=self.button_text_color,
                          padx="15", pady="1", font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                          activebackground=self.active_button_color, activeforeground=self.active_button_color_text,
                          command=self.add_sing)
        else:
            self.btn2 = Button(text="Редактировать подпись", background=self.button_color, foreground=self.button_text_color,
                               padx="15", pady="1",
                               font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                               activebackground=self.active_button_color,
                               activeforeground=self.active_button_color_text,
                               command=self.add_sing)
        self.btn4 = Button(text="Настройки", background=self.button_color, foreground=self.button_text_color,
                           padx="15", pady="1", font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                           activebackground=self.active_button_color, activeforeground=self.active_button_color_text, command=self.settings)
        self.btn4.pack(side=BOTTOM, fill=X)
        self.btn2.pack(side=BOTTOM, fill=X)
        self.btn1.pack(side=BOTTOM, fill=X)
        self.text.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.delete_window)
        sy.config(command=self.text.yview)
        sx.config(command=self.text.xview)
        self.text.focus()
        self.root.mainloop()

    def change_sing(self, *args):
        if '==========' in self.text1_stringvar.get():
            messagebox.showerror("Добавление подписи", '''"==========" - недопустимый символ. Пожалуйста, уберите его.''')
            return
        if not self.text1_stringvar.get():
            answer = messagebox.askyesno(title="Добавление подписи", message="Подпись не была введена." + '\n' + "Вы действительно хотите удалить текущую подпись?")
            if answer:
                messagebox.showinfo("Добавление подписи", "Подпись успешно удалена.")
                self.btn2["text"] = "Добавить подпись"
                self.sing = ''
        else:
            self.sing = self.text1_stringvar.get()
            messagebox.showinfo("Добавление подписи", "Подпись успешно сохранена.")
            self.btn2["text"] = "Редактировать подпись"
        self.delete_help_window()
        return

    def save(self):
        save_data = self.text.get(1.0, END).rstrip('\n')
        if save_data:
            if self.copies:
                if os.path.isfile(os.path.basename(self.file)):
                    a = open(os.path.basename(self.file), "a", encoding="utf8")
                    try:
                        a.write(u'' + save_data + '\n' * 2 + self.sing + '\n' * 3)
                        messagebox.showinfo("Ввод текста", "Текст успешно сохранён.")
                        a.close()
                        self.text.delete('1.0', END)

                    except Exception as e:
                        messagebox.showerror("Ввод текста", str(e))

                else:
                    shutil.copyfile(f"{self.file}", f"{os.path.basename(self.file)}")
                    a = open(os.path.basename(self.file), "a", encoding='utf8')
                    try:
                        a.write(u'' + save_data + '\n' * 2 + self.sing + '\n' * 3)
                        messagebox.showinfo("Ввод текста", "Текст успешно сохранён.")
                        a.close()
                        self.text.delete('1.0', END)

                    except Exception as e:
                        messagebox.showerror("Ввод текста", str(e))

            else:
                a = open(self.file, "a", encoding='utf8')
                try:
                    a.write(u'' + save_data + '\n' * 2 + self.sing + '\n' * 3)
                    messagebox.showinfo("Ввод текста", "Текст успешно сохранён.")
                    a.close()
                    self.text.delete('1.0', END)

                except Exception as e:
                    messagebox.showerror("Ввод текста", str(e))

            if self.period:
                if not os.path.isfile(f"HOW_MANY_SEND{os.path.basename(self.file)}"):
                    a = open(f"HOW_MANY_SEND{os.path.basename(self.file)}", "w")
                    a.close()
                    a = open(f"HOW_MANY_SEND{os.path.basename(self.file)}", "r")
                    send = 0
                else:
                    a = open(f"HOW_MANY_SEND{os.path.basename(self.file)}", "r")
                    send = int(a.read())
                a.close()
                a = open(f"HOW_MANY_SEND{os.path.basename(self.file)}", "w")
                a.close()
                a = open(f"HOW_MANY_SEND{os.path.basename(self.file)}", "a")
                send += 1
                a.write(str(send))
                a.close()
                if self.period:
                    if send % self.period == 0:
                        self.email()
        else:
            messagebox.showerror("Ввод текста", "Введите текст.")
        return

    def add_sing(self):
        self.root1 = Tk()
        self.root1.configure(bg=self.window_color)
        self.root.wm_attributes('-alpha', 0.3)
        if not self.sing:
            self.root1.title("Добавление подписи")
        else:
            self.root1.title("Редактирование подписи")
        self.root.protocol("WM_DELETE_WINDOW", self.delete_windows)
        self.root1.protocol("WM_DELETE_WINDOW", self.delete_help_window)
        #self.root1.geometry(f"{int(self.L_porgramm * 0.2)}x{int(self.H_programm * 0.25)}")
        #self.root.attributes("-fullscreen", False)
        self.root1.bind("<Return>", self.change_sing)
        self.text['state'] = 'disabled'
        self.btn1['state'] = 'disabled'
        self.btn2['state'] = 'disabled'
        self.btn4['state'] = 'disabled'
        self.btn3 = Button(self.root1, text="Сохранить", background=self.button_color, foreground=self.button_text_color,
                           padx="15", pady="1", font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                           activebackground=self.active_button_color, activeforeground=self.active_button_color_text, command=self.change_sing)
        self.btn3.pack(side=BOTTOM, fill=X)
        self.root.resizable(False, False)
        self.root1.resizable(True, False)
        sx= Scrollbar(self.root1, orient=HORIZONTAL)
        sx.pack(side=BOTTOM, fill=X)
        self.text1_stringvar = StringVar(self.root1)
        self.text1_stringvar.set(self.sing)
        self.text1 = Entry(self.root1, bg=self.window_color, fg=self.main_text_color, font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}", textvariable=self.text1_stringvar, xscrollcommand=sx.set)
        self.text1.pack(side=BOTTOM, fill=X)
        self.root1.focus_set()
        self.text1.focus_force()
        sx.config(command=self.text1.xview)
        self.root1.mainloop()

    def delete_windows(self):
        self.root1.destroy()
        self.root.destroy()
        a = open("Settings.txt", 'w')
        a.close()
        a = open("Settings.txt", "a")
        #print(self.copies)
        try:
            a.write(f"v=========={self.v}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("v==========10" + '\n')
        try:
            a.write(f"window_color=========={self.window_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("window_color==========blue" + '\n')
        try:
            a.write(f"button_color=========={self.button_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("button_color==========yellow" + '\n')
        try:
            a.write(f"active_button_color=========={self.active_button_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("active_button_color==========orange" + '\n')
        try:
            a.write(f"active_button_color_text=========={self.active_button_color_text}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("active_button_color_text==========black" + '\n')
        try:
            a.write(f"main_text_color=========={self.main_text_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("main_text_color==========white" + '\n')
        try:
            a.write(f"button_text_color=========={self.button_text_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("button_text_color==========blue" + '\n')
        try:
            a.write(f"font=========={self.font}" + '\n')

        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("font==========" + '\n')
        try:
            a.write(f"sing=========={self.sing}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("sing==========" + '\n')
        try:
            a.write(f"copies=========={self.copies}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("copies==========False" + '\n')
        try:
            a.write(f"period=========={self.period}")
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("period==========10")
        a.close()
        a = open("Fastfile.txt", "w")
        a.close()
        a = open("Fastfile.txt", "a")
        a.write(self.b)
        a.close()
        a = open("Backslash.txt", "w")
        a.close()
        a = open("Backslash.txt", "a")
        a.write("\\")
        a.close()

    def delete_window(self):
        self.root.destroy()
        a = open("Settings.txt", 'w')
        a.close()
        a = open("Settings.txt", 'a')
        try:
            a.write(f"v=========={self.v}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("v==========10" + '\n')
        try:
            a.write(f"window_color=========={self.window_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("window_color==========blue" + '\n')
        try:
            a.write(f"button_color=========={self.button_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("button_color==========yellow" + '\n')
        try:
            a.write(f"active_button_color=========={self.active_button_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("active_button_color==========orange" + '\n')
        try:
            a.write(f"active_button_color_text=========={self.active_button_color_text}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("active_button_color_text==========black" + '\n')
        try:
            a.write(f"main_text_color=========={self.main_text_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("main_text_color==========white" + '\n')
        try:
            a.write(f"button_text_color=========={self.button_text_color}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("button_text_color==========blue" + '\n')
        try:
            a.write(f"font=========={self.font}" + '\n')

        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("font==========" + '\n')
        try:
            a.write(f"sing=========={self.sing}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("sing==========" + '\n')
        try:
            a.write(f"copies=========={self.copies}" + '\n')
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("copies==========False" + '\n')
        try:
            a.write(f"period=========={self.period}")
        except Exception as e:
            messagebox.showerror("Техническое окно", str(e))
            a.write("period==========10")
        a.close()
        a = open("Fastfile.txt", "w")
        a.close()
        a = open("Fastfile.txt", "a")
        a.write(self.b)
        a.close()
        a = open("Backslash.txt", "w")
        a.close()
        a = open("Backslash.txt", "a")
        a.write("\\")
        a.close()

    def delete_help_window(self):
        self.text['state'] = 'normal'
        self.root.wm_attributes('-alpha', 1)
        self.btn1['state'] = 'normal'
        self.btn2['state'] = 'normal'
        self.btn4['state'] = 'normal'
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.delete_window)
        self.root1.destroy()

    def save_copies(self):
        self.copies = not self.copies
        if self.copies:
            self.checkbuton["text"] = "Работать с оригиналами файлов"
            messagebox.showinfo("Настройки", "Теперь все изменения будут происходить с копиями файлов.")
        else:
            self.checkbuton["text"] = 'Сохранять копиии файлов' + '\n' + 'и работать с ними'
            messagebox.showinfo("Настройки", "Теперь все изменения будут происходить с оригиналами файлов.")

    def settings(self):
        if self.text.get(1.0, END).strip('\n'):
            answer = messagebox.askyesno("Ввод текста", "При сохранении настроек введённый текст не сохранится." + '\n' + 'Продолжить?')
            if not answer:
                return
        self.root1 = Tk()
        self.root1.configure(bg=self.window_color)
        self.root.wm_attributes('-alpha', 0.3)
        self.root1.title("Настройки")
        self.root.protocol("WM_DELETE_WINDOW", self.delete_windows)
        self.root1.protocol("WM_DELETE_WINDOW", self.delete_help_window)
        self.root1.geometry(f"{int(self.L_porgramm * 0.2)}x{int(self.H_programm * 0.75)}")
        self.root1.resizable(False, False)
        self.root.resizable(False, False)
        self.text['state'] = 'disabled'
        self.btn1['state'] = 'disabled'
        self.btn2['state'] = 'disabled'
        self.btn4['state'] = 'disabled'
        self.text_wind_colors = {"Белый": "white", "Красный": "red", "Жёлтый": "yellow", "Чёрный": "black",
                       "Оранжевый": "orange", "Зелёный": "green", "Синий": "blue", "Голубой": '#42aaff'}
        self.colors_reverse = {"white": "Белый", "red": "Красный", "yellow": "Жёлтый", "black": "Чёрный",
                               "orange": "Оранжевый", "green": "Зелёный", "blue": "Синий", '#42aaff': "Голубой"}
        #self.list_of_colors = [i for i in self.text_wind_colors]
        color_back = Label(self.root1, text='Цвет окон:', bg=self.window_color, fg=self.main_text_color,
                           font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}')
        color_back.pack(anchor=NW)
        self.what_color_back = StringVar(self.root1)
        self.what_color_back.set(self.colors_reverse[self.window_color])
        self.new_wind_color = OptionMenu(self.root1,self.what_color_back, "Белый", "Красный",  "Оранжевый","Жёлтый", "Зелёный", "Голубой", "Синий", "Чёрный")
        self.new_wind_color.config(bg=self.button_color, fg=self.button_text_color, font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                 activebackground=self.active_button_color, activeforeground=self.active_button_color_text)
        self.new_wind_color["menu"].config(bg=self.button_color, fg=self.button_text_color, font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                         activebackground=self.active_button_color, activeforeground=self.active_button_color_text)
        self.new_wind_color.pack(anchor=NE)
        color_text = Label(self.root1, text='Цвет текста окон:', bg=self.window_color, fg=self.main_text_color,
                           font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}')
        color_text.pack(anchor=NW)
        self.what_color_text = StringVar(self.root1)
        self.what_color_text.set(self.colors_reverse[self.main_text_color])
        self.new_text_color = OptionMenu(self.root1, self.what_color_text, "Белый", "Красный", "Оранжевый", "Жёлтый",
                                         "Зелёный", "Голубой", "Синий", "Чёрный")
        self.new_text_color.config(bg=self.button_color, fg=self.button_text_color,
                                   font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                   activebackground=self.active_button_color,
                                   activeforeground=self.active_button_color_text)
        self.new_text_color["menu"].config(bg=self.button_color, fg=self.button_text_color,
                                           font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                           activebackground=self.active_button_color,
                                           activeforeground=self.active_button_color_text)
        self.new_text_color.pack(anchor=NE)
        color_button = Label(self.root1, text='Цвет кнопок:', bg=self.window_color, fg=self.main_text_color,
                           font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}')
        color_button.pack(anchor=NW)
        self.what_color_button = StringVar(self.root1)
        self.what_color_button.set(self.colors_reverse[self.button_color])
        self.new_button_color = OptionMenu(self.root1, self.what_color_button, "Белый", "Красный", "Оранжевый", "Жёлтый",
                                         "Зелёный", "Голубой", "Синий", "Чёрный")
        self.new_button_color.config(bg=self.button_color, fg=self.button_text_color,
                                   font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                   activebackground=self.active_button_color,
                                   activeforeground=self.active_button_color_text)
        self.new_button_color["menu"].config(bg=self.button_color, fg=self.button_text_color,
                                           font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                           activebackground=self.active_button_color,
                                           activeforeground=self.active_button_color_text)
        self.new_button_color.pack(anchor=NE)
        color_button_text = Label(self.root1, text='Цвет текста кнопок:', bg=self.window_color, fg=self.main_text_color,
                             font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}')
        color_button_text.pack(anchor=NW)
        self.what_color_button_text = StringVar(self.root1)
        self.what_color_button_text.set(self.colors_reverse[self.button_text_color])
        self.new_button_text_color = OptionMenu(self.root1, self.what_color_button_text, "Белый", "Красный", "Оранжевый",
                                           "Жёлтый",
                                           "Зелёный", "Голубой", "Синий", "Чёрный")
        self.new_button_text_color.config(bg=self.button_color, fg=self.button_text_color,
                                     font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                     activebackground=self.active_button_color,
                                     activeforeground=self.active_button_color_text)
        self.new_button_text_color["menu"].config(bg=self.button_color, fg=self.button_text_color,
                                             font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                             activebackground=self.active_button_color,
                                             activeforeground=self.active_button_color_text)
        self.new_button_text_color.pack(anchor=NE)
        color_button_active = Label(self.root1, text='Цвет активной кнопки:', bg=self.window_color, fg=self.main_text_color,
                                  font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}')
        color_button_active.pack(anchor=NW)
        self.what_color_active_button = StringVar(self.root1)
        self.what_color_active_button.set(self.colors_reverse[self.active_button_color])
        self.new_button_color = OptionMenu(self.root1, self.what_color_active_button, "Белый", "Красный", "Оранжевый",
                                           "Жёлтый",
                                           "Зелёный", "Голубой", "Синий", "Чёрный")
        self.new_button_color.config(bg=self.button_color, fg=self.button_text_color,
                                     font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                     activebackground=self.active_button_color,
                                     activeforeground=self.active_button_color_text)
        self.new_button_color["menu"].config(bg=self.button_color, fg=self.button_text_color,
                                             font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                             activebackground=self.active_button_color,
                                             activeforeground=self.active_button_color_text)
        self.new_button_color.pack(anchor=NE)
        color_button_active_text = Label(self.root1, text='Цвет текста активной кнопки:', bg=self.window_color,
                                    fg=self.main_text_color,
                                    font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}')
        color_button_active_text.pack(anchor=NW)
        self.what_color_active_button_text = StringVar(self.root1)
        self.what_color_active_button_text.set(self.colors_reverse[self.active_button_color_text])
        self.new_button_color = OptionMenu(self.root1, self.what_color_active_button_text, "Белый", "Красный", "Оранжевый",
                                           "Жёлтый",
                                           "Зелёный", "Голубой", "Синий", "Чёрный")
        self.new_button_color.config(bg=self.button_color, fg=self.button_text_color,
                                     font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                     activebackground=self.active_button_color,
                                     activeforeground=self.active_button_color_text)
        self.new_button_color["menu"].config(bg=self.button_color, fg=self.button_text_color,
                                             font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                             activebackground=self.active_button_color,
                                             activeforeground=self.active_button_color_text)
        self.new_button_color.pack(anchor=NE)
        font_type = Label(self.root1, text='Тип шрифта:', bg=self.window_color,
                                         fg=self.main_text_color,
                                         font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}')
        font_type.pack(anchor=NW)
        self.font_type = StringVar(self.root1)
        self.font_type.set(self.font)
        self.new_font_type = OptionMenu(self.root1, self.font_type, 'Algerian', 'Arial', 'Broadway', 'Calibri', 'Century', 'Sylfaen', 'Symbol', 'Times')
        self.new_font_type.config(bg=self.button_color, fg=self.button_text_color,
                                     font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                     activebackground=self.active_button_color,
                                     activeforeground=self.active_button_color_text)
        self.new_font_type["menu"].config(bg=self.button_color, fg=self.button_text_color,
                                             font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                             activebackground=self.active_button_color,
                                             activeforeground=self.active_button_color_text)
        self.new_font_type.pack(anchor=NE)
        period = Label(self.root1, text='Частота отправки копий:', bg=self.window_color,
                                         fg=self.main_text_color,
                                         font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}')
        self.help_period = {'После каждой записи':1, 'Раз в 2 записи':2, 'Раз в 3 записи':3, 'Раз в 5 записей':5, 'Раз в 10 записей':10, 'Раз в 15 записей':15, 'Раз в 20 записей':20,'Никогда':0}
        self.reverse_help_period = {1:'После каждой записи', 2:'Раз в 2 записи',3:'Раз в 3 записи', 5:'Раз в 5 записей', 10:'Раз в 10 записей', 15:'Раз в 15 записей', 20:'Раз в 20 записей', 0:"Никогда"}
        period.pack(anchor=NW)
        self.period_1 = StringVar(self.root1)
        self.period_1.set(self.reverse_help_period[self.period])
        self.period_time = OptionMenu(self.root1, self.period_1, 'После каждой записи', 'Раз в 2 записи', 'Раз в 3 записи', 'Раз в 5 записей',
                                        'Раз в 10 записей', 'Раз в 15 записей', 'Раз в 20 записей', 'Никогда')
        self.period_time.config(bg=self.button_color, fg=self.button_text_color,
                                  font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                  activebackground=self.active_button_color,
                                  activeforeground=self.active_button_color_text)
        self.period_time["menu"].config(bg=self.button_color, fg=self.button_text_color,
                                          font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                          activebackground=self.active_button_color,
                                          activeforeground=self.active_button_color_text)
        self.period_time.pack(anchor=NE)
        fast_file = Label(self.root1, text='Файл, открывающийся при запуске:', bg=self.window_color,
                                         fg=self.main_text_color,
                                         font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}')
        fast_file.pack(anchor=NW)
        #a.close()
        if self.b:
            self.fast_file = Button(self.root1, text="Изменить", background=self.button_color,
                               foreground=self.button_text_color,
                               padx="15", pady="1",
                               font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                               activebackground=self.active_button_color,
                               activeforeground=self.active_button_color_text, command=self.fastfile)
            self.fast_file.pack(anchor=NE)
            help = Label(self.root1, text='', bg=self.window_color, font = int(self.H_programm * self.L_porgramm / 1036800))
            help.pack(anchor=NE)
            self.delete_fastfile = Button(self.root1, text="Удалить", background=self.button_color,
                               foreground=self.button_text_color,
                               padx="15", pady="1",
                               font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                               activebackground=self.active_button_color,
                               activeforeground=self.active_button_color_text, command=self.delete_fast)
            self.delete_fastfile.pack(anchor=NE)
        else:
            self.fast_file = Button(self.root1, text="Добавить", background=self.button_color,
                                    foreground=self.button_text_color,
                                    padx="15", pady="1",
                                    font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                                    activebackground=self.active_button_color,
                                    activeforeground=self.active_button_color_text, command=self.fastfile
                                    )
            self.fast_file.pack(anchor=NE)
            help = Label(self.root1, text='', bg=self.window_color,
                         font=int(self.H_programm * self.L_porgramm / 1036800))
            help.pack(anchor=NE)
            self.delete_fastfile = Button(self.root1, text="Удалить", background=self.button_color,
                                          foreground=self.button_text_color,
                                          padx="15", pady="1",
                                          font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                                          activebackground=self.active_button_color,
                                          activeforeground=self.active_button_color_text, command=self.delete_fast)
            self.delete_fastfile.pack(anchor=NE)

        if self.copies:
            self.checkbuton = Button(self.root1, bg=self.button_color, fg=self.button_text_color,
                        text='Работать с оригиналами файлов', font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}', activebackground=self.active_button_color,
                        activeforeground=self.active_button_color_text, command=self.save_copies)

        else:
            self.checkbuton = Button(self.root1, bg=self.button_color, fg=self.button_text_color,
                                          text='Сохранять копиии файлов' + '\n' + 'и работать с ними',
                                          font=f'{self.font} {int(self.L_porgramm * self.H_programm / 138240)}',
                                          activebackground=self.active_button_color,
                                          activeforeground=self.active_button_color_text, command=self.save_copies)
        self.show = Button(self.root1, text="Файл сохранения текущего сеанса", background=self.button_color,
                           foreground=self.button_text_color,
                           padx="15", pady="1",
                           font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                           activebackground=self.active_button_color,
                           activeforeground=self.active_button_color_text, command=self.fileworking)
        self.btn5 = Button(self.root1, text="Сохранить настройки", background=self.button_color, foreground=self.button_text_color,
                               padx="15", pady="1",
                               font=f"{self.font} {int(self.H_programm * self.L_porgramm / 138240)}",
                               activebackground=self.active_button_color,
                               activeforeground=self.active_button_color_text, command=self.check_change_settings)
        self.btn5.pack(side=BOTTOM, fill=X)
        self.show.pack(side=BOTTOM, fill=X)
        self.checkbuton.pack(side=BOTTOM)
        self.root1.mainloop()

    def check_change_settings(self):
        '''
        self.what_color_back
        self.what_color_text
        self.what_color_button
        self.what_color_button_text
        self.what_color_active_button
        self.what_color_active_button_text
        '''
        if self.what_color_back.get() == self.what_color_text.get():
            messagebox.showerror("Настройки", "Цвет окна и цвет текста окна не могут быть одинаковыми.")
            return
        if self.what_color_button.get() == self.what_color_button_text.get():
            messagebox.showerror("Настройки", "Цвет кнопки и цвет текста кнопки не могут быть одинаковыми.")
            return
        if self.what_color_active_button == self.what_color_active_button_text:
            messagebox.showerror("Настройки", "Цвет активной кнопки и цвет текста активной кнопки не могут быть одинаковыми.")

        self.font = self.font_type.get()
        self.window_color = self.text_wind_colors[self.what_color_back.get()]
        self.main_text_color = self.text_wind_colors[self.what_color_text.get()]
        self.button_color = self.text_wind_colors[self.what_color_button.get()]
        self.button_text_color = self.text_wind_colors[self.what_color_button_text.get()]
        self.active_button_color = self.text_wind_colors[self.what_color_active_button.get()]
        self.active_button_color_text = self.text_wind_colors[self.what_color_active_button_text.get()]
        self.period = self.help_period[self.period_1.get()]
        #messagebox.showinfo("Настройки", "Настройки успешно сохранены.")
        self.delete_help_window()
        self.root.destroy()
        self.create_window()

    def fileworking(self):
        if not self.copies:
            answer = messagebox.askyesno("Настройки", f"Текущий файл сохранения: {self.file}" + '\n' + "Изменить?")
        else:
            a = open("Backslash.txt", "r")
            b = a.read()[0]
            a.close()
            answer = messagebox.askyesno("Настройки", "Текущий файл сохранения:" + os.getcwd() + b + os.path.basename(self.file) + '\n' + "Изменить?")
        if answer:
            file = filedialog.askopenfilename(title="Выбор файла для записи",
                                              filetypes=(("txt files", "*.txt"), ("txt files", "*.txt")))
            while not os.path.isfile(file):
                messagebox.showerror("Настройки",
                                     "Файл для записи не был выбран." + '\n' + 'Для отмены операции закройте это сообщение и в появившемся окне нажмите No.' + '\n' + "Иначе нажмите Yes и выберите файл для записи.")
                answer = messagebox.askyesno(title="Настройки", message="Выбрать файл для записи?")
                if not answer:
                    return
                file = filedialog.askopenfilename(title="Выбор файла для записи",
                                                  filetypes=(("txt files", "*.txt"), ("txt files", "*.txt")))
            self.file = file
            messagebox.showinfo("Настройки", "Файл записи текущего сеанса успешно изменён.")
            return
        else:
            return

    def fastfile(self):
        if self.b:
            answer = messagebox.askyesno("Настройки", f"Файл, открывающийся при запуске: {self.b}" + '\n' + "Изменить?")
        else:
            answer = True
        if answer:
            file = filedialog.askopenfilename(title="Выбор файла, открывающегося при запуске",
                                              filetypes=(("txt files", "*.txt"), ("txt files", "*.txt")))
            while not os.path.isfile(file):
                messagebox.showerror("Настройки",
                                     "Файл, открывающийся при запуске, не выбран." + '\n' + 'Для отмены операции закройте это сообщение и в появившемся окне нажмите No.' + '\n' + "Иначе нажмите Yes и выберите файл, открывающийся при запуске.")
                answer = messagebox.askyesno(title="Настройки", message="Выбрать файл, открывающийся при запуске?")
                if not answer:
                    return
                file = filedialog.askopenfilename(title="Выбор файла, открывающегося при запуске",
                                                  filetypes=(("txt files", "*.txt"), ("txt files", "*.txt")))
            if self.b:
                messagebox.showinfo("Настройки", "Файл, открывающийся при запуске, успешно изменён.")
            else:
                messagebox.showinfo("Настройки", "Файл, открывающийся при запуске, успешно добавлен.")
            self.b = file
            self.fast_file['text'] = "Изменить"
        return

    def delete_fast(self):
        if not self.b:
            messagebox.showinfo("Настройки", f"Файл, открывающийся при запуске, не назначен и не может быть удалён.")
        else:
            self.b = ''
            messagebox.showerror("Настройки", f"Файл, открывающийся при запуске, успешно удалён.")
            self.fast_file['text'] = "Добавить"
        return

    def email(self):
        messagebox.showinfo("Ввод текста", "Отправка резервной копии." + '\n' + 'Пожалуйста, подождите...')
        message = MIMEMultipart()
        message["Subject"] = "Автоотправка резервной копии"
        message["From"] = "shifrovalshchik@list.ru"
        if self.copies:
            filepath = os.path.basename(self.file)
        else:
            filepath = self.file
        if True:  # Если файл существует
            ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
            if ctype is None or encoding is not None:  # Если тип файла не определяется
                ctype = 'application/octet-stream'  # Будем использовать общий тип
            maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
            encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
            file.add_header('Content-Disposition', 'attachment', filename="Цитаты.txt")  # Добавляем заголовки
            message.attach(file)
        message.attach(MIMEText('', 'plain'))
        try:
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            server.login("shifrovalshchik@list.ru", "Zxoiet123")
            server.sendmail("shifrovalshchik@list.ru", adress, message.as_string())
            messagebox.showinfo("Ввод текста", "Отправка резервной копии успешно завершена.")
            server.quit()
        except Exception as e:
            messagebox.showerror("Ввод текста", f"Отправка копии не выполнена. Причина: {str(e.args)}")
        return

a = WindAutorization("Ввод текста", "shifrovalshchik@list.ru", "Zxoiet123", "smtp.mail.ru", 465)
adress = a.adress.get()
try:
    os.mkdir(adress)
except Exception:
    pass
os.chdir(f"./{adress}")
if not os.path.isfile("Settings.txt"):
    a = open("Settings.txt", "w")
    a.close()
    a = open("Settings.txt", 'a')
    a.write("v==========10" + '\n')
    a.write("window_color==========blue" + '\n')
    a.write("button_color==========#42aaff" + '\n')
    a.write("active_button_color==========yellow" + '\n')
    a.write("active_button_color_text==========orange" + '\n')
    a.write("main_text_color==========white" + '\n')
    a.write("button_text_color==========white" + '\n')
    a.write("font==========Arial" + '\n')
    a.write("sing==========" + '\n')
    a.write("copies==========False" + '\n')
    a.write("period==========10")
    a.close()
if not os.path.isfile("Backslash.txt"):
    a = open("Backslash.txt", "w")
    a.close()
    a = open("Backslash.txt", "a")
    a.write("\\")
    a.close()
if not os.path.isfile("Fastfile.txt"):
    a = open("Fastfile.txt", "w")
    b = False
    a.close()
else:
    a = open("Fastfile.txt", "r")
    b = a.read()
    a.close()
datas = {}
a = open("Settings.txt", "r")
settings = a.read()
a.close()
settings = settings.split('\n')
for i in settings:
    try:
        datas[i.split("==========")[0]] = i.split("==========")[1]
    except IndexError:
        pass
if not b:
    file = get_file()
else:
    file = b

s = Savedatas(file, datas)