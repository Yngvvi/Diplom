import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score
from scipy.optimize import least_squares
from Classaes import Graph, PlotGraph, LinGraph

# Фурье кусками

class Model(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        global n
        Mod = furCikl(n, args, x)
        return Mod


# Формирует ряд Фурье нужной длинны
def furCikl(n, arg, x):
    if n == 0:
        return arg[0]
    else:
        return arg[2*n]*np.cos(n*x) + arg[2*n-1]*np.sin(n*x) + furCikl(n-1, arg, x)


def regr(args, x, y):
    global n
    Mod = furCikl(n, args, x)
    return Mod - y


def get_fur_graph(N, dff, x='Heading', y='Front_Z'):
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
    plt.xlabel('Количество членов ряда Фурье')
    plt.ylabel('Коэффициент детерминации')
    plt.title('Аппроксимация функции рядами Фурье')
    ax.set_xlim([1, N])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
    plt.grid()

path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_R'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5
df['Back_R'] = (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5

# Выделение коробки
df = df.iloc[10400:]
# Крайняя граница для деления на участки
max_heading = max(df['Heading'])

# Аппроксимация Heading рядами Фурье по частям начало
# Первая половина
# data_1 = df.loc[df['Heading'] <= max_heading/2]

# Вторая половина
# data_1 = df.loc[df['Heading'] > max_heading/2]

# Первая четверть
# data_1 = df.loc[df['Heading'] <= max_heading/4]

# Вторая четверть
# data_1 = df.loc[(df['Heading'] > max_heading/4) & (df['Heading'] <= max_heading/2)]

# Третья четверть
# data_1 = df.loc[(df['Heading'] > max_heading/2) & (df['Heading'] <= max_heading*3/4)]

# Четвертая четверть
# data_1 = df.loc[df['Heading'] > max_heading*3/4]

# data_1 = data_1.reset_index(drop=True)
# get_fur_graph(10, data_1)
# Аппроксимация Heading рядами Фурье по частям конец

# Аппроксимация Roll рядами Фурье
# get_fur_graph(10, df, x='Roll')

# Аппроксимация Pitch рядами Фурье
# get_fur_graph(10, df, x='Pitch')

# Аппроксимация M_UP рядами Фурье
# get_fur_graph(20, df, x='M_UP')

# Аппроксимация M_Right рядами Фурье
# get_fur_graph(20, df, x='M_Right')

# Аппроксимация Bat50 рядами Фурье
# get_fur_graph(20, df, x='Bat50')


# Аналогичные действия для других осей и направлений

# Ось Х Front
# get_fur_graph(20, df, x='Heading', y='Front_X')
# get_fur_graph(20, df, x='Roll', y='Front_X')
# get_fur_graph(20, df, x='Pitch', y='Front_X')
# get_fur_graph(20, df, x='M_UP', y='Front_X')
# get_fur_graph(20, df, x='M_Right', y='Front_X')
# get_fur_graph(20, df, x='Bat50', y='Front_X')

# Ось Х Back
# get_fur_graph(20, df, x='Heading', y='Back_X')
# get_fur_graph(20, df, x='Roll', y='Back_X')
get_fur_graph(20, df, x='Pitch', y='Back_X')
# get_fur_graph(20, df, x='M_UP', y='Back_X')
# get_fur_graph(20, df, x='M_Right', y='Back_X')
# get_fur_graph(20, df, x='Bat50', y='Back_X')

plt.show()
