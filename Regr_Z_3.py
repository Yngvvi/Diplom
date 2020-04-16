import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score


class Plot(object):
    def __init__(self, name):
        self.name = name
        self.sliders = []
        self.fig = plt.figure()

    def sliderfunc(self):
        for (obj, P) in self.OPs:
            P.set_offsets(obj.xy.T)
        self.fig.canvas.draw_idle()

    def add_slider(self, obj, method, nominal, limits):
        ybot = 0.03 * (len(self.sliders) + 1)
        name = obj.name + '.' + method
        ax_slider = plt.axes([0.25, ybot, 0.50, 0.02], facecolor="w")
        slider = Slider(ax_slider, name, limits[0], limits[1], valinit=nominal)

        def callback(val):
            getattr(obj, method)(val)
            self.sliderfunc()

        slider.on_changed(callback)
        self.sliders.append(slider)
        return slider

    def plotme(self, objs):
        ybot = 0.03 * (len(self.sliders) + 3)
        A = plt.axes([0.15, ybot, 0.65, 0.50])
        self.OPs = []
        for obj in objs:
            P = A.scatter(obj.x, obj.y)
            self.OPs.append((obj, P))
        plt.show()


class Data(object):
    def __init__(self, x, *args):
        self.args = args
        self.x = x
        self.update()

    def update(self):
        self.y = self.args[0] + self.args[0] * np.cos(self.x)
        self.xy = np.vstack((self.x, self.y))


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')



