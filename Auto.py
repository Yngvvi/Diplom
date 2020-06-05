import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import least_squares
from sklearn.metrics import r2_score

# Общая модель
class Model_new (object):
    def __init__(self, x, args, mod):
        self.x = x
        self.args = args
        if mod == 'L':
            self.y = self.model_light(x, args)
        elif mod == 'F':
            self.y = self.model(x, args)
        elif mod == 'Z':
            self.y = self.model_Z(x, args)

    def model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]) + args[2]*np.sin(x[0]) + args[3]*x[1]
        # Компенсация маршевых двигателей
        Mod = Mod + args[4]*x[2]*np.abs(np.cos(x[0]))*np.sin(x[0]/2)
        Mod = Mod + args[5]*x[3]*np.sin(x[0]/2)
        # Компенсация работы батарей 50В
        Mod = Mod + args[6]*(x[4] - args[7])*np.sin(x[0]/2)
        # Компенсация угла дифферента
        Mod = Mod + args[8] * x[5]
        return Mod

    def model_light(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]) + args[2]*np.sin(x[0]) + args[3]*x[1]
        # Компенсация угла дифферента
        Mod = Mod + args[4] * x[2]
        return Mod

    def model_Z(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0] * 2)
        Mod = Mod + +args[3] * np.sin(x[0] * 2) ** 2
        Mod = Mod + args[4] * np.sin(0.81 * x[0])
        Mod = Mod + args[5] * x[1] + args[6] * x[2]
        return Mod


def setPointGraph_new(tittle, x, *y, pos='lower right'):
    fig, ax = plt.subplots()
    y_lebels = []
    if x.name is None:
        x_lebel = 'Index'
    else:
        x_lebel = x.name
    for i in y:
        ax.scatter(x, i, s=1)
        if i.name is not None:
            y_lebels.append(i.name)
        else:
            y_lebels.append('Model')
    ax.set_title(tittle)
    ax.set_xlabel(x_lebel)
    ax.legend(y_lebels, loc=pos)
    ax.grid()


def setGraph_new(tittle,  x, *y, pos='upper right'):
    fig, ax = plt.subplots()
    y_lebels = []
    if x.name is None:
        x_lebel = 'Index'
    else:
        x_lebel = x.name
    # Больше 2-х функций plot переварить не может, поэтому цикл
    for i in y:
        ax.plot(x, i)
        y_lebels.append(i.name)
    ax.set_title(tittle)
    ax.set_xlabel(x_lebel)
    ax.legend(y_lebels, loc=pos)
    ax.grid()


def z_regr(args, x, y):
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0] * 2)
    Mod = Mod + +args[3] * np.sin(x[0] * 2) ** 2
    Mod = Mod + args[4] * np.sin(0.81 * x[0])
    Mod = Mod + args[5] * x[1] + args[6] * x[2]
    return Mod - y


def siple_regr(args, x, y):
    # Компенсация курса и крена
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
    # Компенсация угла дифферента
    Mod = Mod + args[4] * x[2]
    return Mod - y


def getMod(y, dff, Model, regr, num):
    p0 = np.ones(num)
    x_data = [dff['Heading'], dff['Roll'], dff['Pitch']]
    res_lsq = least_squares(regr, p0, args=(x_data, dff[y]))
    Mod_front = Model(x_data, res_lsq.x)
    dff[y + '_comp'] = dff[y] - Mod_front.y
    return Mod_front.y


def printInfo(res, y, dff, Mod, prec=4):
    print('Коэффициенты для ' + y, np.round(res.x, 2))
    print('Коэффициент детерминации' + y, round(r2_score(dff[y], Mod), prec))


def getAll(y, dff, Model, regr, num, M='L', gr_nums=2, prec=4, pos='lower right'):
    p0 = np.ones(num)
    x_data = [dff['Heading'], dff['Roll'], dff['Pitch']]
    res_lsq = least_squares(regr, p0, args=(x_data, dff[y]))
    Mod = Model(x_data, res_lsq.x, M)
    dff[y + '_comp'] = dff[y] - Mod.y
    print('Коэффициенты для ' + y, np.round(res_lsq.x, 2))
    print('Коэффициент детерминации ' + y, round(r2_score(dff[y], Mod.y), prec))
    if gr_nums == 2:
        setGraph_new('Compensation ' + y, dff.index, dff[y], dff[y + '_comp'], pos=pos)
    else:
        setGraph_new('Compensation ' + y, dff.index, dff[y + '_comp'], pos=pos)
    setPointGraph_new('Compensation ' + y, dff['Heading'], dff[y], Mod.y)


# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573219511080000.csv'

path = input('Введите путь до файла ',)

df = pd.read_csv(path, sep=';')

# Удаление строк в которых аппарат ещё не движется
df_clean = df.drop(df.index[(df['VertForvUp'] == 0) & (df['VertForvDown'] == 0) &
                   (df['VertBackUp'] == 0) & (df['VertBackDown'] == 0)])
# или перемещается с использованием маневренных двигателей
df_clean = df_clean.drop(df.index[(df['VertForvUp'].abs() + df['VertForvDown'].abs()
                   + df['VertBackUp'].abs() + df['VertBackDown'].abs()) > 0.15])

df_clean['Bat50'] = df_clean['Bat1_50_I'] + df_clean['Bat2_50_I'] + \
                    df_clean['Bat3_50_I'] + df_clean['Bat4_50_I']

df_clean['Front_R'] = (df_clean['Front_X']**2 + df_clean['Front_Y']**2 + df_clean['Front_Z']**2)**0.5
df_clean['Back_R'] = (df_clean['Back_X']**2 + df_clean['Back_Y']**2 + df_clean['Back_Z']**2)**0.5


getAll('Front_X', df_clean, Model_new, siple_regr, 5)
getAll('Front_Y', df_clean, Model_new, siple_regr, 5)
getAll('Front_R', df_clean, Model_new, siple_regr, 5, gr_nums=1)
getAll('Front_Z', df_clean, Model_new, z_regr, 7, M='Z', gr_nums=1)
df_clean['Front_sum_R'] = (df_clean['Front_X_comp']**2 + df_clean['Front_Y_comp']**2 + df_clean['Front_Z_comp']**2)**0.5
setGraph_new('Сравнеие', df_clean.index, df_clean['Front_R_comp'], df_clean['Front_sum_R'])

plt.show()