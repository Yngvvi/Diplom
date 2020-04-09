import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from Utilities import setGraph, setPointGraph


def Model(x, b,  k, a):
    y = b + k*np.cos(x) + a*np.sin(x)
    return y


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')
length = df.shape[0]
x_data, y_data = (df['Heading'].values, df['Front_Y'].values)

popt, pcov= curve_fit(Model, x_data, y_data)

Mod1 = Model(df['Heading'], *popt)
df['Y_Front_comp'] = df['Front_Y'] - Mod1

print('Параметры: ', popt)
print("R2-score curve_fit: %.2f" % r2_score(Mod1, df['Front_Y']) )

# Точечный график
setPointGraph(min(df['Heading']), max(df['Heading']), ['Front_Y', 'Y_Front_comp'],
              'Heading', 'Model', df['Heading'], df['Front_Y'], Mod1)
# Линейный график
setGraph(0, length, ['Front_Y', 'Y_Front_comp',], 'Index', 'Front_Y',
         df.index, df['Front_Y'], df['Y_Front_comp'])

plt.show()
