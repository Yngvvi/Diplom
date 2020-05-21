import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from Utilities import setGraph, setPointGraph
from sklearn.metrics import r2_score

# Работает медленно - запускать осторожно!


def model(args, x, y):
    # Компенсация курса и крена
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
    # Компенсация маршевых двигателей
    Mod = Mod + args[4] * x[2] * np.abs(np.cos(x[0])) * np.sin(x[0] / 2)
    Mod = Mod + args[5] * x[3] * abs(np.sin(x[0] / 2))
    # Компенсация работы батарей 50В
    Mod = Mod + args[6] * (x[4] - args[7]) * np.sin(x[0] / 2)
    # Компенсация угла дифферента
    Mod = Mod + args[8] * x[5]
    return Mod - y


def Model(x, args):
    # Компенсация курса и крена
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
    # Компенсация маршевых двигателей
    Mod = Mod + args[4] * x[2] * np.abs(np.cos(x[0])) * np.sin(x[0] / 2)
    Mod = Mod + args[5] * x[3] * abs(np.sin(x[0] / 2))
    # Компенсация работы батарей 50В
    Mod = Mod + args[6] * (x[4] - args[7]) * np.sin(x[0] / 2)
    # Компенсация угла дифферента
    Mod = Mod + args[8] * x[5]
    return Mod


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'

df = pd.read_csv(path, sep=';')
length = df.shape[0]
df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']

x_data = [df['Heading'], df['Roll'], df['M_Right'], df['M_Right'], df['Bat50'], df['Pitch']]

p0 = np.ones(9)
res_lsq = least_squares(model, p0, args=(x_data, df['Front_Y']))
Mod1 = Model(x_data, res_lsq.x)

p_front = [-3575, 16240, 1750, 17930, 3, -2, 5, -15, 500]
p_front_2 = [-3228.21, 16116.8, 1369.44, 11300.11, 0, 0, 0, 0, 2798.97]

# Ручная подборка
Mod2 = Model(x_data, p_front)
# Упрощенная модель
Mod3 = Model(x_data, p_front_2)

df['Y_Front_comp'] = df['Front_Y'] - Mod1
df['Y_Front_comp2'] = df['Front_Y'] - Mod2
df['Y_Front_comp3'] = df['Front_Y'] - Mod3

print('Параметры least_squares: ', res_lsq.x)
print("R2-score least_squares: %.2f" % r2_score( df['Front_Y'], Mod1))
print("R2-score hand: %.2f" % r2_score( df['Front_Y'], Mod2))
print("R2-score light: %.2f" % r2_score( df['Front_Y'], Mod3))

# Точечный график
setPointGraph(min(df['Heading']), max(df['Heading']), ['Front_Y', 'Y_Front_comp'],
              'Heading', 'Model', df['Heading'], df['Front_Y'], Mod1)
# Линейный график
setGraph(0, length, ['Front_Y', 'Регрессия', 'Ручная', 'Light model'], 'Index', 'Front_Y',
         df.index, df['Front_Y'], df['Y_Front_comp'],  df['Y_Front_comp2'], df['Y_Front_comp3'])

plt.show()
