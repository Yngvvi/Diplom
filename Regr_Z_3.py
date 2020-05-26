import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score


class Graph(object):
    def __init__(self, tittle, x_leb):
        self.sliders = []
        self.R2 = None
        self.fig = plt.figure(figsize=(6 * 3.13, 4 * 3.13))
        self.ax_sc = self.fig.add_subplot(2, 1, 1)
        self.ax_pl = self.fig.add_subplot(2, 1, 2)
        self.ax_sc.set_title(tittle[0])
        # self.ax_pl.set_title(tittle[1])
        self.ax_sc.set_xlabel(x_leb[0])
        self.ax_pl.set_xlabel(x_leb[1])
        self.ax_sc.grid()
        self.ax_pl.grid()

    def add_slider(self, obj, name, nominal, limits):
        ybot = 0.03 * (len(self.sliders) // 2 + 1)
        x_bot = 0.05 + 0.5 * ((2 + len(self.sliders)) % 2)
        ax_slider = plt.axes([x_bot, ybot, 0.36, 0.02])
        slider = Slider(ax_slider, name, limits[0], limits[1], valinit=nominal)

        def update(val):
            for i in range(len(self.sliders)):
                obj.args[i] = self.sliders[i].val
            Mod = obj.model(obj.x, obj.args)

            self.R2 = round(r2_score(self.y_sc_fon, Mod), 2)
            plt.title(self.R2, position=(0.2, 0.75))

            xx = np.vstack((self.x_sc, Mod))
            self.graph_sc.set_offsets(xx.T)
            self.graph_pl.set_ydata(self.y_fon - Mod)
            self.fig.canvas.draw_idle()

        slider.on_changed(update)
        self.sliders.append(slider)
        return slider

    def reset(self, event):
        for slider in self.sliders:
            slider.reset()

    def eject(self, event):
        print('R2 =', self.R2)
        for slider in self.sliders:
            print(round(slider.val, 2), end=', ')
        print()

    def auto_slider(self, obj, num, name):
        for i in range(num):
            if obj.args[i] == 0:
                bot = -100
                top = 100
            if abs(obj.args[i]) <= 1:
                  top = 10
                  bot = -10

            else:
                if 1 < abs(obj.args[i]) <= 50:
                    de = 10
                elif 50 < abs(obj.args[i]) <= 1000:
                    de = 5
                elif 1000 < abs(obj.args[i]) <= 10000:
                    de = 3
                elif abs(obj.args[i]) > 10000:
                    de = 2
                top = de * obj.args[i]
                bot = obj.args[i] - top
            if bot < top:
                self.add_slider(obj, name + str(i), obj.args[i], (bot, top))
            else:
                self.add_slider(obj, name + str(i), obj.args[i], (top, bot))

    def plot_sc(self, x, y_fon, y_var, s=1, y_dop=None):
        if y_dop is None:
            y_dop = []
        self.y_sc_fon = y_fon
        self.x_sc = x
        y_lebels = [y_fon.name, y_var.name]
        self.ax_sc.scatter(x, y_fon, s=s)
        self.graph_sc = self.ax_sc.scatter(x, y_var, s=s)
        if len(y_dop) != 0:
            for y_d in y_dop:
                self.ax_pl.scatter(x, y_d, s=s)
                y_lebels.append(y_d.name)
        plt.subplots_adjust(left=0.2)
        self.ax_sc.legend(y_lebels, loc='upper right')

    def plot_pl(self, x, y_fon, y_var, y_dop=None):
        if y_dop is None:
            y_dop = []
        self.y_fon = y_fon
        y_lebels = [y_fon.name, y_var.name]
        # self.ax_pl.plot(x, y_fon) #Для графиков с большым смещением
        self.graph_pl, = self.ax_pl.plot(x, y_var)
        if len(y_dop) != 0:
            for y_d in y_dop:
                self.ax_pl.plot(x, y_d)
                y_lebels.append(y_d.name)
        y_bot = 0.022 * (len(self.sliders) + 0)
        plt.subplots_adjust(left=0.2, bottom=y_bot)
        self.ax_pl.legend(y_lebels, loc='upper right')
        # Кнопка Reset
        resetax = plt.axes([0.05, 0.55, 0.1, 0.04])
        button = Button(resetax, 'Reset')
        button.on_clicked(self.reset)
        # Кнопка Print
        eject = plt.axes([0.05, 0.75, 0.1, 0.04])
        button2 = Button(eject, 'Print')
        button2.on_clicked(self.eject)

        plt.show()


class Model(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]*args[2]) + args[3]*np.sin(x[0]*args[4])
        Mod = Mod + +args[5]*np.sin(x[0]*args[6])**2
        Mod = Mod + args[7]*np.sin(x[0]*args[8])
        Mod = Mod + args[9]* x[1] + args[10]* x[2]

        # Компенсация маршевых двигателей
        # Mod = Mod + args[3]*x[2]*np.abs(np.cos(x[0]))*np.sin(x[0]/2)
        # Mod = Mod + args[4]*x[3]*np.sin(x[0]/2)
        # # # Компенсация работы батарей 50В
        # Mod = Mod + args[5]*(x[4] - args[6])*np.sin(x[0]/2)
        # # # Компенсация угла дифферента
        # Mod = Mod + args[7] * x[5]
        return Mod


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']

# p_front = [-32036.87, -1170.44, 1.0, -697.0, 2.0, 1434.76, 2.0, -282.64, 0.69, -901.41]

p_front = [-32341.58, -1193.28, 1, -767.25, 2, 1203.61, 2,  -221.68, 0.81, 562.73, 4792.14]
# St 1
# -31726.0, -1298.33, 1.06, -686.74, 2.04, 524.09, 2.11, -2648.0, 0.02, 264.94, -2.83, -723.22,
# st 2 0.61
# -31726.0, -1646.73, 1.06, 35.01, 6.38, 524.09, 2.11, -2648.0, 0.02, 559.68, -2.83, -723.22,

# 0.48 Но попадает в горб
# -31726.0, -1860.28, 1.06, -399.44, 2.46, 524.09, 2.11, -2648.0, 0.02, 264.94, -2.83, -723.22

# -32179.47, -1228.65, 1.03, -13.47, 2.46, 146.0, 2.11, 2635.07, 0.02, 264.94, -2.83, -723.22,
# -31726.0, -1860.28, 1.06, -399.44, 2.46, 524.09, 2.11, -529.6, 0.67, 256.3, -4.32, -723.22
# p_front = [-31726, -2000]
# -31726.0, -1170.44, 1.0, -697.0, 2.0, 827.0, 2.0, -407.0, 0.69, -166.0, 0, -901.41
# -31726.0, -1608.0, 1.0, -697.0, 2.0, 827.0, 2.0, -407.0, 0.69, -166.0, 0, -2000
Mod1 = Model([df['Heading'], df['Pitch'], df['Roll']], p_front)
df['Z_Front_comp'] = df['Front_Z'] - Mod1.y

# -31726.0, -1860.28, 1.06, -702.9, 2.46, 1135.39, 2.11, -303.51, 0.67, 385.9, -4.32, -723.22,

Gr = Graph(['Front_Z', 'Test'], ['Heading','Index'])
# Gr.add_slider(Mod1, 'a0', Mod1.args[0],(-45000, -15000))
# Gr.add_slider(Mod1, 'a1', Mod1.args[1],(-2000, 0))

Gr.auto_slider(Mod1, 11, 'a')

Gr.plot_sc(df['Heading'], df['Front_Z'], Mod1.y, )
Gr.plot_pl(df.index, df['Front_Z'], df['Z_Front_comp'], )
