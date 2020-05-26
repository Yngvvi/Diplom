# Опробуем модель от оси Z На остальных функциях
# Работает хуже

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import least_squares
from sklearn.metrics import r2_score
from time import process_time  # Считает время работы
from Utilities import plotFig, scatFig, setPointGraph_new, setGraph_new


class Model_Z(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]) + args[2]*np.sin(x[0]*2)
        Mod = Mod + +args[3]*np.sin(x[0]*2)**2
        Mod = Mod + args[4]*np.sin(0.81*x[0])
        Mod = Mod + args[5]* x[1] + args[6] * x[2]
        return Mod


def z_regr(args, x, y):
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0] * 2)
    Mod = Mod + +args[3] * np.sin(x[0] * 2) ** 2
    Mod = Mod + args[4] * np.sin(0.81 * x[0])
    Mod = Mod + args[5] * x[1] + args[6] * x[2]
    return Mod - y


def getMod(y, dff, Model=Model_Z, regr=z_regr, num=7):
    p0 = np.ones(num)
    x_data = [dff['Heading'], dff['Roll'], dff['Pitch']]
    res_lsq = least_squares(regr, p0, args=(x_data, dff[y]))
    Mod_front = Model(x_data, res_lsq.x)
    dff[y + '_comp'] = dff[y] - Mod_front.y
    return res_lsq.x, Mod_front.y


def printInfo(res, y, dff, Mod, prec=4):
    print('Коэффициенты для ' + y, np.round(res.x, 2))
    print('Коэффициент детерминации' + y, round(r2_score(dff[y], Mod), prec))


def getAll(y, dff, Model=Model_Z, regr=z_regr, num=7, prec=4, pos='lower right'):
    p0 = np.ones(num)
    x_data = [dff['Heading'], dff['Roll'], dff['Pitch']]
    res_lsq = least_squares(regr, p0, args=(x_data, dff[y]))
    Mod = Model(x_data, res_lsq.x)
    dff[y + '_comp'] = dff[y] - Mod.y
    print('Коэффициенты для ' + y, np.round(res_lsq.x, 2))
    print('Коэффициент детерминации ' + y, round(r2_score(dff[y], Mod.y), prec))
    setGraph_new('Compensation' + y, dff.index,
                 dff[y], dff[y + '_comp'], pos=pos)
    setPointGraph_new('Compensation' + y, dff['Heading'], dff[y], Mod.y)



path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'


df = pd.read_csv(path, sep=';')
df['Timestamp'] = df['Timestamp'] *(10**(-15))

# Удаление строк в которых аппарат ещё не движется
df_clean = df.drop(df.index[(df['VertForvUp'] == 0) & (df['VertForvDown'] == 0) &
                   (df['VertBackUp'] == 0) & (df['VertBackDown'] == 0)])
# или перемещается с использованием маневренных двигателей
df_clean = df_clean.drop(df.index[(df['VertForvUp'].abs() + df['VertForvDown'].abs()
                   + df['VertBackUp'].abs() + df['VertBackDown'].abs()) > 0.15])

df_clean['Bat50'] = df_clean['Bat1_50_I'] + df_clean['Bat2_50_I'] + \
                    df_clean['Bat3_50_I'] + df_clean['Bat4_50_I']


# Расчёт коэффициентов для фронтального датчика
# По оси X
getAll('Front_X', df_clean)

plt.show()
