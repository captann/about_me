# нахождение минимума функции методом дихотомии
from math import *
import random
from config import *

def min_otr():
    x0 = 0.001
    delta = x0 / 10
    k = 0
    k6 = 0
    xprev = 0
    xm = 0
    flag = True
    while True:
        if flag:
            if f(x0 + delta) < f(x0):
                k = k + 1
            elif f(x0 + delta) >= f(x0):
                delta = -delta
                k = k + 1
            if f(x0 + delta) >= f(x0):
                delta = delta / 2
                k6 = k6 + 1
                if k6 == 3:
                    a, b = x0 - delta, x0 + delta
                    break
        if k >= 2:
            xm = x0
            x0 = x1

        x1 = x0 + delta
        flag = True

        if f(x1) >= f(x0):
            a, b = sorted([xm, x1])
            break
        elif f(x1) < f(x0):
            k = k + 1
            flag = False
    return a, b
