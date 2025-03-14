# файл, использующийся для нахождения градиента от функции нескольких переменных
k_local = 3
N_local = 8
polinom_coeff = [((5 - k_local) / 10, ''), (0, ''), (-(N_local + 1) / 2, ''), (1, '')]

variables = ['x']

zero = (0, '')
# каждая строка - коэффициенты при переменной
polinom_coeffs= [[((5 - k_local) / 10, ''), (0, ''), (-(N_local + 1) / 2, ''), (1, '')]]

polinom_degrees = [len(i) - 1 for i in polinom_coeffs]

def convert_to_str_multiple(polinom_degrees=polinom_degrees, polinom_coeffs=polinom_coeffs, variables=variables):
    res = []
    for i in range(len(variables)):
        variable = variables[i]
        func = ''
        polinom_degree = polinom_degrees[i]
        polinom_coeff = polinom_coeffs[i]
        for pow in range(polinom_degree, -1, -1):
            func = func + f'{polinom_coeff[polinom_degree - pow][0]} * {variable} ** {pow}' + '*' * (polinom_coeff[polinom_degree - pow][1] != '') + f'{polinom_coeff[polinom_degree - pow][1]} +  '
        res.append(func)

    return ''.join(res)[:-4]

def f_multiple(*values):
    d = {variables[i]: values[i] for i in range(len(values))}
    return eval(convert_to_str_multiple(), d)




def find_gradient_vect(*values):
    polinom_degrees, polinom_coeffs, variables = gradient_stuff()
    diction = {variables[i]: values[i] for i in range(len(values))}
    res = []
    for i in range(len(variables)):
        variable = variables[i]
        func = ''
        polinom_degree = polinom_degrees[i]
        polinom_coeff = polinom_coeffs[i]
        for pow in range(polinom_degree, -1, -1):
            func = func + f'{polinom_coeff[polinom_degree - pow][0]} * {variable} ** {pow} ' + '*' * (polinom_coeff[polinom_degree - pow][1] != '') + f'{polinom_coeff[polinom_degree - pow][1]} + '
        res.append(eval(func[:-2], diction))


    return res

def find_gradient(*values):
    diction = {variables[i]: values[i] for i in range(len(variables))}
    return eval(convert_to_str_multiple(*gradient_stuff()), diction)


def gradient_stuff(polinom_degrees=polinom_degrees, polinom_coeffs=polinom_coeffs):
    new_degreees = [polinom_degrees[i] - 1 for i in range(len(polinom_degrees))]
    new_coeffs = []
    for variable in range(len(new_degreees)):
        polinom_degree = new_degreees[variable] + 1
        polinom_coeff = polinom_coeffs[variable]
        new_coeff = [0] * polinom_degree
        new_degree = polinom_degree - 1
        for pow in range(polinom_degree - 1, -1, -1):
            new_coeff[new_degree - pow] = (polinom_coeff[new_degree - pow][0] * (pow + 1), polinom_coeff[new_degree - pow][1])
        new_coeffs.append(new_coeff)
    return new_degreees, new_coeffs, variables


if __name__ == '__main__':
    print(convert_to_str_multiple())
    print(find_gradient(1))
    print(find_gradient_vect(1))