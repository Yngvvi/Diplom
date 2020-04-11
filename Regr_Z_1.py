import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from Utilities import setGraph, setPointGraph


def Model(x, a, b, d, e, f, g, h, i, j, k, m, n, p, s):
# def Model(x, a, b, d, e, f, g, h):
#     y = a + b*np.cos(x) + d*np.sin(2*x) + e*np.sin(2*x)**2
    # y = a + b*np.cos(x) + d*np.sin(2*x) + e*np.sin(2*x)**2 + f*np.sin(x) + g*np.cos(3*x) + h*np.cos(x/3) # 0.60
    # y = a + b*x + d*x**2 + e*x**3+f*x**4+g*x**5+h*x**6+i*x**7 # 0.48
    # y = a + b*np.cos(x)+d*np.cos(x)**2+e*np.cos(x)**3+f*np.cos(x)**4+g*np.cos(x)**5+h*np.cos(x)**6 # 0.54 но медленно
    # y = a + b*np.cos(x)+d*np.sin(x)+e*np.cos(3*x)+f*np.cos(x/3)+g*np.sin(x)**2+h*np.sin(x)**6+i*np.sin(2*x)**3+\
    #     j*np.sin(2*x)**4 # 0.62
    return y


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')
length = df.shape[0]
x_data, y_data = (df['Heading'].values, df['Front_Z'].values)

# popt, pcov= curve_fit(Model, x_data, y_data)

# popt = [-31970.3, -1310.8, -582.5, 1040.6, -93.5, 238.9, -170.2]
# [-32000 -1070 -701 1106]
# Mod1 = Model(df['Heading'], *popt)
# df['Z_Front_comp'] = df['Front_Z'] - Mod1
# Mod1 = -31700 - 1600*np.cos(df['Heading']) - 1000*np.sin(2*df['Heading']) + 800*np.sin(2*df['Heading'])**2 #0.63

fig, ax = plt.subplots()

a0 = -31700

Mod1 = a0 - 1600 * np.cos(df['Heading']) - 500 * np.sin(2 * df['Heading']) + 800 * np.sin(2 * df['Heading']) ** 2
df['Z_Front_comp'] = df['Front_Z'] - Mod1

a_sl = plt.axes()
sl_a = Slider(a_sl, 'a', -35000, -25000, valinit=a0)

def update(val):
    a = sl_a.val
    Mod1 = a0 - 1600 * np.cos(df['Heading']) - 500 * np.sin(2 * df['Heading']) + 800 * np.sin(2 * df['Heading']) ** 2
    ax.set_ydata(Mod1)
    fig.canvas.draw_idle()

sl_a.on_changed(update)
# print('Параметры: ', popt)
# print("R2-score curve_fit: %.2f" % r2_score(Mod1, df['Front_Z']) )

# Точечный график
# setPointGraph(min(df['Heading']), max(df['Heading']), ['Front_Z', 'Z_Front_comp'],
#               'Heading', 'Model', df['Heading'], df['Front_Z'], Mod1)


# Линейный график
# setGraph(0, length, ['Front_Z', 'Z_Front_comp',], 'Index', 'Front_Z',
#          df.index, df['Front_Z'], df['Z_Front_comp'])

# setGraph(0, length, ['Z_Front_comp'], 'Index', 'Front_Z',
#          df.index, df['Z_Front_comp'])




ax.scatter(df['Heading'], df['Front_Z'], s=1)
ax.scatter(df['Heading'], Mod1, s=1)
ax.set_xlabel('Heading')
ax.legend(['Front_Z', 'Z_Front_comp'], loc='upper right')
ax.grid()


plt.show()
