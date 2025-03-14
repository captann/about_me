# нахождение минимума функции градиентным спуском
import random
from config import *
from several_x import *



class Vector:
    def __init__(self, x: list):
        self.coords = x
        self.length = len(self.coords)

    def st(self, alpha: int):
        return Vector([self.coords[i] ** alpha for i in range(self.length)])

    def umn(self, k: float):
        return Vector([self.coords[i] * k for i in range(self.length)])

    def __sub__(self, other):
        res = []
        M = max(self.length, other.length)
        m = min(self.length, other.length)
        flag = self.length > other.length
        for i in range(M):
            if i < m:
                res.append(self.coords[i] - other.coords[i])
            else:
                if flag:
                    res.append(self.coords[i])
                else:
                    res.append(other.coords[i])
        return Vector(res)

    def __add__(self, other):
        res = []
        M = max(self.length, other.length)
        m = min(self.length, other.length)
        flag = self.length > other.length
        for i in range(M):
            if i < m:
                res.append(self.coords[i] + other.coords[i])
            else:
                if flag:
                    res.append(self.coords[i])
                else:
                    res.append(other.coords[i])
        return Vector(res)

    def __str__(self):
        return str(self.coords)

def algoritm():
    # этап 1
    k = 0

    x0 = Vector([random.random() for _ in range(len(variables))])
    # альфа
    step = random.random()
    x1 = x0

    while True:
        # этап 2
        x0 = x1
        x1 = x0 - Vector(find_gradient_vect(*x0.coords)).umn(step)

        if f_multiple(*x1.coords) >= f_multiple(*x0.coords):
            step = step / 2
        else:
            eps = 10 ** -8
            if f_multiple(*x0.coords) - f_multiple(*x1.coords) <= eps:
                return x1.coords
            else:
                k = k + 1


if __name__ == '__main__':
    print(algoritm())


