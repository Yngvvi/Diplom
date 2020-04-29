import pandas as pd
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import least_squares
from Classaes import LinGraph, Graph, PlotGraph
from Models import Model


def siple_regr_mod(args, x, y):
    # Компенсация курса и крена
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
    # Компенсация угла дифферента
    Mod = Mod + args[4] * x[2]
    return Mod - y


# Если сразу использовать p0 длиной 9 появляется огромное a4, которое портит модель
def getP(res, num=9):
    popt = np.zeros(num)
    popt[:4] = res[:4]
    popt[-1] = res[-1]
    return popt


# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
path = 'src/stz_R_emi_nakoplenie_1573455126581000.csv'

df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']

# Для path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
# p_front = [1460, 0, -16570, -1160, -12, -11, 85, 13, 26207]
# p_back = [2700, 0, -16420, 2110, -58, -19, -80, -56, 28220]

# Для 'src/stz_R_emi_nakoplenie_1573455126581000.csv'
p_front = [1590, 1312.0, -16504.0, -10497, -11.0, -2.0, 12.0, -19.0, 30034.0]
p_back = [-1432, 4906, -16252, 4877, 6.0, -30.0, -50.0, 28.0, 28915.0, ]

p0 = np.ones(5)
x_data = [df['Heading'], df['Roll'], df['M_UP'], df['M_Right'], df['Bat50'], df['Pitch']]

# # Предварительный расчёт коэффициентов для фронтального датчика
# res_lsq_front = least_squares(siple_regr_mod, p0, args=([df['Heading'], df['Roll'], df['Pitch']], df['Front_X']))
# popt_front = getP(res_lsq_front.x)
# Mod1 = Model(x_data, popt_front)
# df['X_Front_comp'] = df['Front_X'] - Mod1.y
#
# print('Полученные коэффициенты:', np.round(res_lsq_front.x, 2))

# Компенсация фронтального датчика
Mod2 = Model(x_data, p_front)
df['X_Front_comp2'] = df['Front_X'] - Mod2.y

# Предварительный расчёт коэффициентов для кормового датчика
res_lsq_back = least_squares(siple_regr_mod, p0, args=([df['Heading'], df['Roll'], df['Pitch']], df['Back_X']))
popt_back = getP(res_lsq_back.x)
Mod3 = Model(x_data, popt_back)
df['X_Back_comp'] = df['Back_X'] - Mod3.y

print('Полученные коэффициенты:', np.round(res_lsq_back.x, 2))

# Компенсация кормового датчика
Mod4 = Model(x_data, p_back)
df['X_Back_comp2'] = df['Back_X'] - Mod4.y

Gr = LinGraph('Test', 'Index')

# Для фронтального датчика

# Gr.auto_slider(Mod2, 9, 'a')
# Gr.plotme(df.index, df['Front_X'], df['X_Front_comp2'], [df['X_Front_comp']], pos='lower right')

# Для одновременного отображения графиков

# Gr1 = Graph(['Front_X', 'Test'], ['Heading','Index'])
# Gr1.auto_slider(Mod2, 9, 'a')
# Gr1.plot_sc(df['Heading'], df['Front_X'], Mod2.y, )
# Gr1.plot_pl(df.index, df['Front_X'], df['X_Front_comp'], pos='lower right')

# Для кормового датчика

Gr.auto_slider(Mod4, 9, 'a')
Gr.plotme(df.index, df['Back_X'], df['X_Back_comp2'], [df['X_Back_comp']], pos='lower right')

