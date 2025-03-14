# код для решения транспортной задачи (визуализация каждого шага в таблице +
# + подсветка таблиц и строк, которые можно использовать)
from prettytable import PrettyTable

MEMORY = set()

def drob(ch, *zn):
    if str(ch) == '0':
        return '0/1'
    if zn:
        zn = zn[0]
    else:
        zn = 1
        return str(ch)
    if str(ch * zn) == '0':
        return '0/1'
    znak = ch * zn / abs(ch * zn) > 0

    ch = abs(ch)
    zn = abs(zn)
    for i in range(1):
        if i == 0:
            CH, ZN = ch, zn
            continue
        m1, m2 = ch, zn
        while m1 != m2:
            if m1 > m2:
                m1 -= m2
            else:
                m2 -= m1
        ch, zn = ch // m1, zn // m1
        if zn != ZN:
            CH = ch * ZN + CH * zn
            ZN *= zn
        else:
            CH += ch
    m1, m2 = CH, ZN
    while m1 != m2:
        if m1 > m2:
            m1 -= m2
        else:
            m2 -= m1
    CH, ZN = int(CH / m1), int(ZN / m1)
    return (f"{'-' * (not znak)}{CH}/{ZN}")


class Drob:
    def __init__(self, drobe: str):
        self.num = int(drobe.split("/")[0])
        self.den = 1
        if "/" in drobe:
            self.den = int(drobe.split("/")[1])

        self.drob = drob(self.num, self.den)

        self.num = int(self.drob.split("/")[0])
        self.den = 1
        if "/" in self.drob:
            self.den = int(self.drob.split("/")[1])

    def reversed(self):
        return Drob(drob(self.den, self.num))

    def __str__(self):
        if self.den == 1:
            return str(self.num)
        return self.drob

    def __eq__(self, other):
        return self.num == other.num and self.den == other.den

    def __ne__(self, other):
        return (self.num != other.num) or (self.den != other.den)

    def __lt__(self, other):
        return self.num * other.den < self.den * other.num

    def __gt__(self, other):
        return self.num * other.den > self.den * other.num

    def __le__(self, other):
        return self.num * other.den <= self.den * other.num

    def __ge__(self, other):
        return self.num * other.den >= self.den * other.num

    def __abs__(self):
        return Drob(drob(abs(self.num), abs(self.den)))

    def __add__(self, other):
        return Drob(drob(self.num * other.den + self.den * other.num,
                         self.den * other.den))

    def __sub__(self, other):
        return Drob(drob(self.num * other.den - self.den * other.num,
                         self.den * other.den))

    def __mul__(self, other):
        return Drob(drob(self.num * other.num, self.den * other.den))

    def __truediv__(self, other):
        return Drob(drob(self.num * other.den, self.den * other.num))


ZERO = Drob('0/1')
MINUS_ONE = Drob('-1/1')


def mk_drob(table):
    new_table = []
    for i in range(len(table)):
        new_table.append([])
        for j in range(len(table[i])):
            new_table[i].append(Drob(str(table[i][j])))
    return new_table


def find_new_element(a, b, c, r):
    return a - (b * c) / r


def get_name(name_number):
    return f"Таблица {name_number}"


class Table:
    def __init__(self, rows: list, columns: list, content, name: str):
        self.rows = rows
        self.columns = columns
        self.content = content
        self.name = name
        self.find_type()

    def __str__(self):
        table = PrettyTable()
        table.title = self.name
        table.field_names = ["БП \\ СП"] + self.columns

        for r in range(len(self.rows)):
            row = []
            for c in range(len(self.columns) + 1):
                if c == 0:
                    row.append(self.rows[r])
                else:
                    row.append(self.content[r][c - 1])
            table.add_row(row)
        row = ["Брать?"] + [" "] * len(self.columns)
        c = []

        for i in range(len(self.content) - 1):
            c.append(self.content[i][-1])
        for i in range(len(c)):
            if c[i] < ZERO:
                for j in range(len(self.content[i])):
                    if self.content[i][j] >= ZERO:
                        row[j + 1] = "+"
        table.add_row(row)

        return str(table)

    def find_type(self):
        types = ["Неполупприведённая", "Полуприведённая", "Приведённая"]
        b = [row[-1] for row in self.content][:-1]
        c = self.content[-1][:-1]
        if any([i < ZERO for i in b[:-1]]):
            self.type = types[0]
        elif all([i >= ZERO for i in b]) and any([i <= ZERO for i in c]):
            self.type = types[1]
        elif all([i >= ZERO for i in b]) and any([i >= ZERO for i in c]):
            self.type = types[2]
        else:
            self.type = 'Не определён'



    def __eq__(self, other):
        return self.rows == other.rows and self.columns == other.colums

    def create_new_table(self, name, row, column):
        print(row, column)

        row = self.rows.index(row)
        column = self.columns.index(column)
        c = self.columns[column]
        self.columns[column] = self.rows[row]
        self.rows[row] = c
        new_content = []

        for i in range(len(self.content)):
            new_content.append([])
            for j in range(len(self.content[i])):
                new_content[i].append(ZERO)
        total_rows = len(self.rows)
        total_columns = len(self.columns)
        new_content[row][column] = Drob(f"{self.content[row][column]}").reversed()
        for i in range(total_rows):
            if i != row:
                new_content[i][column] = self.content[i][column] / \
                                         self.content[row][column]
        for j in range(total_columns):
            if j != column:
                new_content[row][j] = MINUS_ONE * self.content[row][j] / \
                                      self.content[row][column]

        for i in range(0, row):
            for j in range(0, column):
                new_content[i][j] = self.content[i][j] - (
                            self.content[row][j] * self.content[i][column] /
                            self.content[row][column])
        # print('---')
        for i in range(row + 1, total_rows):
            for j in range(0, column):
                new_content[i][j] = self.content[i][j] - (
                            self.content[row][j] * self.content[i][column] /
                            self.content[row][column])

                pass
                # print(i, j, self.content[i][j])
        # print('---')

        for i in range(0, row):
            for j in range(column + 1, total_columns):
                new_content[i][j] = self.content[i][j] - (
                            self.content[row][j] * self.content[i][column] /
                            self.content[row][column])

                # print(i, j, self.content[i][j])
        for i in range(row + 1, total_rows):
            for j in range(column + 1, total_columns):
                new_content[i][j] = self.content[i][j] - (
                            self.content[row][j] * self.content[i][column] /
                            self.content[row][column])

                # print(i, j, self.content[i][j])
                pass
        new_table = Table(self.rows, self.columns, new_content, name)
        return new_table


    def show_line(self, bas_col):

        col = self.columns.index(bas_col)
        table = PrettyTable()
        table.title = self.name
        table.field_names = ["БП \\ СП"] + self.columns + [f"b/{bas_col}"] + ["Min?"]
        minimising = []
        for r in range(len(self.rows)):
            row = []
            for c in range(len(self.columns) + 2):
                if c == 0:
                    row.append(self.rows[r])
                elif c !=0 and c <= len(self.columns):
                    row.append(self.content[r][c - 1])
                else:
                    row.append(self.content[r][c - 2] /self.content[r][col] )
            minimising.append(row[-1])
        indexes = []
        if list(filter(lambda x: x < ZERO, minimising[:-1])):
            m = max(filter(lambda x: x < ZERO, minimising[:-1]))
            for i in range(len(minimising)):
                if minimising[i] == m:
                    indexes.append(i)
        for r in range(len(self.rows)):
            row = []
            for c in range(len(self.columns) + 2):
                if c == 0:
                    row.append(self.rows[r])
                elif c !=0 and c <= len(self.columns):
                    row.append(self.content[r][c - 1])
                else:
                    row.append(self.content[r][c - 2] /self.content[r][col] )
            if r in indexes:
                row.append("+")
            else:
                row.append(" ")
            table.add_row(row)

        return str(table)




def algoritm(rows, columns, content):
    name_number = 1
    table = Table(rows, columns, content, get_name(name_number))
    while True:
        print(table)
        bas_col = input("Колонка: ").split()[0]
        print(table.show_line(bas_col))
        bas_line = input("Строка: ").split()[0]
        name_number = name_number + 1
        table = table.create_new_table(row=bas_line, column=bas_col,name=get_name(name_number))

    print(table.type)
    print(table)


if __name__ == "__main__":
    algoritm(["y5", "y6", "Ф*(y)"], ["y1", "y2", "y3", "y4", "c"],
             mk_drob([
                 [2, -3, -1, 0, 4],
                 [5, -2, 0, 1, -3],
                 [10, -1, -2,  4, 0]
             ]))
    algoritm(["y5", "y6", "Ф*(y)"], ["y1", "y2", "y3", "y4", "c"],
        mk_drob([
        [2, -1, 1, 0, 3],
        [7, -2, 0, -1, -1],
        [14, -1, 3, -2, 0]
        ]))
    algoritm(["x3", "x4", "x5", "x6", "F(x)"], ["x1", "x2", "b"],
             mk_drob([
                 [-2, -5, 10],
                 [3, 2, -1],
                 [1, 0, -2],
                 [0, -1, 4],
                 [4, -3, 0]
             ]))
    """[-1, -1, 2, -1, -1],
        [2, 2, 2, 2, 2],
        [10, -1, -2, 4, 0]"""
