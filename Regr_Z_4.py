import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score
from scipy.optimize import least_squares
from Classaes import Graph, PlotGraph, LinGraph

# Размер ряда Фурье
# n = 15



class Model(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        Mod = furCikl(n, args, x)
        return Mod


# Формирует ряд Фурье нужной длинны
def furCikl(n, arg, x):
    if n == 0:
        return arg[0]
    else:
        return arg[2*n]*np.cos(n*x) + arg[2*n-1]*np.sin(n*x) + furCikl(n-1, arg, x)


def regr(args, x, y):
    Mod = furCikl(n, args, x)
    return Mod - y


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

N = 20

R2 = []
for n in range (2, N, 1):
    p0 = np.ones(2 * n + 1)
    x_data = df['Heading']
    res_lsq_front = least_squares(regr, p0, args=(x_data, df['Front_Z']))
    Mod_front = Model(x_data, res_lsq_front.x)
    R2.append(round(r2_score(df['Front_Z'], Mod_front.y), 4))

X = np.arange(2, N, 1)
fig, ax = plt.subplots()
ax.plot(X, R2)
ax.plot(X, R2, 'ro')
plt.xlabel('Количество членов ряда Фурье')
plt.ylabel('Коэффициент детерминации')
plt.title('Аппроксимация функции рядами Фурье')
ax.set_xlim([1, N])
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))

plt.grid()
plt.show()

# p0 = np.ones(2*n + 1)
# x_data = df['Heading']
# res_lsq_front = least_squares(regr, p0, args=(x_data, df['Front_Z']))
# Mod_front = Model(x_data, res_lsq_front.x)
# df['Z_Front_comp'] = df['Front_Z'] - Mod_front.y

# prec = 4
# print('Коэффициенты для фронтального датчика:', res_lsq_front.x)
# print('Коэффициент детерминации', round(r2_score(df['Front_Z'], Mod_front.y), prec))
#
# Gr = Graph(['Front_Z', 'Test'], ['Heading','Index'])
#
# Gr.auto_slider(Mod_front, 2*n+1, 'a')
# Gr.plot_sc(df['Heading'], df['Front_Z'], Mod_front.y )
# Gr.plot_pl_one(df.index, df['Front_Z'], df['Z_Front_comp'])

