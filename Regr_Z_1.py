import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from Utilities import setGraph, setPointGraph


def Model(x, a, b, d, e, f, g, h, i, j, k, m, n, p, s):
    # y = a + b*np.cos(x) + d*np.sin(2*x) + e*np.sin(2*x)**2 + f*np.sin(x) + g*np.cos(3*x) + h*np.cos(x/3) # 0.60
    # y = a + b*x + d*x**2 + e*x**3+f*x**4+g*x**5+h*x**6+i*x**7 # 0.48
    # y = a + b*np.cos(x)+d*np.cos(x)**2+e*np.cos(x)**3+f*np.cos(x)**4+g*np.cos(x)**5+h*np.cos(x)**6 # 0.54 но медленно
    y = a + b*np.cos(x)+d*np.sin(x)+e*np.cos(3*x)+f*np.cos(x/3)+g*np.sin(x)**2+h*np.sin(x)**6+i*np.sin(2*x)**3+\
        j*np.sin(2*x)**4 # 0.62
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
