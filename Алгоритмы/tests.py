from grad import algoritm
from parab import *
from math import *
error = 0
suc = 0
values = []
for i in range(1000):

    try:
        values.append(algoritm()[0])
        suc += 1
    except Exception:
        error += 1
    print(suc, error)
    print('---')
#print(abs(sqrt(30) / 2 - sum(values) / suc ))
x = 20
import decimal
print(

decimal.Decimal(0.2) * decimal.Decimal(x) ** decimal.Decimal(3) +  decimal.Decimal(0) * decimal.Decimal(x) ** decimal.Decimal(2) +  decimal.Decimal(-4.5) * decimal.Decimal(x) ** decimal.Decimal(1) +  decimal.Decimal(1) * decimal.Decimal(x) ** decimal.Decimal(0) +
decimal.Decimal(0.6000000000000001) * decimal.Decimal(x) ** decimal.Decimal(2) +  decimal.Decimal(0) * decimal.Decimal(x) ** decimal.Decimal(1) +  decimal.Decimal(-4.5) * decimal.Decimal(x) ** decimal.Decimal(0)
)