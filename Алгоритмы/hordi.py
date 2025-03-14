# нахождение минимума функции с помощью метода хорд
from config import *
from dihotomy import min_otr
from prettytable import PrettyTable
mytable = PrettyTable()

def hordi(a, b, eps):
    global mytable
    mytable = PrettyTable()
    mytable.field_names = ["Итерация", "a", "b", "df(a)", "df(b)",
                           'df_a * df_b < 0', "x*", "x~",
                           "df(x~)"]
    # 1
    k = 0
    x_zv = 0
    x_tilda = 0
    df_tilda = 0
    while True:
        df_a = df(a)
        df_b = df(b)
        df_str = ''
        # 2
        if df_a * df_b >= 0:
            if df_a < 0 and df_b < 0:
                x_zv = b
            elif df_a > 0 and df_b > 0:
                x_zv = a
        # 3
        x_tilda = a - (df_a * (b - a)) / (df_b - df_a)
        k = k + 1
        # 4
        df_tilda = df(x_tilda)
        # 5
        mytable.add_row([k, round(a, 5), b, round(df_a, 5), round(df_b, 5), df_a * df_b < 0, round(x_zv, 5), round(x_tilda, 5), round(df_tilda, 5)])

        if abs(df_tilda) <= eps:
            x_zv = x_tilda
            return x_zv, k
        # 6
        if df_tilda > 0:
            b = x_tilda
        else:
            a = x_tilda
if __name__ == '__main__':
    a, b = 1, 2
    n = 0
    eps = 10 ** n
    res,  k = hordi(a, b, eps)
    while k < 4:
        n = n - 1
        eps = 10 ** n
        res, k = hordi(a, b, eps)
    print(f'Минимальная точность для 4х итераций: {10**n}')


    print(f'x* = {round(hordi(a, b, eps)[0], 5)}, Fmin={round(f(hordi(a, b, eps)[0]), 5)}')
    print(mytable)