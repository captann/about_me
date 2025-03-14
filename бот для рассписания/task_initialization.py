from integration import *
from datetime import datetime

tasks = []
calendar_integration = CalendarIntegration()


def generate_events_and_tasks(date):
    global tasks, calendar_integration
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

    task6 = Task(name="Закачка кистей", total_tasks=100, completed_tasks=0,
                 start_date=datetime(2023, 4, 10, hour=10),
                 last_completed_date=None,
                 deadline=datetime(2025, 4, 10, hour=10), start_event_id=None,
                 end_event_id=None, dlt=timedelta(hours=1))

    slots = calendar_integration.get_slots(date)
    tasks = [task2, task3, task4, task5, task6]
    for i in calendar_integration.tasks:
        tasks.append(i)
    for i in tasks:
        calendar_integration.add_task(i)
    schedule = generate_schedule(tasks, slots)
    return schedule


def add_events(schedule):
    for event in schedule:
        calendar_id = calendar_integration.get_calendar_id(event.name)
        calendar_integration.google_calendar.add_event(calendar_id=calendar_id,
                                                       event_name=event.name,
                                                       start_time=event.start_time,
                                                       end_time=event.end_time)


def main(*args):
    import json
    d = 0
    if args:
        d = args[0]
    date = datetime.now() + timedelta(days=d)
    print('g date setup', date)
    result = generate_events_and_tasks(date)
    add_events(result)
    translate_to_other_keys = {
        "Системная аналитика": [],
        "Научно-исследовательская работа": [],
        "Цифровая кафедра": [],
        "Закачка кистей": [],

    }
    for i in result:
        if i.name in translate_to_other_keys:
            translate_to_other_keys[i.name].append([
                [i.start_time.hour, i.start_time.minute],
                [i.end_time.hour, i.end_time.minute]
            ])
    with open('schedule.json', 'w', encoding='utf-8') as f:
        json.dump(translate_to_other_keys, f, ensure_ascii=False, indent=4)
    return True

if __name__ == "__main__":
    main()
