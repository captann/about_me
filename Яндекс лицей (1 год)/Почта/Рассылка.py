import xlrd, sys, shutil
import pymorphy2
from docxtpl import DocxTemplate
import mimetypes                                          # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                # Импортируем энкодер
from email.mime.base import MIMEBase                      # Общий тип
from email.mime.image import MIMEImage                    # Изображения
from email.mime.audio import MIMEAudio                    # Аудио
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
morph = pymorphy2.MorphAnalyzer()
if not os.path.isdir("Приглашения"):
    os.mkdir("Приглашения")
os.chdir(f'./Приглашения')

def create_document(way, name,email):
    doc = DocxTemplate(way)
    content = {"name" : name}
    doc.render(content)
    doc.save(email + '.docx ')


def send_mail(*args):  # нужно указать либо путь к файлу с email либо сам email(1й пункт) текст сообщения(2й пункт) и путь к ПАПКЕ, где лежит файл для отправки (1го типа)
    global morph
    fileway = ''
    email_list = args[0]
    count = 0
    text = "Привет!"
    text += '\n' + "Хочу отправить тебе приглашение на выпускной."
    text += "\n" + "Не отвечай на это сообщения, я всё равно его не прочту."
    text += '\n' + "Твой АНОНИМУС"
    if True:
        for email in email_list:
            text = (text, 'plain', '1251')
            text = "Привет!"
            text += '\n' + "Хочу отправить тебе приглашение на выпускной."
            text += "\n" + "Не отвечай на это сообщения, я всё равно его не прочту."
            text += '\n' + "Твой АНОНИМУС"
            message = MIMEMultipart()
            message["Subject"] = "Приглашение"
            message["From"] = "shifrovalshchik@list.ru"
            body = text
            filepath = email + '.docx'
            filename = os.path.basename(filepath)  # Только имя файла
            if os.path.isfile(filepath):  # Если файл существует
                ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
                if ctype is None or encoding is not None:  # Если тип файла не определяется
                    ctype = 'application/octet-stream'  # Будем использовать общий тип
                maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
                if maintype == 'text':  # Если текстовый файл
                    with open(filepath) as fp:  # Открываем файл для чтения
                        file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
                        fp.close()  # После использования файл обязательно нужно закрыть
                elif maintype == 'image':  # Если изображение
                    with open(filepath, 'rb') as fp:
                        file = MIMEImage(fp.read(), _subtype=subtype)
                        fp.close()
                elif maintype == 'audio':  # Если аудио
                    with open(filepath, 'rb') as fp:
                        file = MIMEAudio(fp.read(), _subtype=subtype)
                        fp.close()
                else:  # Неизвестный тип файла
                    with open(filepath, 'rb') as fp:
                        file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                        file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                        fp.close()
                    encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
                file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
                message.attach(file)
            message.attach(MIMEText(body, 'plain'))
            try:
                server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
                server.login(message["From"], "Zxoiet123")
                server.sendmail(message["From"], email, message.as_string())
                server.quit()
                count += 1
                print(f"Отправлено {count} сообщений из {len(emails)}.")
                print(f"Сообщение успешно отправлено на адрес {email}")
            except Exception:
                print(f"Сообщение не отправлено на почту: {email}")
                print(f"Отправлено {count} сообщений из {len(emails)}.")
        os.chdir('..')
        shutil.rmtree(f'./Приглашения', ignore_errors=True, onerror=None)
        print("Работа завершена.")
way = input("Введите путь к файлу exel и название файла (без разрешения!)... ") + ".xlsx"
while not os.path.exists(way):
    way = input("Введите путь к файлу exel и название файла (без разрешения!)... ") + ".xlsx"
rb = xlrd.open_workbook(way)
sheet = rb.sheet_by_index(0)
vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
emails = []
way = input("Введите путь расположения докумена в формате .docx и его имя (без разрешения!)... ")  + ".docx"
while not os.path.exists(way):
    way = input("Введите путь расположения докумена в формате .docx и его имя (без разрешения!)... ") +  ".docx"
for datas in vals:
    create_document(way, datas[0], datas[1])
    emails.append(datas[1])
    print(f"Создано документ для : {datas[0]}")
if emails == []:
    print("Нет адресов и имён.")
    sys.exit()

send_mail(emails)