import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score

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

    def plotme(self, x, y_fon, y_var):
        self.y_fon = y_fon
        self.ax.plot(x, y_fon)
        self.graph, = self.ax.plot(x, y_var)
        y_bot = 0.03 * (len(self.sliders) + 3)
        plt.subplots_adjust(left=0.2, bottom=y_bot)
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
        Mod = args[0] + args[1]*np.cos(x) + args[2]*np.sin(x)
        return Mod


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

Mod1 = Model(df['Heading'], [-2400, 16500, 2000])
df['Y_Front_comp'] = df['Front_Y'] - Mod1.y

Gr = LinGraph('Test', 'Index')

Gr.add_slider(Mod1, 'a0', Mod1.args[0],(-5000, 1000))
Gr.add_slider(Mod1, 'b0', Mod1.args[1],(10000, 20000))
Gr.add_slider(Mod1, 'c0', Mod1.args[2],(1000, 3000))


Gr.plotme(df.index, df['Front_Y'], df['Y_Front_comp'])


