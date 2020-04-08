import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import curve_fit
from Utilities import setGraph


def Model(x, x_front_head_amp):
    y = x_front_head_amp*np.sin(x)
    return y

path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

x_front_head_amp2 = -16500

length = df.shape[0]


x_data, y_data = (df['Heading'].values, df['Front_X'].values)
popt, pcov= curve_fit(Model, x_data, y_data)
x_front_head_amp  = popt[0]

print(popt)
df['X_Front_comp'] = df['Front_X'] - Model(df['Heading'], x_front_head_amp)
df['X_Front_comp2'] = df['Front_X'] - x_front_head_amp2*np.sin(df['Heading'])


# Точечный график
fig, ax = plt.subplots()
ax.scatter(df['Heading'], df['Front_X'], s=1)
ax.scatter(df['Heading'], Model(x_data, x_front_head_amp), s=1)
ax.set_ylabel('Front_X')
ax.set_xlabel('Heading')
ax.grid()


fig, ax = plt.subplots()
ax.set_xlim(0, length)

ax.plot(df.index, df['Front_X'])
ax.plot(df.index, df['X_Front_comp'])
ax.plot(df.index, df['X_Front_comp2'], ':')

ax.set_title('Model')
ax.set_xlabel('Index')
ax.legend(['Front_X', 'X_Front_comp', 'X_Front_comp2'], loc='lower right')
ax.grid()

# setGraph(0, length, ['Front_X', 'X_Front_comp', 'X_Front_comp2'], 'Index', 'Front_X',
#          df.index, df['Front_X'], df['X_Front_comp'], df['X_Front_comp2'])


plt.show()
