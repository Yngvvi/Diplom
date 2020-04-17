import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import curve_fit, least_squares
from sklearn.metrics import r2_score
from Utilities import setGraph, setPointGraph


def Model(x1, x2, p):
    y = p[0] + p[1]*np.cos(x1) + p[2]*np.sin(x1) + p[3]*x2
    return y


# def Model_sq(p, x1, x2, y):
#     funq = p[0] + p[1]*np.cos(x1) + p[2]*np.sin(x1) + p[3]*x2
#     return funq - y


def Model_sq(p, x, y):
    funq = p[0] + p[1]*np.cos(x[0]) + p[2]*np.sin(x[0]) + p[3]*x[1]
    return funq - y


def Simple_model(x, b, k, a):
    y = b + k*np.cos(x) + a*np.sin(x)
    return y


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')
length = df.shape[0]

x1_data, x2_data, y_data = (df['Heading'].values, df['Roll'].values, df['Front_Y'].values)

popt, pcov= curve_fit(Simple_model, x1_data, y_data)

p0 = np.ones(4)
res_lsq = least_squares(Model_sq, p0, args=([x1_data, x2_data], y_data))

Mod2 = Simple_model(df['Heading'], *popt)
df['Y_Front_comp2'] = df['Front_Y'] - Mod2

print('Параметры curve_fit :', popt)
print("R2-score curve_fit: %.2f" % r2_score(Mod2, df['Front_Y']))


Mod1 = Model(x1_data, x2_data, res_lsq.x)
df['Y_Front_comp'] = df['Front_Y'] - Mod1

print('Параметры least_squares: ', res_lsq.x)
print("R2-score least_squares: %.2f" % r2_score(Mod1, df['Front_Y']))

# Точечный график
setPointGraph(min(df['Heading']), max(df['Heading']), ['Front_Y', 'Y_Front_comp'],
              'Heading', 'Model', df['Heading'], df['Front_Y'], Mod1)
# Линейный график
setGraph(0, length, ['Front_Y', 'Y_Front_comp1', 'Y_Front_comp2'], 'Index', 'Front_Y',
         df.index, df['Front_Y'], df['Y_Front_comp'], df['Y_Front_comp2'])

plt.show()
