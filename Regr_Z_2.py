import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score
from Utilities import setGraph, setPointGraph


def update(val):
    a0 = sl_a.val
    Mod1 = a0 - 1600*np.cos(df['Heading'])
    # graph.set_ydata
    xx = np.vstack((df['Heading'], Mod1))
    graph.set_offsets(xx.T)
    fig.canvas.draw_idle()


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

fig, ax = plt.subplots()
# plt.subplots_adjust(left=0.25, bottom=0.25)
a0 = -31700

Mod1 = a0 - 1600*np.cos(df['Heading'])
# graph, = plt.plot(df.index, Mod1, lw=2)
graph = plt.scatter(df['Heading'], Mod1, s=1)
graph2 = ax.scatter(df['Heading'], df['Front_Z'], s=1)

# Mod1 = a0 - 1600 * np.cos(df['Heading']) - 500 * np.sin(2 * df['Heading']) + 800 * np.sin(2 * df['Heading']) ** 2
# df['Z_Front_comp'] = df['Front_Z'] - Mod1

a_sl = plt.axes([0.15, 0.02, 0.4, 0.03])
sl_a = Slider(a_sl, 'a0', -35000, -25000, valinit=a0)

sl_a.on_changed(update)

# ax.set_xlabel('Heading')
# ax.legend(['Front_Z', 'Z_Front_comp'], loc='upper right')
ax.grid()

resetax = plt.axes([0.85, 0.02, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    sl_a.reset()

button.on_clicked(reset)

plt.show()
