import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from sklearn.metrics import r2_score
from scipy.optimize import least_squares


class Model(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        global n
        Mod = poly(n, args, x)
        return Mod


# Формирует ряд Фурье нужной длинны
def poly(n, arg, x):
    if n == 0:
        return arg[0]
    else:
        return arg[n]*x**n + poly(n-1, arg, x)


def regr(args, x, y):
    global n
    Mod = poly(n, args, x)
    return Mod - y


def get_poly_graph(N, dff, x='Heading', y='Front_Z'):
    R2 = []
    global n
    for n in range(2, N, 1):
        p0 = np.ones(2 * n + 1)
        x_data = dff[x]
        res_lsq_front = least_squares(regr, p0, args=(x_data, dff[y]))
        Mod_front = Model(x_data, res_lsq_front.x)
        R2.append(round(r2_score(dff[y], Mod_front.y), 4))

    X = np.arange(2, N, 1)
    fig, ax = plt.subplots()
    ax.plot(X, R2)
    ax.plot(X, R2, 'ro')
    plt.xlabel('Степень полинома')
    plt.ylabel('Коэффициент детерминации')
    plt.title('Аппроксимация функции полиномом')
    ax.set_xlim([1, N])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
    plt.grid()


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_R'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5
df['Back_R'] = (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5

# Выделение коробки
df = df.iloc[4200:]
# Повторная нумерация
df = df.reset_index(drop=True)
# , 'M_Right'

# get_poly_graph(10, df, x='Roll')
get_poly_graph(10, df, x='Heading', y='Front_Z')

plt.show()
