import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score
from scipy.optimize import least_squares

class LinGraph(object):
    def __init__(self, tittle, x_leb):
        self.sliders = []
        self.fig, self.ax = plt.subplots()
        plt.title(tittle)
        plt.xlabel(x_leb)
        plt.grid()

    def add_slider(self, obj, name, nominal, limits):
        ybot = 0.03 * (len(self.sliders)//2 + 1)
        x_bot = 0.05 + 0.5*((2 + len(self.sliders))%2)
        ax_slider = plt.axes([x_bot, ybot, 0.36, 0.02])
        slider = Slider(ax_slider, name, limits[0], limits[1], valinit=nominal)

        def update(val):
            for i in range(len(self.sliders)):
                obj.args[i] = self.sliders[i].val
            Mod = obj.model(obj.x, obj.args)
            self.graph.set_ydata(self.y_fon - Mod)
            self.fig.canvas.draw_idle()

        slider.on_changed(update)
        self.sliders.append(slider)
        return slider

    def reset(self, event):
        for slider in self.sliders:
            slider.reset()

    def plotme(self, x, y_fon, y_var, y_dop=None):
        if y_dop is None:
            y_dop = []
        self.y_fon = y_fon
        y_lebels = [y_fon.name, y_var.name]
        self.ax.plot(x, y_fon)
        self.graph, = self.ax.plot(x, y_var)
        if len(y_dop) != 0:
            for y_d in y_dop:
                self.ax.plot(x, y_d)
                y_lebels.append(y_d.name)

        y_bot = 0.03 * (len(self.sliders) + 3)
        plt.subplots_adjust(left=0.2, bottom=y_bot)
        self.ax.legend(y_lebels, loc='upper right')
        # Кнопка Reset
        resetax = plt.axes([0.05, 0.55, 0.1, 0.04])
        button = Button(resetax, 'Reset')
        button.on_clicked(self.reset)
        plt.show()


class Model(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]) + args[2]*np.sin(x[0]) + args[3]*x[1]
        # Компенсация маршевых двигателей
        # Mod = Mod + args[4]*x[2]*(abs(np.cos(x[0]))*np.sin(x[0]/2))
        Mod = Mod + args[4]*x[2] * (np.abs(np.sin(x[0])) - args[5]*np.cos(x[0]))
        return Mod

    def simple(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
        # Компенсация маршевых двигателей
        Mod = Mod + args[4]*x[2]*(abs(np.cos(x[0]))*np.sin(x[0]/2))
        return Mod

    def regr(self, args, x, y):
        Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
        Mod = Mod + args[4] * x[2] * (np.abs(np.sin(x[0])) - args[5] * np.cos(x[0]))
        return Mod - y


def regr(args, x, y):
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
    Mod = Mod + args[4] * x[2] * (np.abs(np.sin(x[0])) - args[5] * np.cos(x[0]))
    return Mod - y

path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

popt = [-3575, 16390, 1750, 17930, 3, 1]
p0 = np.ones(6)
res_lsq = least_squares(regr, p0, args=([df['Heading'], df['Roll'], df['M_UP']], df['Front_Y']))

# popt, pcov= curve_fit(Model.model, df['Heading'], df['Front_Y'])

# M = Model.model()
print(res_lsq.x)

Mod1 = Model([df['Heading'], df['Roll'], df['M_UP']], res_lsq.x)

df['Y_Front_comp'] = df['Front_Y'] - Mod1.y
df['Y_Front_comp2'] = df['Front_Y'] - Mod1.simple([df['Heading'], df['Roll'], df['M_UP']], [-3575, 16390, 1750, 17930, 3])

Gr = LinGraph('Test', 'Index')

Gr.add_slider(Mod1, 'a0', Mod1.args[0],(-5000, 1000))
Gr.add_slider(Mod1, 'a1', Mod1.args[1],(10000, 20000))
Gr.add_slider(Mod1, 'a2', Mod1.args[2],(1000, 3000))
Gr.add_slider(Mod1, 'a3', Mod1.args[3],(15000, 30000))
Gr.add_slider(Mod1, 'a4', Mod1.args[4],(0, 30))
Gr.add_slider(Mod1, 'a5', Mod1.args[5],(-10, 20))

Gr.plotme(df.index, df['Front_Y'], df['Y_Front_comp'], [df['Y_Front_comp2']])

