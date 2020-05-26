import pandas as pd
import numpy as np  # Нужен для cos и sin на столбец
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from sklearn.metrics import r2_score
from Classaes import LinGraph, PlotGraph, Graph
from Utilities import setPointGraph_new, setGraph_new
from Models import Model


def siple_regr_mod(args, x, y):
    # Компенсация курса и крена
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
    # Компенсация угла дифферента
    Mod = Mod + args[4] * x[2]
    return Mod - y


def getP(res, num=9):
    popt = np.zeros(num)
    popt[:4] = res[:4]
    popt[-1] = res[-1]
    return popt


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_R'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5

# df['Back_res'] = (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5

# p_front = [1460, -16570, -1160, -12, -11, 85, 13, 26207]
# p_back = [2700, -16420, 2110, -58, -19, -80, -56, 28220]

p_front = [37000, -1000, 1000]


# Регрессия
p0 = np.ones(5)
x_data = [df['Heading'], df['Roll'], df['M_UP'], df['M_Right'], df['Bat50'], df['Pitch']]
res_lsq = least_squares(siple_regr_mod, p0, args=([df['Heading'], df['Roll'], df['Pitch']], df['Front_R']))
popt= getP(res_lsq.x)
Mod_R = Model(x_data, popt)
df['Front_R_comp'] = df['Front_R'] - Mod_R.y

# setGraph_new('Compensation', df.index, df['Front_R'], df['Front_R_comp'], pos='lower right')
# setPointGraph_new('Compensation', df['Heading'], df['Front_R'], Mod_R.y)
# plt.show()

print('Коэффициенты для фронтального датчика по оси х:', np.round(res_lsq.x, 2))
print('Коэффициент детерминации', round(r2_score(df['Front_R'], Mod_R.y), 4))




Gr = LinGraph('Test', 'Index')
Gr.auto_slider(Mod_R, 9, 'a')
Gr.plot_one(df.index, df['Front_R'], df['Front_R_comp'])



'''
36160.0, -249.0, -568.0, -458.0, -1.0, 4.0, -21.0, -7.0, 1152.0, 
36215.0, -256.0, -568.0, -665.0, -0.0, 7.0, -21.0, -13.0, 1152.0, 
36215.0, -256.0, -539.0, -651.0, -2.0, 7.0, -22.0, -11.0, 1152.0, 
'''