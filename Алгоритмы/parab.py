# нахождение минимума функции с помощью метода парабол
from config import *
from dihotomy import min_otr
from prettytable import PrettyTable
mytable = PrettyTable()


def find_a0(x1):
    return f(x1)
def find_a1(x1, x2):
    return (f(x2) - find_a0(x1)) / (x2 - x1)
def find_a2(x1, x2, x3):
    return 1 / (x3 - x2) * ((f(x3) - f(x1)) / (x3 - x1) - (f(x2) - f(x1)) / (x2 - x1))
def get_x1_x2_x3(a, b):

    x1 = a + (b - a) / 17
    x2 = a + (b - a) / 7
    x3 = b - (b - a) / 17

    return x1, x2, x3

def parabola_new(a, b, eps):
    global mytable
    mytable = PrettyTable()
    mytable.field_names = ['Номер итерации', 'a', 'b', 'x1', 'f(x1)', 'x2', 'f(x2)', 'x3', 'f(x3)', 'x~', 'f(x~)']
    k = 0
    x1, x2, x3 = get_x1_x2_x3(a, b)

    a1 = find_a1(x1, x2)
    a2 = find_a2(x1, x2, x3)
    x_tilda = 0.5 * (x1 + x2 - a1 / a2)
    x_tilda_prev = 0
    mytable.add_row([k, round(a, 5), round(b, 5), round(x1, 5), round(f(x1), 5), round(x2, 5), round(f(x2), 5), round(x3, 5), round(f(x3), 5), round(x_tilda, 5), round(f(x_tilda), 5)])
    while True:
        if k != 0:


            a1 = find_a1(x1, x2)
            a2 = find_a2(x1, x2, x3)
            x_tilda_prev = x_tilda
            x_tilda = 0.5 * (x1 + x2 - a1 / a2)
            if abs(x_tilda - x_tilda_prev) <= eps:
                return x_tilda, k
        #1
        if (x1 < x_tilda < x2 < x3) and (f(x_tilda) > f(x2)):
            x1 = x_tilda
            k = k + 1
        #2
        elif (x1 < x_tilda < x2 < x3) and (f(x_tilda) <= f(x2)):
            x3 = x2
            x2 = x_tilda
            k = k + 1
        #3
        elif (x1 < x2 < x_tilda < x3) and (f(x_tilda) > f(x2)):
            x3 = x_tilda
            k = k + 1
        #4
        elif (x1 < x2 < x_tilda < x3) and (f(x_tilda) <= f(x2)):
            x1 = x2
            x2 = x_tilda
            k = k + 1
        mytable.add_row(
            [k, round(a, 5), round(b, 5), round(x1, 5), round(f(x1), 5),
             round(x2, 5), round(f(x2), 5), round(x3, 5), round(f(x3), 5),
             round(x_tilda, 5), round(f(x_tilda), 5)])


if __name__ == '__main__':
    a, b = min_otr()
    n=-3
    eps = 10 ** n
    print(f'Минимальная точность для 4х итераций: {10**n}')
    print(parabola_new(a, b, eps))
    print(mytable)
