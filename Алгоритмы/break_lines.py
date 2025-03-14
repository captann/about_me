# нахождение минимума функции с помощью метода ломанных
from math import *
from sympy import symbols, Eq, solve
from parab import min_otr
from config import *
from prettytable import PrettyTable
L_table = PrettyTable()
alg = PrettyTable()

delts = PrettyTable()
delts.min_width = 30

def f(x):
    return x ** 6 - 8 * x + 3

def find_L(a, b):
    global  L_table
    L_table.field_names = ['Уравнение второй производной', 'Значения, из которых выбираем', 'Максимальное значение']
    # надо найти наибольший модуль функции производной на отрезке
    #a, b = min_otr()
    x = symbols('x')
    # первая производная
    degree, df_1 = df_coef()
    # уравнение вида "вторая производная равна нулю"
    eq = Eq(eval(convert_to_str(*df_coef(degree, df_1))), 0)
    I = 1j
    # решения этого уравнения

    solution = [eval(str(i)) for i in solve(eq, x) if not isinstance(i, complex)]
    # убирание комплексных корней и тех корней, что не лежат в промежутке (a, b)
    solution = list(filter(lambda x: not isinstance(x, complex) and a <= x <= b, solution))
    # добавляем концы отрезков
    solution.append(b)
    solution.append(a)
    # отставляем только уникальные x
    solution = list(filter(lambda x: x in solution, solution))
    # нахождение модуля первой производной для её точек экстремума и на её границах
    values = [abs(df(x)) for x in solution]
    L_table.add_row([eq,  values, max(values)])
    return max(values)
def lomannie(a, b, eps):
    global L_table, delts
    k = 0
    L = find_L(a, b)
    print(L)

    x0 = 1/2 * ((f(a) - f(b)) / L + a + b)
    y0 = 1/2 * (f(a) + f(b) + L * (a - b))
    print(y0)
    x_zv = x0
    p_zv = y0
    delta = f(x_zv) - p_zv
    delts.field_names = ['Итерация', 'Значение delta']

    delts.add_row([k, delta])

    if delta <= eps:
        return x0
    current_point = (x_zv, p_zv)
    points = set()
    points.add(current_point)

    treug = 1 / (2 * L) * (f(x_zv) - p_zv)
    xst_1 = x_zv - treug
    xst_2 = x_zv + treug
    p = 1 / 2 * (f(x_zv) + p_zv)
    x_zv_prev = x_zv

    points.remove(current_point)
    points.add((xst_1, p))
    points.add((xst_2, p))
    alg.field_names = ["Итерация", "X(k)", "X(k)*", "P(k)*",
                       "F(Xk*)",
                       "DLT(k+1)", "Треугольник", "X'(k+1)", "X''(k+1)", "P(k+1)", "Точки"]
    alg.add_row([k, round(x0, 5), round(x_zv, 5), round(p_zv, 5),round(f(x_zv), 5), round(delta, 5),
                 round(treug, 5), round(xst_1, 5), round(xst_2, 5), round(p, 5), [[round(j, 5) for j in i] for i in points]])
    while (delta) > eps:
        x_zv, p_zv = min(points, key=lambda x: x[1])
        current_point = (x_zv, p_zv)
        delta = f(x_zv) - p_zv
        if (delta) < eps:
            return x_zv_prev

        treug = 1 / (2 * L) * (f(x_zv) - p_zv)
        xst_1 = x_zv - treug
        xst_2 = x_zv + treug
        p = 1 / 2 * (f(x_zv) + p_zv)
        points.add((xst_1, p))
        points.add((xst_2, p))
        points.remove(current_point)
        x_zv_prev = x_zv

        k = k + 1
        delts.add_row([k, delta])
        alg.add_row([k, round(x0, 5), round(x_zv, 5), round(p_zv, 5),
                     round(f(x_zv), 5), round(delta, 5),
                     round(treug, 5), round(xst_1, 5), round(xst_2, 5),
                     round(p, 5), [[round(j, 5) for j in i] for i in points]])
        if k == 4:
            print(delta)
            return x_zv_prev





if __name__ == '__main__':
    a, b = 1, 2
    eps = 10 ** -100
    print(lomannie(a, b, eps))
    print(alg)



