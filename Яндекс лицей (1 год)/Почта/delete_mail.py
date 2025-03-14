import imaplib, time, pymorphy2, colorama
from colorama import Fore, Back
colorama.init()
morph = pymorphy2.MorphAnalyzer()
comment = morph.parse('секунда')[0]
def get_datas():
    print(Fore.YELLOW  + '\n' + "Проверка...")
    mail = imaplib.IMAP4_SSL("imap.mail.ru")
    mail.login("shifrovalshchik@list.ru", "Zxoiet123")
    mail.list()
    mail.select("inbox")
    result, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split()
    for i in id_list:
        mail.store(i, "+FLAGS", "\\Deleted")
        mail.expunge()
    print(Fore.GREEN + "Проверка успешно завершена." + '\n')
    time.sleep(1)
count = input(Fore.BLUE + "Введите интервал между проверками... ")
while not count.isdigit():
    count = input(Fore.BLUE + "Введите интервал между проверками... ")
count = int(count)
abc = count
while True:
    get_datas()
    count = abc
    while count:
        count -= 1
        print(Fore.BLUE + f"Следующая поверка входящих через {count + 1} {comment.make_agree_with_number(count + 1).word}.")
        time.sleep(1)