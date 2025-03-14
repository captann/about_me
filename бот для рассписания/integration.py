from datetime import datetime
from algorytms import Task  # Импортируем класс Task
from test_ggl import GoogleCalendar, \
    moscow_tz  # Импортируем класс GoogleCalendar

from datetime import timedelta


class Event:
    def __init__(self, start_time, end_time, task):
        self.name = task.name
        self.start_time = start_time
        self.end_time = end_time
        self.task = task
        self.status = False

    def __str__(self):
        from prettytable import PrettyTable
        table = PrettyTable()
        table.field_names = ['Параметр', 'Значение']
        table.add_row(['Имя', self.name])
        table.add_row(['Начало', self.start_time])
        table.add_row(['Конец', self.end_time])
        return str(table)


class Generate_tt:
    def __init__(self, tasks, slots):
        self.tasks = tasks
        self.free_slots = slots
        self.MIN_SLOT_DURATION = timedelta(minutes=30)

        # Сортируем задачи по приоритету (от большего к меньшему)
        self.tasks.sort(key=lambda x: x.priority, reverse=True)

        self.tasks_for_today = []
        self.extra = []
        self.MAX_ONE_TASK_TIME = timedelta(
            hours=3.5)  # Максимальное время для одной задачи
        self.time_today = timedelta()  # Общее время, выделенное на задачи
        good = []
        extra = []
        # Формируем список задач для выполнения сегодня
        for task in self.tasks:

            if (datetime.now() - (task.last_completed_date)).days >= 1:
                good.append(task)
            else:
                extra.append(task)
        good.sort(key=lambda x: (datetime.now() - x.last_completed_date).days, reverse=True)
        extra.sort(key=lambda x: (datetime.now() - x.last_completed_date).days, reverse=True)
        names = []
        for i in good:
            if i.name not in names:
                names.append(i.name)
                self.tasks_for_today.append(i)
        names = []

        for i in extra:
            if i.name not in names:
                names.append(i.name)
                self.extra.append(i)
        for elem in self.extra:
            self.tasks_for_today.append(elem)
        self.schedule_tasks()

    def schedule_tasks(self):
        self.schedule = []

        for task in self.tasks_for_today:
            # Рассчитываем необходимое время для задачи с учетом скорости выполнения
            required_speed = task.required_speed if task.required_speed > 0 else 1  # Устанавливаем единицу, если скорость нулевая
            actual_speed = task.actual_speed if task.actual_speed > 0 else 1  # Устанавливаем единицу, если скорость нулевая

            min_speed = min(required_speed,
                            actual_speed)  # Используем минимальную скорость

            # Рассчитываем время, необходимое для выполнения задач с учетом скорости
            tasks_per_minute = min_speed / (
                    24 * 60)  # Количество задач в минуту
            required_minutes = (
                                       1 / tasks_per_minute) * 60  # Переводим в минуты

            # Ограничиваем время выполнения 4 часами, если требуется больше
            task_duration = min(timedelta(minutes=required_minutes),
                                self.MAX_ONE_TASK_TIME)
            if task.name == 'Закачка кистей':
                task_duration = timedelta(minutes=30)

            # Проходим по доступным временным слотам
            new_free_slots = []  # Новый список свободных слотов
            self.free_slots = list(filter(lambda x: (x[1] - x[0]) >= self.MIN_SLOT_DURATION, self.free_slots))
            for slot_start, slot_end in self.free_slots:
                current_time = slot_start
                while current_time < slot_end and task_duration > timedelta(0):
                    # Вычисляем, сколько времени можно выделить в текущем слоте
                    available_time = min(task_duration,
                                         slot_end - current_time)
                    if True:
                        # Добавляем задачу в расписание
                        self.schedule.append(Event(
                            task=task,
                            start_time=current_time,
                            end_time=current_time + available_time
                        ))

                        # Обновляем время и сокращаем необходимое время выполнения задачи
                        current_time += available_time
                        task_duration -= available_time
                        self.time_today += available_time
                    else:
                        current_time = slot_end

                    if task_duration <= timedelta(0):
                        break

                if current_time < slot_end:
                    new_free_slots.append((current_time, slot_end))

            # Обновляем список свободных слотов
            self.free_slots = new_free_slots

    def get_schedule(self):
        return self.schedule


def get_free_time_slots(events, date):
    start_of_day = moscow_tz.localize(
        datetime(date.year, date.month, date.day, 0, 0))
    end_of_day = moscow_tz.localize(
        datetime(date.year, date.month, date.day, 23, 59, 59))

    # Формируем список всех занятых промежутков
    busy_intervals = []
    for event in events:
        start = datetime.fromisoformat(
            event['start']['dateTime'].replace('Z', '+00:00'))
        end = datetime.fromisoformat(
            event['end']['dateTime'].replace('Z', '+00:00'))

        busy_intervals.append((start, end))
    busy_intervals.sort(key=lambda x: x[0])
    # Вычисляем свободные промежутки
    free_intervals = []
    current_time = start_of_day

    for start, end in busy_intervals:
        if current_time < start:
            free_intervals.append((current_time, start))
        current_time = max(current_time, end)

    if current_time < end_of_day:
        free_intervals.append((current_time, end_of_day))

    return free_intervals


class CalendarIntegration:
    def __init__(self):
        self.tasks = []
        self.google_calendar = GoogleCalendar()  # Инициализируем класс GoogleCalendar
        self.load_tasks_from_calendar()

    def add_task(self, task):
        # Добавляем событие начала задачи в календарь
        calendar_id_start = self.get_calendar_id('Начало новой задачи')
        now = datetime.now()

        if self.google_calendar.is_time_available(date=task.start_date.date(),
                                                  start_time=task.start_date,
                                                  end_time=task.start_date + task.dlt):
            if self.google_calendar.is_time_available(
                    date=task.deadline.date(), start_time=task.deadline,
                    end_time=task.deadline + task.dlt):
                start_id = self.google_calendar.add_event(
                    calendar_id=calendar_id_start,
                    event_name=f'Начало новой задачи: {task.name}',
                    start_time=task.start_date,
                    end_time=task.start_date + task.dlt
                    # Можем использовать одно и то же время для начала
                )

                # Добавляем событие дедлайна в календарь
                calendar_id_deadline = self.get_calendar_id('Дедлайны')
                if task.deadline:  # Проверяем, задан ли дедлайн
                    end_id = self.google_calendar.add_event(
                        calendar_id=calendar_id_deadline,
                        event_name=f'Дедлайн: {task.name}',
                        start_time=task.deadline,
                        end_time=task.deadline + task.dlt
                        # Также можно настроить время окончания
                    )
                task.start_event_id = start_id
                task.end_event_id = end_id
                self.tasks.append(task)  # Добавляем задачу в список задач
                print(
                    f"Задача '{task.name}' добавлена, событие начала и дедлайн созданы.")
                return True, ""
            else:
                return False, "Дедлайн"
        else:
            return False, "Начало"

    def load_tasks_from_calendar(self):
        """Загрузка задач из календаря."""
        calendar_id = self.get_calendar_id('Начало новой задачи')
        self.tasks.extend(self.google_calendar.get_tasks(
            calendar_id))  # Получаем задачи и добавляем в список
        print(
            f"Задачи загружены из календаря: {[task.name for task in self.tasks]}")

    def update_task(self, task):
        """Обновление событий задачи (начало работы и дедлайн) в календарях."""
        # Обновление события о начале работы над задачей
        calendar_id_starts = self.get_calendar_id(
            'Начало новой задачи')
        # Предполагаем, что у нас есть календарь для начала работы

        if self.google_calendar.is_time_available(date=task.start_date.date(),
                                                  start_time=task.start_date,
                                                  end_time=task.start_date + task.dlt):
            if self.google_calendar.is_time_available(
                    date=task.deadline.date(), start_time=task.deadline,
                    end_time=task.deadline + task.dlt):

                if task.start_event_id and task.start_date:
                    self.google_calendar.update_event(
                        calendar_id=calendar_id_starts,
                        event_id=task.start_event_id,
                        new_start_time=task.start_date + task.dlt,
                        new_end_time=task.start_date + task.dlt,
                        new_description=f'Начало новой задачи: {task.name}'

                        # Можно настроить новое время окончания события
                    )
                    print(
                        f'Событие о начале работы над задачей "{task.name}" обновлено в календаре.')

                # Обновление события о дедлайне задачи
                calendar_id_deadlines = self.get_calendar_id('Дедлайны')
                if task.end_event_id and task.deadline:
                    self.google_calendar.update_event(
                        calendar_id=calendar_id_deadlines,
                        event_id=task.end_event_id,
                        new_start_time=task.deadline,
                        new_end_time=task.deadline,
                        new_description=f'Дедлайн: {task.name}'
                        # Можно настроить новое время окончания
                    )
                    print(
                        f'Дедлайн задачи "{task.name}" обновлён в календаре.')
                    return True, ""
            return False, "Дедлайн"
        else:
            return False, "Начало"

    def remove_task(self, task):
        """Удаление дедлайна задачи и мероприятия о начале работы над задачей из календаря."""
        calendar_id_deadlines = self.get_calendar_id('Дедлайны')
        calendar_id_starts = self.get_calendar_id(
            'Начало новой задачи')  # Предполагаем, что у нас есть календарь для начала работы

        # Удаляем дедлайн
        if hasattr(task, 'end_event_id'):
            self.google_calendar.delete_event(
                calendar_id=calendar_id_deadlines,
                event_id=task.end_event_id
            )
            print(f'Дедлайн задачи "{task.name}" удалён из календаря.')

        # Удаляем событие о начале работы над задачей
        if hasattr(task,
                   'start_event_id'):  # Предполагаем, что у нас есть event_id для начала работы
            self.google_calendar.delete_event(
                calendar_id=calendar_id_starts,
                event_id=task.start_event_id
            )
            print(
                f'Событие о начале работы над задачей "{task.name}" удалено из календаря.')

    def get_calendar_id(self, calendar_name):
        """Получаем идентификатор календаря по его названию."""
        return next(
            (calendar['id'] for calendar in self.google_calendar.calendar_list
             if calendar['summary'] == calendar_name), None)

    def get_event_ids(self, calendar_id, start_date, end_date):
        """
        Получаем идентификаторы первого и последнего события в календаре
        за указанный промежуток времени.
        """
        events = self.google_calendar.get_events(calendar_id, start_date,
                                                 end_date)
        start_event_id = None
        end_event_id = None

        if events:
            start_event_id = events[0]['id']  # Идентификатор первого события
            end_event_id = events[-1]['id']  # Идентификатор последнего события

        return start_event_id, end_event_id

    def get_slots(self, date):
        r = [self.google_calendar.get_events_by_date(id_c, date) for
             id_c in [i['id'] for i in self.google_calendar.calendar_list]]
        events = []
        for i in r:
            for j in i:
                events.append(j)
        time_slots = get_free_time_slots(events, date)

        return time_slots


def generate_schedule(tasks, slots):
    tt = Generate_tt(tasks, slots)

    return tt.get_schedule()





# Пример использования
if __name__ == "__main__":
    # Создаем экземпляр интеграции
    calendar_integration = CalendarIntegration()
    task2 = Task(name="Системная аналитика",
                 start_date=datetime(2024, 10, 1, hour=0),
                 deadline=datetime(2024, 12, 1, hour=8))
    task3 = Task(name="Научно-исследовательская работа",
                 start_date=datetime(2024, 7, 1, hour=1),
                 deadline=datetime(2024, 12, 1, hour=0))
    task5 = Task(name="Цифровая кафедра",
                 start_date=datetime(2024, 10, 1, hour=1),
                 deadline=datetime(2024, 12, 1, hour=1))
    task4 = Task(name="Учёба", total_tasks=100, completed_tasks=0,
                 start_date=datetime(2022, 9, 1, hour=10),
                 last_completed_date=None,
                 deadline=datetime(2024, 12, 20, hour=10), start_event_id=None,
                 end_event_id=None, dlt=timedelta(hours=1))
    import datetime as dt
    date = dt.datetime.now() + timedelta(days=1)
    slots = calendar_integration.get_slots(date)
    t = [task2, task3, task4, task5]
    for i in t:
        (calendar_integration.add_task(i))
    for i in calendar_integration.tasks:
        t.append(i)
    schedule = generate_schedule(t, slots)
    for i in schedule:
        print(i)
