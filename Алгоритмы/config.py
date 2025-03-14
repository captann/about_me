eps = 0.015
k_local = 3
N_local = 8
round_up = 8
polinom_coeff = [1, 0, 0, 0, 0, -8, 3]
#x 8* 6 - 8x + 3
polinom_degree = len(polinom_coeff) - 1

def convert_to_str(polinom_degree=polinom_degree, polinom_coeff=polinom_coeff):
    func = ''
    for pow in range(polinom_degree, -1, -1):
        func = func + f'{polinom_coeff[polinom_degree - pow]} * x ** {pow} + '
    func = func[:-2]
    return func

def f(x, polinom_degree=polinom_degree, polinom_coeff=polinom_coeff):
    func = 0
    for pow in range(polinom_degree, -1, -1):
        func = func + polinom_coeff[polinom_degree - pow] * x ** pow
    return func


def df(x, polinom_degree=polinom_degree, polinom_coeff=polinom_coeff):
    new_coeff = [0] * polinom_degree
    new_degree = polinom_degree - 1
    for pow in range(polinom_degree - 1, -1, -1):
        new_coeff[new_degree - pow] = polinom_coeff[new_degree - pow] * (pow + 1)
    return f(x, new_degree, new_coeff)

def df_coef(polinom_degree=polinom_degree, polinom_coeff=polinom_coeff):
    new_coeff = [0] * polinom_degree
    new_degree = polinom_degree - 1
    for pow in range(polinom_degree - 1, -1, -1):
        new_coeff[new_degree - pow] = polinom_coeff[new_degree - pow] * (pow + 1)
    return new_degree, new_coeff

if __name__ == '__main__':
    pass