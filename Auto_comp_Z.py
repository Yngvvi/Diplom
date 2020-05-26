import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import least_squares
from sklearn.metrics import r2_score
from time import process_time  # Считает время работы
from Utilities import plotFig, scatFig, setPointGraph_new, setGraph_new

# Для подбора только Z функции


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
        Mod = Mod + args[5]* x[1]
        return Mod


def z_regr(args, x, y):
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0] * 2)
    Mod = Mod + args[3] * np.sin(x[0] * 2) ** 2
    Mod = Mod + args[4] * np.sin(0.81 * x[0])
    Mod = Mod + args[5] * x[1]
    return Mod - y


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
p0 = np.ones(6)
x_data = [df['Heading'], df['Pitch']]

res_lsq_front = least_squares(z_regr, p0, args=(x_data, df['Front_Z']))
Mod_front = Model_Z(x_data, res_lsq_front.x)
df['Z_Front_comp'] = df['Front_Z'] - Mod_front.y

prec = 4
print('Коэффициенты для фронтального датчика:', res_lsq_front.x)
print('Коэффициент детерминации', round(r2_score(df['Front_Z'], Mod_front.y), prec))

setPointGraph_new('Compensation', df['Heading'], df['Front_Z'], Mod_front.y)

plt.show()
