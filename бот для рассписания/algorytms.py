from datetime import datetime, timedelta
from prettytable import PrettyTable
import os, json

def create_json(day_number=1, gi=0, bp=0, zakachka=0, sa=0, dc=0, prev=None, nir=0):
    if day_number == 1 or prev == None:
        # Задаем путь к папке для данных
        data_folder = f"{day_number}/main/data"

        # Создаем папки, если они не существуют
        os.makedirs(data_folder, exist_ok=True)

        # Задаем данные
        data = {
            'date': [day_number],
            'gi_meds_taken': [gi],
            'bp_meds_taken': [bp],
            'hand_exercise_weight': [zakachka]
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

        tasks_completed_file = os.path.join(data_folder, "tasks_completed.json")
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


        with open(prev + '/' + 'gi_meds_taken.json', 'r', encoding='utf-8') as f:
            gi_meds_taken = json.load(f)
        gi_meds_taken.append(gi)

        gi_js = os.path.join(data_folder,
                                            "gi_meds_taken.json")

        with open(gi_js, 'w', encoding='utf-8') as f:
            json.dump(gi_meds_taken, f)



        with open(prev + '/' + 'bp_meds_taken.json', 'r', encoding='utf-8') as f:
            bp_meds_taken = json.load(f)
        bp_meds_taken.append(bp)

        bp_js = os.path.join(data_folder,
                                            "bp_meds_taken.json")

        with open(bp_js, 'w', encoding='utf-8') as f:
            json.dump(bp_meds_taken, f)

        with open(prev + '/' + 'hand_exercise_weight.json', 'r', encoding='utf-8') as f:
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
        with open(prev + '/' + 'tasks_completed.json', 'r', encoding='utf-8') as f:
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

def day_number():
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
        day_number = max(numbers)
    else:
        create_json(day_number=1)
    return (os.path.abspath('.') + '/' + f'{day_number}')


class Task:
    def __init__(self, name=None, total_tasks=None, completed_tasks=None,
                 start_date=None, last_completed_date=None, deadline=None,
                 start_event_id=None, end_event_id=None,
                 dlt=timedelta(hours=1)):
        self.dlt = dlt
        self.name = name
        self.total_tasks = total_tasks
        self.completed_tasks = completed_tasks
        self.deadline = deadline
        self.start_date = start_date
        self.last_completed_date = datetime.now() - timedelta(
            days=last_completed_date) if last_completed_date else datetime.now() - timedelta(
            days=3)
        self.priority = 0.0
        self.required_speed = 0.0
        self.actual_speed = 0.0
        self.urgency = "Обычный"
        # Добавляем коэффициенты срочности
        self.urgency_coefficients = {
            "Обычный": 1.0,
            "Высокий": 10.0,
            "Просрочен": 0.5}
        self.start_event_id = start_event_id
        self.end_event_id = end_event_id

        self.calculate_priority()

    def calculate_priority(self):
        upper_coeff = 1
        import json
        with open(f'{day_number()}/main/data/weights.json', 'r') as file:
            weights = json.load(file)
        with open(f'{day_number()}/main/data/tasks_completed.json',
                  'r') as file:
            stats = json.load(file)
        with open(f'{day_number()}/main/data/total_tasks.json', 'r') as file:
            tt = json.load(file)

        if self.name == "Цифровая кафедра":
            self.completed_tasks = sum(stats["tasks_completed_dc"])
            self.total_tasks = tt['total_tasks_dc']
            weight = weights["digital_course_progress"]
            hands = stats["tasks_completed_dc"]

            ind = -1
            for i in range(len(stats["tasks_completed_dc"])):
                if stats["tasks_completed_dc"][i] != 0:
                    ind = i
            if ind != -1:
                days_ago = len(hands) - 1 - ind  # Количество дней назад
                self.last_completed_date = datetime.now() - timedelta(days=days_ago)
            else:
                self.last_completed_date = datetime.now() - timedelta(
                    days=len(hands) + 1)

        elif self.name == "Системная аналитика":
            self.completed_tasks = sum(stats["tasks_completed_sa"])
            weight = weights["sa_course_progress"]
            self.total_tasks = tt['total_tasks_sa']
            hands = stats["tasks_completed_sa"]

            ind = -1
            for i in range(len(stats["tasks_completed_sa"])):
                if stats["tasks_completed_sa"][i] != 0:
                    ind = i
            if ind != -1:
                days_ago = len(hands) - 1 - ind  # Количество дней назад
                self.last_completed_date = datetime.now() - timedelta(days=days_ago)
            else:
                self.last_completed_date = datetime.now() - timedelta(
                    days=len(hands) + 1)


        elif self.name == "Научно-исследовательская работа":
            self.completed_tasks = sum(stats["tasks_completed_nir"])
            weight = weights["nir_course_progress"]
            self.total_tasks = tt['total_tasks_nir']
            ind = -1
            hands = stats["tasks_completed_nir"]
            for i in range(len(stats["tasks_completed_nir"])):
                if stats["tasks_completed_nir"][i] != 0:
                    ind = i
            if ind != -1:
                days_ago = len(hands) - 1 - ind  # Количество дней назад
                self.last_completed_date = datetime.now() - timedelta(days=days_ago)
            else:
                self.last_completed_date = datetime.now() - timedelta(
                    days=len(hands) + 1)
        elif self.name == 'Закачка кистей':
            with open(f'{day_number()}/main/data/hand_exercise_weight.json',
                      'r') as file:
                hands = json.load(file)
            weight = weights["hand_exercise_weight"]
            ind = -1

            # Находим индекс последнего дня, когда была выполнена задача
            for i in range(len(hands)):
                if hands[i] != 0:
                    ind = i

            # Подсчитываем выполненные задачи
            self.total_tasks = 15
            self.completed_tasks = self.total_tasks - sum(hands) / len(hands)

            # Определяем дату последнего выполнения задачи
            if ind != -1:
                days_ago = len(hands) - 1 - ind  # Количество дней назад
                self.last_completed_date = datetime.now() - timedelta(days=days_ago)
            else:
                self.last_completed_date = datetime.now() - timedelta(
                    days=len(hands) + 1)
            upper_coeff = 2000

        if self.completed_tasks:
            total_completed_tasks = self.completed_tasks / self.total_tasks
            self.priority = (1 - total_completed_tasks) * weight
        else:
            self.completed_tasks = 0
            self.priority = 1
            self.total_tasks = 10 ** 6
        self.determine_urgency()
        # Используем коэффициенты срочности
        self.priority *= self.urgency_coefficients[self.urgency]

        # Фактор частоты выполнения
        days_since_last_completed = (
                datetime.now() - self.last_completed_date).days
        if days_since_last_completed > 1:  # Пример: если не выполнялась больше 3 дней
            self.priority *= 1.2  # Увеличиваем приоритет
        elif days_since_last_completed <= 1:  # Если выполнялась вчера или сегодня
            self.priority *= 0.8  # Уменьшаем приоритет
        self.calculate_speeds()

        if self.required_speed == self.actual_speed:
            speed_cf = 1
        elif self.required_speed > self.actual_speed:
            speed_cf = 1 + (
                        self.required_speed - self.actual_speed) / self.required_speed
        else:
            speed_cf = 1 - (
                        self.actual_speed - self.required_speed) / self.actual_speed

        self.priority *= speed_cf
        self.priority *= upper_coeff

    def determine_urgency(self):
        today = datetime.now()
        total_time = (self.deadline - self.start_date).days
        time_left = (self.deadline - today).days
        if self.deadline < today:
            self.urgency = "Просрочен"
        elif time_left / total_time <= 0.15 and self.completed_tasks < self.total_tasks:
            self.urgency = "Высокий"
        else:
            self.urgency = "Обычный"

    def calculate_speeds(self):
        today = datetime.now()
        days_remaining = (self.deadline - today).days

        if days_remaining > 0:
            tasks_left = self.total_tasks - self.completed_tasks
            self.required_speed = tasks_left / days_remaining
        else:
            self.required_speed = float('inf')
        td = (datetime.now() - self.start_date).days
        self.actual_speed = self.completed_tasks / td

    def __str__(self):
        table = PrettyTable()
        table.field_names = ["Название задачи", "Приоритет",
                             "Требуемая скорость", "Фактическая скорость",
                             "Выполнено", "Всего задач", "Дедлайн",
                             "Срочность"]
        table.add_row([
            self.name,
            f"{self.priority:.6f}",
            f"{self.required_speed:.6f}",
            f"{self.actual_speed:.6f}",
            self.completed_tasks,
            self.total_tasks,
            self.deadline.strftime("%Y-%m-%d %H:%M"),
            self.urgency
        ])
        return table.get_string()


if __name__ == "__main__":
    # Пример использования
    task1 = Task(name="Цифровая кафедра", start_date=datetime(2024, 11, 1),
                 deadline=datetime(2024, 11, 10))
    task2 = Task(name="Системная аналитика", start_date=datetime(2024, 7, 1),
                 deadline=datetime(2024, 12, 1))
    task3 = Task(name="Научно-исследовательская работа",
                 start_date=datetime(2024, 10, 15),
                 deadline=datetime(2024, 12, 1))

    # Расчет приоритета, срочности и скоростей

    print(task1)
    print(task2)
    print(task3)
