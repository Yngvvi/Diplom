import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np  # Нужен для cos и sin на столбец


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
        Mod = Mod + args[4]*x[2]*np.abs(np.cos(x[0]))*np.sin(x[0]/2)
        Mod = Mod + args[5]*x[3]*np.sin(x[0]/2)
        # Компенсация работы батарей 50В
        Mod = Mod + args[6]*(x[4] - args[7])*np.sin(x[0]/2)
        # Компенсация угла дифферента
        Mod = Mod + args[8] * x[5]
        return Mod

    def my_model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
        # Компенсация маршевых двигателей
        Mod = Mod + args[4] * x[2] * (np.abs(np.sin(x[0])) - np.cos(x[0]))
        Mod = Mod + x[3] * (args[5] * np.abs(np.sin(x[0])) + args[6] * np.cos(x[0]))
        # [-3575, 16240, 1750, 17930, 3, 2, 1]

    def simple(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
        # Компенсация маршевых двигателей
        Mod = Mod + args[4]*x[2]*(np.abs(np.sin(x[0])) - np.cos(x[0]))

        return Mod


def auto_slid(Model, graph, num, name):
    for i in range(num):
        bot = Model.args[i]//10
        top = 4*Model.args[i] + bot + 1
        if bot < top:
            graph.add_slider(Mod1, name + str(i), Mod1.args[i], (bot, top))
        else:
            graph.add_slider(Mod1, name + str(i), Mod1.args[i], (top, bot))


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']

p_front = [-3575, 16240, 1750, 17930, 3, -2, 5, -15, 500]
p_back = [-750, 15230, 4350, 4980, -3, -4, -25, -14, -4250]

# Компенсация фронтального датчика
Mod1 = Model([df['Heading'], df['Roll'], df['M_UP'], df['M_Right'], df['Bat50'], df['Pitch']], p_front)
df['Y_Front_comp'] = df['Front_Y'] - Mod1.y
df['Y_Front_comp2'] = df['Front_Y'] - Mod1.simple([df['Heading'], df['Roll'], df['M_UP']], [-3575, 16390, 1750, 17930, 3, 1])
# Компенсация кормового датчика
Mod2 = Model([df['Heading'], df['Roll'], df['M_UP'], df['M_Right'], df['Bat50'], df['Pitch']], p_back)
df['Y_Back_comp'] = df['Back_Y'] - Mod2.y

Gr = LinGraph('Test', 'Index')

# Для фронтального датчика

# Gr.add_slider(Mod1, 'a0', Mod1.args[0],(-5000, 1000))
# Gr.add_slider(Mod1, 'a1', Mod1.args[1],(-20000, 50000))
# Gr.add_slider(Mod1, 'a2', Mod1.args[2],(-5000, 10000))
# Gr.add_slider(Mod1, 'a3', Mod1.args[3],(-25000, 50000))
# Gr.add_slider(Mod1, 'a4', Mod1.args[4],(-100, 100))
# Gr.add_slider(Mod1, 'a5', Mod1.args[5],(-100, 100))
# Gr.add_slider(Mod1, 'a6', Mod1.args[6],(-100, 100))
# Gr.add_slider(Mod1, 'a7', Mod1.args[7],(-100, 100))
# Gr.add_slider(Mod1, 'a8', Mod1.args[8],(-10000, 10000))
#
# Gr.plotme(df.index, df['Front_Y'], df['Y_Front_comp'], )
#[df['Y_Front_comp2']]

# Для кормового датчика
Gr.add_slider(Mod2, 'a0', Mod2.args[0],(-5000, 1000))
Gr.add_slider(Mod2, 'a1', Mod2.args[1],(-20000, 50000))
Gr.add_slider(Mod2, 'a2', Mod2.args[2],(-5000, 10000))
Gr.add_slider(Mod2, 'a3', Mod2.args[3],(0, 20000))
Gr.add_slider(Mod2, 'a4', Mod2.args[4],(-100, 100))
Gr.add_slider(Mod2, 'a5', Mod2.args[5],(-100, 100))
Gr.add_slider(Mod2, 'a6', Mod2.args[6],(-100, 100))
Gr.add_slider(Mod2, 'a7', Mod2.args[7],(-100, 100))
Gr.add_slider(Mod2, 'a8', Mod2.args[8],(-10000, 0))

Gr.plotme(df.index, df['Back_Y'], df['Y_Back_comp'], )
