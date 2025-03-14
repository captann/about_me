class Config:
    def __init__(self):
        self.required_calendars = {
                                   "Учёба": "Календарь для предметов, которые не были отдельно вынесены и обозначены",
                                   "Цифровая кафедра": "",
                                   "Системная аналитика": "",
                                   "Научно-исследовательская работа": "",
                                   "Закачка кистей": "",
                                   "Дорога": "",
                                   "Сон": "",
                                   "Дедлайны": "",
                                   "Начало новой задачи": "",
                                   "Институт": "",
                                   "Еда": "",
                                   "Прочее": ""
                                   }
        self.road_timing = {"В институт": 75,
                            "Из института": 90,
                            "Из ниститута, не спеша": 110,
                            "Иные, короткие дистанции": 20,
                            "Иные, средние дистанции": 60,
                            "Иные, длинные дистанции": 120,
                            }

    def __str__(self):
        from prettytable import PrettyTable
        table = PrettyTable()
        table.field_names = ["Название календаря", "Описание календаря"]
        for key in self.required_calendars:
            table.add_row([key, self.required_calendars[key]])
        return str(table)

if __name__ == '__main__':
    c = Config()
    print(c)
