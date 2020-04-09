import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import curve_fit, least_squares
from sklearn.metrics import r2_score
from Utilities import setGraph, setPointGraph


def Model(x, x_front_head_amp):
    y = x_front_head_amp*np.sin(x)
    return y


def Model_sq(x_front_head_amp, x, y):
    return x_front_head_amp*np.sin(x) - y


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

x_front_head_amp1 = -16500
length = df.shape[0]

x_data, y_data = (df['Heading'].values, df['Front_X'].values)

popt, pcov= curve_fit(Model, x_data, y_data)
res_lsq = least_squares(Model_sq, 1, args=(x_data, y_data))

x_front_head_amp  = popt[0]
x_front_head_amp2  = res_lsq.x[0]

Mod1 = Model(df['Heading'], x_front_head_amp)
Mod2 = Model(df['Heading'], x_front_head_amp2)

df['X_Front_comp'] = df['Front_X'] - Mod1
df['X_Front_comp1'] = df['Front_X'] - x_front_head_amp1*np.sin(df['Heading'])
df['X_Front_comp2'] = df['Front_X'] - Mod2

print('x_front_head_amp curve_fit =', x_front_head_amp)
print('x_front_head_amp least_squares =', x_front_head_amp2)
print("R2-score curve_fit: %.2f" % r2_score(Mod1, df['Front_X']) )
print("R2-score least_squares: %.2f" % r2_score(Mod2, df['Front_X']))

# Точечный график
setPointGraph(min(df['Heading']), max(df['Heading']), ['Front_X', 'Model1', 'Model2'],
              'Heading', 'Model', df['Heading'], df['Front_X'], Mod1, Mod2)
# Линейный график
setGraph(0, length, ['Front_X', 'X_Front_comp', 'X_Front_comp1', 'X_Front_comp2'], 'Index', 'Front_X',
         df.index, df['Front_X'], df['X_Front_comp'], df['X_Front_comp1'], df['X_Front_comp2'])

plt.show()

