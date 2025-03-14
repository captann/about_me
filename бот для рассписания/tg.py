import threading

import random

import requests
import telebot
import json
from telebot import types
from tg_config import TOKEN, AUTHORIZED_USER_ID
from ans_config import Config_texts
from ans_config import Config_time as CT
import os
import datetime
from task_initialization import main as setup_timetable
threats = []
chat_id = AUTHORIZED_USER_ID
bot = telebot.TeleBot(TOKEN)

def check_internet_connection():
    try:
        # Отправляем запрос к Google с ограничением по времени в 3 секунды
        response = requests.get("http://www.google.com", timeout=3)
        # Если запрос прошёл успешно, возвращаем True
        return response.status_code == 200
    except requests.ConnectionError:
        # Если не удалось подключиться, возвращаем False
        return False


def save_energy():
    import os
    from datetime import timedelta, datetime
    print('energe_saving')
    # Определение текущего времени и времени выключения через 2 минуты
    current_time = datetime.now()
    shutdown_time = current_time + timedelta(minutes=2)
    shutdown_time_str = shutdown_time.strftime("%H:%M")

    # Рассчитываем время пробуждения на 5:59
    wake_time = datetime.combine(current_time.date(),
                                 datetime.strptime("05:59", "%H:%M").time())

    # Проверка: если время пробуждения уже прошло, добавляем еще один день
    if wake_time <= current_time:
        wake_time += timedelta(days=1)

    # Переводим время пробуждения в Unix-формат
    wake_time_epoch = int(wake_time.timestamp())
    print(f"Время пробуждения: {wake_time} (Unix: {wake_time_epoch})")

    # Команда для настройки пробуждения с использованием rtcwake
    wake_time_command = f"sudo rtcwake -m off -t {wake_time_epoch}"
    os.system(wake_time_command)
    print(f"Команда rtcwake установлена для пробуждения в 5:59 утра")

    # Команда для выключения через 2 минуты
    shutdown_command = f"sudo shutdown -h {shutdown_time_str}"
    os.system(shutdown_command)
    print(f"Компьютер выключится в {shutdown_time_str}")


def create_json(day_number=1, gi=0, bp=0, zakachka=0, sa=0, dc=0, prev=None,
                nir=0):
    if day_number == 1 or prev == None:
        # Задаем путь к папке для данных
        data_folder = "1/main/data"

        # Создаем папки, если они не существуют
        os.makedirs(data_folder, exist_ok=True)

        # Задаем данные
        data = {
            'date': [day_number],
            'gi_meds_taken': [gi],
            'bp_meds_taken': [bp],
            'hand_exercise_weight': [zakachka],
            'nir_course_progress': [nir],
            'digital_course_progress': [dc],
            'sa_course_progress': [sa]

        }

        # Задаем весовые коэффициенты для различных показателей
        weights = {
            'gi_meds_taken': 0.025,
            'bp_meds_taken': 0.025,
            'hand_exercise_weight': 0.15,
            'digital_course_progress': 0.25,
            'sa_course_progress': 0.25,
            'nir_course_progress': 0.3
        }

        # Функция для записи данных в JSON файлы
        def save_to_json(data_dict, folder):
            for key, values in data_dict.items():
                file_path = os.path.join(folder, f"{key}.json")
                with open(file_path, 'w') as f:
                    json.dump(values, f, indent=4)
                print(f"Сохранено: {file_path}")

        # Записываем данные в JSON файлы
        save_to_json(data, data_folder)

        # Сохраняем весовые коэффициенты в отдельный JSON файл
        weights_file = os.path.join(data_folder, "weights.json")
        with open(weights_file, 'w') as f:
            json.dump(weights, f, indent=4)
        print(f"Сохранено: {weights_file}")

        total_tasks_file = os.path.join(data_folder, "total_tasks.json")
        with open(total_tasks_file, 'w') as f:
            json.dump({
                "total_tasks_sa": 100,
                "total_tasks_dc": 100,
                "total_tasks_nir": 100
            }
                , f, indent=4)
        print(f"Сохранено: {total_tasks_file}")

        tasks_completed_file = os.path.join(data_folder,
                                            "tasks_completed.json")
        with open(tasks_completed_file, 'w') as f:
            json.dump({
                "tasks_completed_sa": [sa],
                "tasks_completed_dc": [dc],
                "tasks_completed_nir": [nir]
            }
                , f, indent=4)
        print(f"Сохранено: {tasks_completed_file}")

        print("Папки и файлы с исходными данными и весами успешно созданы.")
    else:
        # Задаем путь к папке для данных
        data_folder = str(day_number) + "/main/data"

        # Создаем папки, если они не существуют

        os.makedirs(data_folder, exist_ok=True)

        with open(prev + '/' + 'date.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        data.append(day_number)

        date_js = os.path.join(data_folder,
                               "date.json")

        with open(date_js, 'w', encoding='utf-8') as f:
            json.dump(data, f)

        with open(prev + '/' + 'gi_meds_taken.json', 'r',
                  encoding='utf-8') as f:
            gi_meds_taken = json.load(f)
        gi_meds_taken.append(gi)

        gi_js = os.path.join(data_folder,
                             "gi_meds_taken.json")

        with open(gi_js, 'w', encoding='utf-8') as f:
            json.dump(gi_meds_taken, f)

        with open(prev + '/' + 'bp_meds_taken.json', 'r',
                  encoding='utf-8') as f:
            bp_meds_taken = json.load(f)
        bp_meds_taken.append(bp)

        bp_js = os.path.join(data_folder,
                             "bp_meds_taken.json")

        with open(bp_js, 'w', encoding='utf-8') as f:
            json.dump(bp_meds_taken, f)

        with open(prev + '/' + 'hand_exercise_weight.json', 'r',
                  encoding='utf-8') as f:
            zax = json.load(f)

        zax.append(zakachka)

        zax_js = os.path.join(data_folder,
                              "hand_exercise_weight.json")

        with open(zax_js, 'w', encoding='utf-8') as f:
            json.dump(zax, f)

        tasks_completed_file = os.path.join(data_folder,
                                            "tasks_completed.json")
        with open(tasks_completed_file, 'w') as f:
            json.dump({
                "tasks_completed_sa": [sa],
                "tasks_completed_dc": [dc],
                "tasks_completed_nir": [nir]
            }, f)

        # Задаем весовые коэффициенты для различных показателей

        # Задаем весовые коэффициенты для различных показателей
        weights = {
            'gi_meds_taken': 0.025,
            'bp_meds_taken': 0.025,
            'hand_exercise_weight': 0.15,
            'digital_course_progress': 0.25,
            'sa_course_progress': 0.25,
            'nir_course_progress': 0.3
        }

        # Сохраняем весовые коэффициенты в отдельный JSON файл
        weights_file = os.path.join(data_folder, "weights.json")
        with open(weights_file, 'w') as f:
            json.dump(weights, f, indent=4)
        print(f"Сохранено: {weights_file}")

        total_tasks_file = os.path.join(data_folder, "total_tasks.json")
        with open(total_tasks_file, 'w') as f:
            json.dump({
                "total_tasks_sa": 100,
                "total_tasks_dc": 100,
                "total_tasks_nir": 100
            }
                , f, indent=4)
        print(f"Сохранено: {total_tasks_file}")
        with open(prev + '/' + 'tasks_completed.json', 'r',
                  encoding='utf-8') as f:
            tcf = json.load(f)
        tcf['tasks_completed_sa'].append(sa)
        tcf['tasks_completed_dc'].append(dc)
        tcf['tasks_completed_nir'].append(nir)

        tasks_completed_file = os.path.join(data_folder,
                                            "tasks_completed.json")
        with open(tasks_completed_file, 'w') as f:
            json.dump(tcf
                      , f, indent=4)
        print(f"Сохранено: {tasks_completed_file}")

        print("Папки и файлы с исходными данными и весами успешно созданы.")


class Dialog:
    def __init__(self):
        self.stop_flag = False
        from datetime import time, datetime
        self.boot_time = time(hour=00, minute=15)
        self.statistics = {}
        self.can_send = True
        self.is_statistic_running = False
        self.Dijits = [str(i) for i in range(0, 16)]
        self.Letters = ['Да', 'Нет']
        self.motivations = Config_texts.texts['motiv']
        self.actions = []
        self.setup_timing()
        self.daily_tasks = {i: [] for i in Config_texts.q_keys}
        if CT().t != 'FIGHT':
            n = datetime.now()
            h = n.hour
            m = n.minute
            k = 5
            if n.minute >= (60 - k):
                m = (m + k) % 60
                h = (h + 1) % 24
            else:
                m = m + k
            self.boot_time = time(hour=h, minute=m)
            print(f'BOOT TIME: {self.boot_time.hour}:{self.boot_time.minute}')
        print(os.path.isfile('save_actions.json'), os.path.isfile(
                'save_daily_tasks.json'))
        if os.path.isfile('save_actions.json') and os.path.isfile(
                'save_daily_tasks.json'):
            print('Trying to load data form file')
            try:
                with open('save_actions.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)
                    if len(r) < len(self.actions):
                        self.actions = r
                        with open('save_daily_tasks.json', 'r',
                                  encoding='utf-8') as f:

                            self.daily_tasks = json.load(f)

                        print('datas are loadad.')

                os.remove('save_actions.json')
                os.remove('save_daily_tasks.json')
            except Exception as e:
                raise e
        self.others = []

        self.LtD = {'Да': 1, 'Нет': 0}
        self.thread = threading.Thread(target=self.check_status)
        self.thread.daemon = True
        threats.append(self.thread)
        self.thread.start()

    def stop(self):
        # Устанавливаем флаг остановки потока
        self.stop_flag = True

        # Ждем завершения потока в течение 1 секунды
        if self.thread.is_alive():
            self.thread.join(timeout=1)  # Попытка завершить поток за 1 секунду
            if self.thread.is_alive():
                print("Не удалось завершить поток за 1 секунду.")
            else:
                print("Поток остановлен.")

        # Запись данных в JSON файлы

        with open('save_actions.json', 'w', encoding='utf-8') as f:
            json.dump(self.actions, f, ensure_ascii=False)
        with open('save_daily_tasks.json', 'w', encoding='utf-8') as f:
            json.dump(self.daily_tasks, f, ensure_ascii=False)
        print("Данные сохранены")

    def check_status(self):
        import time

        while not self.stop_flag:
            self.make_func()
            from datetime import datetime
            now = datetime.now()

            if all([self.daily_tasks[key] for key in self.daily_tasks]) or (self.boot_time.hour == now.hour and self.boot_time.minute == now.minute):
                if not self.is_statistic_running:
                    self.make_statistic()
                    self.setup_timing()
                    save_energy()
                    print('shutting down')

            time.sleep(1)

    def make_statistic(self):

        self.is_statistic_running = True
        self.daily_tasks['gi_q'] = int(
            all([self.LtD[i] for i in self.daily_tasks['gi_q']]))
        self.daily_tasks['bp_q'] = int(
            all([self.LtD[i] for i in self.daily_tasks['bp_q']]))
        self.daily_tasks['sa_q'] = sum(
            [int(i) for i in self.daily_tasks['sa_q']])
        self.daily_tasks['za_q'] = sum(
            [int(i) for i in self.daily_tasks['za_q']])
        self.daily_tasks['nir_q'] = sum(
            [int(i) for i in self.daily_tasks['nir_q']])
        self.daily_tasks['dc_q'] = sum(
            [int(i) for i in self.daily_tasks['dc_q']])

        import os
        directories = next(os.walk('.'))[1]
        numbers = []
        day_number = 1
        prev = None
        for i in directories:
            try:
                numbers.append(int(i))
            except Exception:
                pass
        if numbers:
            day_number = max(numbers) + 1
            prev = str(max(numbers)) + '/main/data'
        create_json(day_number=day_number,
                    gi=self.daily_tasks['gi_q'],
                    bp=self.daily_tasks['bp_q'],
                    zakachka=self.daily_tasks['za_q'],
                    sa=self.daily_tasks['sa_q'],
                    nir=self.daily_tasks['nir_q'],
                    dc=self.daily_tasks['dc_q'],
                    prev=prev
                    )
        from test_datas import write_file
        me = write_file(decay_coefficient=0.9,
                        weights_file=str(
                            day_number) + "/main/data/weights.json",
                        data_folder=str(day_number) + "/main/data",
                        output_dir=str(day_number) + "/main/graphics",
                        graphics_folder=str(day_number) + "/main/graphics",
                        pdf_folder=str(day_number) + "/main/pdf",
                        gi=True
                        )
        other = write_file(decay_coefficient=0.9,
                           weights_file=str(
                               day_number) + "/main/data/weights.json",
                           data_folder=str(day_number) + "/main/data",
                           output_dir=str(day_number) + "/main/graphics",
                           graphics_folder=str(day_number) + "/main/graphics",
                           pdf_folder=str(day_number) + "/main/pdf",
                           gi=False
                           )
        with open(me, 'rb') as file:
            bot.send_document(chat_id, file,
                              caption=f'Вот график твоей эффективности за {str(datetime.date.today())} ✅')
        for person in self.others:
            with open(other, 'rb') as file:
                bot.send_document(person, file,
                                  caption=f'График эффективности за {str(datetime.date.today())} ')
        current_time = datetime.datetime.now()
        delta = 1
        if current_time.hour == 0:
            delta = 0
        setup_timetable(delta)
        self.daily_tasks = {i: [] for i in Config_texts.q_keys}
        self.actions = []
        self.can_send = True

        self.is_statistic_running = False

    def send_questions(self, text, type, time, key):
        keys = {'L': self.Letters, 'D': self.Dijits}
        keys = keys[type]
        self.add_action([time, text, key, keys])

    def send_motivation(self, time):
        self.add_action([time, random.choice(self.motivations), []])

    def send_reminding(self, time, text):
        self.add_action([time, text, []])

    def add_action(self, args):
        self.actions.append(args)
        self.actions.sort(
            key=lambda x: datetime.datetime.strptime(x[0], "%H:%M"))

    def make_func(self):
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        if self.actions:
            nearest = [int(i) for i in self.actions[0][0].split(':')]
            if self.can_send:
                # naarest - время запуска
                # если текуще время больше времени запуска, h > nearest[0]
                # или часы равны времени запуска и время запуска в минутах меньше текущего
                if self.actions[0][-1]:
                    markup = telebot.types.ReplyKeyboardMarkup(
                        resize_keyboard=True)
                    markup.add(*self.actions[0][-1])

                    if h > nearest[0]:
                        self.can_send = False
                        bot.send_message(chat_id=chat_id,
                                         text=self.actions[0][1],
                                         reply_markup=markup)
                        bot.register_next_step_handler_by_chat_id(chat_id,
                                                                  lambda
                                                                      msg: self.handle_message(
                                                                      msg=msg,
                                                                      key=
                                                                      self.actions[
                                                                          0][
                                                                          -1],
                                                                      who=
                                                                      self.actions[
                                                                          0][
                                                                          -2]))
                    elif h == nearest[0] and m >= nearest[1]:
                        self.can_send = False
                        bot.send_message(chat_id=chat_id,
                                         text=self.actions[0][1],
                                         reply_markup=markup)
                        bot.register_next_step_handler_by_chat_id(chat_id,
                                                                  lambda
                                                                      msg: self.handle_message(
                                                                      msg=msg,
                                                                      key=
                                                                      self.actions[
                                                                          0][
                                                                          -1],
                                                                      who=
                                                                      self.actions[
                                                                          0][
                                                                          -2]))
                else:
                    markup = types.ReplyKeyboardRemove()
                    if h > nearest[0]:
                        self.can_send = False
                        bot.send_message(chat_id=chat_id,
                                         text=self.actions[0][1],
                                         reply_markup=markup)
                        self.remove_action()

                    elif h == nearest[0] and m >= nearest[1]:
                        self.can_send = False
                        bot.send_message(chat_id=chat_id,
                                         text=self.actions[0][1],
                                         reply_markup=markup)
                        self.remove_action()

    def handle_message(self, msg, key, who=()):
        if not self.stop_flag:
            if msg.text.lower() not in [str(i).lower() for i in key]:
                bot.register_next_step_handler_by_chat_id(chat_id, lambda
                    msg: self.handle_message(msg, key))
                self.can_send = False

            elif not key:

                if who:
                    self.daily_tasks[who].append(msg.text)
                self.remove_action()

            else:
                if who:
                    self.daily_tasks[who].append(msg.text)
                bot.send_message(chat_id=chat_id, text="Данные записаны, спасибо!",
                                 reply_markup=types.ReplyKeyboardRemove())
                self.remove_action()
        

    def remove_action(self):
        self.can_send = True
        if self.actions:
            self.actions = self.actions[1:]

    def setup_timing(self):
        # отправка мотивации
        if self.actions:
            markup = types.ReplyKeyboardRemove()
            bot.send_message(chat_id, text="Время ответа прошло.",
                             reply_markup=markup)
            for key in self.daily_tasks:
                if not self.daily_tasks[key]:
                    if key in ['bp_q', 'gi_q']:
                        self.daily_tasks[key].append('Нет')
                    else:
                        self.daily_tasks[key].append('0')
            self.make_statistic()

        Config_time = CT()
        print(CT())
        motivation_phrases_time_hours = Config_time.motivation_phrases_time_hours
        motivation_phrases_time_minutes = Config_time.motivation_phrases_time_minutes
        for i in range(len(motivation_phrases_time_minutes)):
            self.send_motivation(
                time=f'{motivation_phrases_time_hours[i]}:{motivation_phrases_time_minutes[i]}')
        # напоминания о таблетках для ЖКТ
        gi_table = Config_time.gi_table
        for i in range(len(gi_table)):
            self.send_reminding(time=f'{gi_table[i][0]}:{gi_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['gi_rem']))
            # Вопросы о таблетках для ЖКТ
        gi_table = Config_time.gi_table2
        for i in range(len(gi_table)):
            self.send_questions(time=f'{gi_table[i][0]}:{gi_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['gi_q']), type="L",
                                key='gi_q')

        # напоминания о таблетках от давления
        bp_table = Config_time.bp_table
        for i in range(len(bp_table)):
            self.send_reminding(time=f'{bp_table[i][0]}:{bp_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['bp_rem']))
        # Вопросы о таблетках от давления
        bp_table = Config_time.bp_table2
        for i in range(len(bp_table)):
            self.send_questions(time=f'{bp_table[i][0]}:{bp_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['bp_q']), type="L",
                                key='bp_q')

        # напоминания о закачке кистей
        za_table = Config_time.za_table
        for i in range(len(za_table)):
            self.send_reminding(time=f'{za_table[i][0]}:{za_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['za_rem']))
        # Вопросы о закачке кистей
        za_table = Config_time.za_table2
        for i in range(len(za_table)):
            self.send_questions(time=f'{za_table[i][0]}:{za_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['za_q']), type="D",
                                key='za_q')

        # напоминания о  системной аналитике
        sa_table = Config_time.sa_table
        for i in range(len(sa_table)):
            self.send_reminding(time=f'{sa_table[i][0]}:{sa_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['sa_rem']))
        # Вопросы о СА
        sa_table = Config_time.sa_table2
        for i in range(len(sa_table)):
            self.send_questions(time=f'{sa_table[i][0]}:{sa_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['sa_q']), type="D",
                                key='sa_q')

        # напоминания о ЦК
        dc_table = Config_time.dc_table
        for i in range(len(dc_table)):
            self.send_reminding(time=f'{dc_table[i][0]}:{dc_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['dc_rem']))
        # Вопросы о ЦК
        dc_table = Config_time.dc_table2
        for i in range(len(dc_table)):
            self.send_questions(time=f'{dc_table[i][0]}:{dc_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['dc_q']), type="D",
                                key='dc_q')
        # напоминания о НИР
        nir_table = Config_time.nir_table
        for i in range(len(nir_table)):
            self.send_reminding(time=f'{nir_table[i][0]}:{nir_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['nir_rem']))
        # Вопросы о НИР
        nir_table = Config_time.nir_table2
        for i in range(len(nir_table)):
            self.send_questions(time=f'{nir_table[i][0]}:{nir_table[i][1]}',
                                text=random.choice(
                                    Config_texts.texts['nir_q']), type="D",
                                key='nir_q')


if __name__ == '__main__':
    was_reboot = False
    was_initalised = False
    n = datetime.datetime.now()
    while True:
        try:
            d = None
            if check_internet_connection():
                if was_reboot:
                    markup = types.ReplyKeyboardRemove()

                    bot.send_message(chat_id,
                                     "Бот пришлось перезапустить. Скопируй свои предыдущие ответы и ответь также. Извини за кривые руки програмиста, которому лень убивать ещё одни выходные на приложение, которым никто кроме него никогда пользоваться не будет.",
                                     reply_markup=markup)
                for thread in threats:
                    thread.join()
                d = Dialog()

                was_initalised = True
                t = datetime.time(hour=n.hour, minute=n.minute, second=n.second)
                if not was_reboot:
                    print(
                        f'Started at {n.hour}:{n.minute}:{n.second} on {n.day}.{n.month}.{n.year}. MODE: {CT().t}')
                else:
                    print(f'Rebooted at {n.hour}:{n.minute}:{n.second} on {n.day}.{n.month}.{n.year}. MODE: {CT().t}')

                # Увеличиваем таймауты для более стабильной работы
                telebot.apihelper.CONNECT_TIMEOUT = 30
                telebot.apihelper.READ_TIMEOUT = 30
                bot.polling(none_stop=True, timeout=60)
            else:
                print("Нет подключения к интернету")
                print("Ожидание подключения...")
                time.sleep(30)  # Ждем 30 секунд перед следующей попыткой
                continue  # Возвращаемся к началу цикла для новой проверки

        except AttributeError as e:
            print(f"Критическая ошибка атрибута: {str(e)}")
            raise e
            exit()
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print(f"Ошибка сети: {str(e)}")
            if was_initalised and d is not None:
                d.stop()
                del d
                d = None
            was_reboot = True
            print('Ошибка сети, будет повторное подключение')
            print('Ожидание перед подключением...')
            time.sleep(30)  # Увеличенное время ожидания для сетевых ошибок
        except Exception as e:
            print(f"Неожиданная ошибка: {str(e)}")
            if was_initalised and d is not None:
                d.stop()
                del d
                d = None
            was_reboot = True
            print('Ошибка, будет повторное подключение')
            print('Подключение...')
            time.sleep(5)