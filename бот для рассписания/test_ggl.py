import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta, timezone
from Calendar_config import Config
from pytz import timezone as tz
from algorytms import Task
import logging
from datetime import time
logging.basicConfig(
    filename='debug.log',  # Имя файла, куда будут записываться логи
    filemode='w',  # Перезаписывать файл каждый раз (используйте 'a' для добавления)
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
moscow_tz = tz("Europe/Moscow")


def filter_events_by_date_and_time(events, date, start_time, end_time):
    """
    Фильтрует события, оставляя только те, которые начинаются и заканчиваются в определенный день и временной интервал.

    :param events: Список всех событий.
    :param date: Объект datetime.date, представляющий день, который нужно проверить.
    :param start_time: Объект datetime.time, представляющий время начала интервала.
    :param end_time: Объект datetime.time, представляющий время окончания интервала.
    :return: Список отфильтрованных событий"""
    # Преобразуем дату и время начала и конца в объекты datetime
    start_datetime = datetime(year=date.year, month=date.month, day=date.day, hour=start_time.hour, minute=start_time.minute)
    end_datetime = datetime(year=date.year, month=date.month, day=date.day, hour=end_time.hour, minute=end_time.minute)

    start_datetime = moscow_tz.localize(start_datetime)
    end_datetime = moscow_tz.localize(end_datetime)
    filtered_events = []
    for event in events:
        event_start_str = event.get('start', {}).get('dateTime')
        event_end_str = event.get('end', {}).get('dateTime')
        # Пропускаем события без времени начала или окончания
        if not event_start_str or not event_end_str:
            continue

        # Преобразуем время начала и окончания событий в объекты datetime
        event_start = datetime.fromisoformat(
            event_start_str.replace("Z", "+00:00"))
        event_end = datetime.fromisoformat(
            event_end_str.replace("Z", "+00:00"))
        if event_start < end_datetime and event_end > start_datetime:
            filtered_events.append(event)
    return filtered_events

def make_timezone_aware(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class GoogleCalendar:
    def __init__(self, credentials_file="token.json"):
        while True:
            try:
                if os.path.isfile(credentials_file):
                    self.creds = Credentials.from_authorized_user_file(credentials_file, ["https://www.googleapis.com/auth/calendar"])
                    self.service = build("calendar", "v3", credentials=self.creds)
                    self.calendar_list = self.service.calendarList().list().execute()['items']
                    self.names = [i['summary'] for i in self.calendar_list]
                    break
                else:
                    SCOPES = ['https://www.googleapis.com/auth/calendar']
                    print(os.path.abspath('.'))
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'client_secret_770813874973-e970c07ecucgqd6kietipl4bsj1jlrut.apps.googleusercontent.com.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                    # Сохраняем токен для будущего использования
                    with open(credentials_file, 'w') as token:
                        token.write(creds.to_json())
                    self.creds = Credentials.from_authorized_user_file(
                        credentials_file,
                        ["https://www.googleapis.com/auth/calendar"])
                    self.service = build("calendar", "v3",
                                         credentials=self.creds)
                    self.calendar_list = \
                    self.service.calendarList().list().execute()['items']
                    self.names = [i['summary'] for i in self.calendar_list]




            except Exception as e:
                print(e.args)
                print('Ошибка создания календаря. Повтор')

        c = Config()
        for name in c.required_calendars:
            if name not in self.names:
                self.create_calendar(name)
                self.names.append(name)
        self.calendar_list = self.service.calendarList().list().execute()['items']




    def create_calendar(self, calendar_name):
        try:
            calendar = {
                "summary": calendar_name,
                "timeZone": "Europe/Moscow"
            }
            created_calendar = self.service.calendars().insert(body=calendar).execute()
            print(f"Календарь '{calendar_name}' создан с ID: {created_calendar['id']}")
            return created_calendar["id"]
        except HttpError as error:
            print(f"Ошибка при создании календаря: {error}")

    def add_event(self, calendar_id, event_name, start_time, end_time, description=""):
        if True:
            event = {
                "summary": event_name,
                "description": description,
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": "Europe/Moscow"
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "Europe/Moscow"
                }
            }
            try:
                created_event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
                print(f"Событие '{event_name}' добавлено в календарь с ID: {calendar_id}")
                return created_event["id"]
            except HttpError as error:
                print(f"Ошибка при добавлении события: {error}")


    def update_event(self, calendar_id, event_id, new_end_time,
                     new_start_time=None, new_description=""):
        """Обновление существующего события в указанный календарь."""
        # Получаем текущее событие
        event = self.service.events().get(calendarId=calendar_id,
                                          eventId=event_id).execute()

        # Обновляем время начала, если новое значение задано
        if new_start_time is not None:
            event['start']['dateTime'] = new_start_time.isoformat()

        # Обновляем время окончания
        event['end']['dateTime'] = new_end_time.isoformat()

        # Обновляем описание, если новое значение задано
        if new_description:
            event['summary'] = new_description
        # Сохраняем обновленное событие
        updated_event = self.service.events().update(calendarId=calendar_id,
                                                     eventId=event_id,
                                                     body=event).execute()
        print(
            f"Событие обновлено: {updated_event.get('htmlLink')}")  # Выводим ссылку на событие

    def delete_event(self, calendar_id, event_id):
        """Удаление события из указанного календаря."""
        self.service.events().delete(calendarId=calendar_id,
                                     eventId=event_id).execute()
        print(f"Событие с ID {event_id} удалено из календаря.")

    def get_tasks(self, calendar_id):
        """Получение событий, представляющих начало новых задач из указанного календаря."""
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=datetime(2022, 1, 1).isoformat() + 'Z',
            singleEvents=True
        ).execute()
        events = events_result.get('items', [])

        tasks = []
        end_id = self.get_calendar_id('Дедлайны')
        import datetime as dt
        deadline_result = self.service.events().list(
            calendarId=end_id,
            timeMin=dt.datetime(2024, 1, 1).isoformat() + 'Z',
            singleEvents=True
        ).execute()
        dead_events = deadline_result.get('items', [])
        for i in range(len(events)):
            event = events[i]

            if 'Начало новой задачи' in event.get('summary',
                                                  ''):  # Проверяем, является ли событие началом новой задачи
                start_time = event['start'].get('dateTime',
                                                event['start'].get('date',
                                                                   None))

                if start_time:
                    name = event['summary'].replace('Начало новой задачи: ',
                                                    '')

                    end_time = ''
                    for j in range(len(dead_events)):
                        de = dead_events[j]
                        if 'Дедлайн' in de.get('summary',
                                                              ''):  # Проверяем, является ли событие началом новой задачи
                            de_name = de['summary'].replace(
                                'Дедлайн: ',
                                '')
                            if de_name == name:
                                end_time = de['start'].get('dateTime',
                                                de['start'].get('date',
                                                                   None))


                    if end_time:
                        # Преобразуем оба времени в объекты datetime
                        start_time = datetime.fromisoformat(start_time)
                        end_time = datetime.fromisoformat(end_time)

                        # Приводим оба времени к "offset-naive"
                        start_time = start_time.replace(tzinfo=None)
                        end_time = end_time.replace(tzinfo=None)

                        tasks.append(Task(
                            name=name,  # Извлекаем название задачи
                            # Здесь можно установить начальное значение, если необходимо
                            start_date=start_time,
                            # Можно использовать более подходящее значение
                            deadline=end_time,  # Дедлайн
                            start_event_id=event['id'],
                            end_event_id=de['id']
                            # Сохраняем event_id для обновления или удаления в будущем
                        ))

        return tasks
    # Метод для получения событий на определенный день
    def get_events_by_date(self, calendar_id, date):

        # Запрашиваем события из Google Calendar API
        events_result = self.service.events().list(
            calendarId=calendar_id,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        # Извлекаем список

        events = events_result.get('items', [])

        events = filter_events_by_date_and_time(events, date, time(hour=0, minute=0, second=0, microsecond=0), time(hour=23, minute=59, second=59, microsecond=59))
        return events
    # Метод для проверки, свободен ли временной интервал
    def is_time_available(self, date, start_time, end_time):
        # Получаем все события на этот день
        r = True
        ids = [self.get_calendar_id(name) for name in self.names]
        for calendar_id in range(len(ids)):
            n = calendar_id

            calendar_id = ids[calendar_id]
            events = self.get_events_by_date(calendar_id=calendar_id, date=date)
            r *= not (filter_events_by_date_and_time(events, date, start_time, end_time))
            if not r:
                return False
        return True

    def get_events(self, calendar_id, start_date, end_date):
        # Преобразуем даты в формат ISO 8601
        start_date_iso = start_date.isoformat() + 'Z'  # добавляем Z для указания на UTC
        end_date_iso = end_date.isoformat() + 'Z'  # добавляем Z для указания на UTC

        # Запрос на получение событий
        cd = calendar_id
        try:
            events_result = self.service.events().list(
                calendarId=calendar_id['id'],
                timeMin=start_date_iso,
                timeMax=end_date_iso,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
        except Exception as e:
            events_result = self.service.events().list(
                calendarId=self.get_calendar_id(calendar_id),
                timeMin=start_date_iso,
                timeMax=end_date_iso,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

        events = events_result.get('items', [])
        return events

    def get_calendar_id(self, calendar_name):
        """Получаем идентификатор календаря по его названию."""
        return next((calendar['id'] for calendar in self.calendar_list if calendar['summary'] == calendar_name), None)


if __name__ == "__main__":
    calendar = GoogleCalendar("token.json")

    calendar_id = calendar.get_calendar_id('Дедлайны')
    start_time_1 = moscow_tz.localize(datetime(2024, 12, 1, 1, 0))
    end_time_1 = start_time_1 + timedelta(minutes=30)

    print(calendar.is_time_available(start_time_1, time(19, 0), time(20, 0)))