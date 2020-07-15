import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# def foo(x1, x2=None):
#     if x2 is None:
#         x2 = []
#     print(x1)
#     if len(x2)!=0:
#         print(x2)
#
#
# x = np.array([1, 5, 10, 15, 20])
#
# foo(x)


def mid(der):
    mid = sum(df[der]) / df.shape[0]
    Mid = df[der] - mid
    mid_res = sum(Mid) / df.shape[0]
    return mid_res


path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'

df = pd.read_csv(path, sep=';')

# Выделение коробки
df = df.iloc[4200:]
# Повторная нумерация
df = df.reset_index(drop=True)

print(mid('Front_X'))

