import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from Utilities import setGraph, setPointGraph


def Model(x, a, b, d, e, f, g, h):
    y = a + b*np.cos(x) + d*np.sin(2*x) + e*np.sin(2*x)**2 + f*np.sin(x)
    y = y + g*np.cos(3*x) + h*np.cos(x/3)
    return y


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')
length = df.shape[0]
x_data, y_data = (df['Heading'].values, df['Front_Z'].values)

popt, pcov= curve_fit(Model, x_data, y_data)

Mod1 = Model(df['Heading'], *popt)
df['Z_Front_comp'] = df['Front_Z'] - Mod1


print('Параметры: ', popt)
print("R2-score curve_fit: %.2f" % r2_score(Mod1, df['Front_Z']) )

# Точечный график
setPointGraph(min(df['Heading']), max(df['Heading']), ['Front_Z', 'Z_Front_comp'],
              'Heading', 'Model', df['Heading'], df['Front_Z'], Mod1)


# Линейный график
# setGraph(0, length, ['Front_Z', 'Z_Front_comp',], 'Index', 'Front_Z',
#          df.index, df['Front_Z'], df['Z_Front_comp'])

plt.show()
