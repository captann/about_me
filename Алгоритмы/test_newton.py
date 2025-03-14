def df2(x):
    return 30 * x ** 4

def df1(x):
    return 6 * x ** 5 - 8

from prettytable import PrettyTable
mytable = PrettyTable()

def newton(a, b, eps):
    k = 0
    x0 = 1.5
    x1 = x0
    while True:
        df_v1 = df1(x0)
        df_v2 = df2(x0)
        if abs(df_v1) <= eps:
            return x1, k
        k = k + 1
        x0 = x1
        x1 = x0 - df_v1 / df_v2

if __name__ == '__main__':
    if __name__ == '__main__':
        a, b = 1, 2
        n = -7
        eps = 10 ** n
        res, k = newton(a, b, eps)
        print(res, k)
