from config import *
def df2(x):
    deg, coefs = df_coef()

    print(x, 30 * x ** 4, df(x=x, polinom_degree=deg, polinom_coeff=coefs))

def df1(x):
    print(x, 6 * x ** 5 - 8, df(x))



df2(1.8)