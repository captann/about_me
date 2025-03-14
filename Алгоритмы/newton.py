# нахождение минимума функции с помощью метода ньютона
import random
from config import *
from dihotomy import min_otr

def df1(x):
    return 6 * x ** 5 - 8

def df2(x):
    return 30 * x ** 4

from prettytable import PrettyTable
mytable = PrettyTable()
def newton(a, b, eps):
    global mytable
    mytable = PrettyTable()
    mytable.field_names = ['Итерация', 'Xk', 'Xk+1', "f'(x0)", "f''(x0)"]
    df_1_coef = df_coef()
    k = 0
    x0 = max(a, b) - (max(a, b) - min(a, b))/ 5
    x1 = x0
    while True:
        df_v1 = df(x0)
        df_v2 = df(x=x0, polinom_degree=df_1_coef[0], polinom_coeff=df_1_coef[1])
        x1 = x0 - df_v1 / df_v2

        if k == 4:
            mytable.add_row([k, round(x0, 5), round(x1, 5), round(df_v1, 5),
                             round(df_v2, 5)])
            print('end', round(abs(df_v1), 7))
            return x1, k
        if abs(df_v1) <= eps:
            return x1, k
        k = k + 1
        mytable.add_row([k-1, round(x0, 5), round(x1, 5), round(df_v1, 5), round(df_v2, 5)])
        x0 = x1



if __name__ == '__main__':

    a, b = 0.8, 1.2
    n = -3
    eps = 10 ** n
    res, k = newton(a, b, eps)
    print(f'Минимальная точность для 4х итераций: {10 ** n}')
    print(res)
    print(mytable)
