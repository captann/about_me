def f(x):
    return x ** 6 - 8 * x + 3
def x(a, b,  L=184):
    return 0.5 * (((f(a) - f(b)) / L + a + b))

print(x(1, 2))