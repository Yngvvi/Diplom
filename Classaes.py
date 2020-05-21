import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
from sklearn.metrics import r2_score


# Для построения линейных графиков (plot)
class LinGraph(object):
    def __init__(self, tittle, x_leb):
        self.sliders = []
        self.fig, self.ax = plt.subplots(figsize=(6 * 3.13, 4 * 3.13))
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
            self.R2 = round(r2_score(self.y_fon, Mod), 2)
            plt.title(self.R2, position=(0.2, 0.75))

        slider.on_changed(update)
        self.sliders.append(slider)
        return slider

    def reset(self, event):
        for slider in self.sliders:
            slider.reset()

    def eject(self, event):
        for slider in self.sliders:
            print(round(slider.val, 0), end=', ')
        print()

    def auto_slider(self, obj, num, name):
        for i in range(num):
            if obj.args[i] == 0:
                bot = -100
                top = 100
            else:
                if abs(obj.args[i]) <= 50:
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

    def plotme(self, x, y_fon, y_var, y_dop=None, pos='upper right'):
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
        y_bot = 0.024 * (len(self.sliders) + 0)
        plt.subplots_adjust(left=0.2, bottom=y_bot)
        self.ax.legend(y_lebels, loc=pos)
        # Кнопка Reset
        resetax = plt.axes([0.05, 0.55, 0.1, 0.04])
        button = Button(resetax, 'Reset')
        button.on_clicked(self.reset)
        # Кнопка Print
        eject = plt.axes([0.05, 0.75, 0.1, 0.04])
        button2 = Button(eject, 'Print')
        button2.on_clicked(self.eject)

        plt.show()

    def plot_one(self, x, y_fon, y_var, pos='upper right'):
        self.y_fon = y_fon
        self.graph, = self.ax.plot(x, y_var)
        y_bot = 0.024 * (len(self.sliders) + 0)
        plt.subplots_adjust(left=0.2, bottom=y_bot)
        self.ax.legend(y_var.name, loc=pos)
        # Кнопка Reset
        resetax = plt.axes([0.05, 0.55, 0.1, 0.04])
        button = Button(resetax, 'Reset')
        button.on_clicked(self.reset)
        # Кнопка Print
        eject = plt.axes([0.05, 0.75, 0.1, 0.04])
        button2 = Button(eject, 'Print')
        button2.on_clicked(self.eject)

        plt.show()



# Для построения точечных графиков (scatter)
class PlotGraph(object):
    def __init__(self, tittle, x_leb):
        self.R2 = None
        self.sliders = []
        self.fig, self.ax = plt.subplots(figsize=(6 * 3.13, 4 * 3.13))
        plt.title(tittle)
        plt.xlabel(x_leb)
        plt.grid()

    def add_slider(self, obj, name, nominal, limits):
        ybot = 0.03 * (len(self.sliders) // 2 + 1)
        x_bot = 0.05 + 0.5 * ((2 + len(self.sliders)) % 2)
        ax_slider = plt.axes([x_bot, ybot, 0.36, 0.02])
        slider = Slider(ax_slider, name, limits[0], limits[1], valinit=nominal)

        def update(val):
            for i in range(len(self.sliders)):
                obj.args[i] = self.sliders[i].val
            Mod = obj.model(obj.x, obj.args)

            self.R2 = round(r2_score(self.y_fon, Mod), 2)
            plt.title(self.R2, position=(0.2, 0.75))

            xx = np.vstack((self.x_sc, Mod))
            self.graph.set_offsets(xx.T)
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
            print(round(slider.val, 0), end=', ')
        print()

    def auto_slider(self, obj, num, name):
        for i in range(num):
            if obj.args[i] == 0:
                bot = -100
                top = 100
            else:
                if abs(obj.args[i]) <= 50:
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

    def plotme(self, x, y_fon, y_var, s=1, y_dop=None, pos='upper right'):
        if y_dop is None:
            y_dop = []
        self.y_fon = y_fon
        self.x_sc = x
        y_lebels = [y_fon.name, y_var.name]
        self.ax.scatter(x, y_fon, s=s)
        self.graph = self.ax.scatter(x, y_var, s=s)
        if len(y_dop) != 0:
            for y_d in y_dop:
                self.ax.scatter(x, y_d, s=s)
                y_lebels.append(y_d.name)

        y_bot = 0.03 * (len(self.sliders) + 2)
        plt.subplots_adjust(left=0.2, bottom=y_bot)
        self.ax.legend(y_lebels, loc=pos)
        # Кнопка Reset
        resetax = plt.axes([0.05, 0.55, 0.1, 0.04])
        button = Button(resetax, 'Reset')
        button.on_clicked(self.reset)
        # Кнопка Print
        eject = plt.axes([0.05, 0.75, 0.1, 0.04])
        button2 = Button(eject, 'Print')
        button2.on_clicked(self.eject)

        plt.show()


# Для одновременного построения точечных и линейных графиков
class Graph(object):
    def __init__(self, tittle, x_leb):
        self.sliders = []
        self.R2 = None
        self.fig = plt.figure(figsize=(6 * 3.13, 4 * 3.13))
        self.ax_sc = self.fig.add_subplot(2, 1, 1)
        self.ax_pl = self.fig.add_subplot(2, 1, 2)
        self.ax_sc.set_title(tittle[0])
        self.ax_pl.set_title(tittle[1])
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
            print(round(slider.val, 0), end=', ')
        print()

    def auto_slider(self, obj, num, name):
        for i in range(num):
            if obj.args[i] == 0:
                bot = -100
                top = 100
            else:
                if abs(obj.args[i]) <= 50:
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

    def plot_sc(self, x, y_fon, y_var, s=1, y_dop=None, pos='upper right'):
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
        self.ax_sc.legend(y_lebels, loc=pos)

    def plot_pl(self, x, y_fon, y_var, y_dop=None, pos='upper right'):
        if y_dop is None:
            y_dop = []
        self.y_fon = y_fon
        y_lebels = [y_fon.name, y_var.name]
        self.ax_pl.plot(x, y_fon)
        self.graph_pl, = self.ax_pl.plot(x, y_var)
        if len(y_dop) != 0:
            for y_d in y_dop:
                self.ax_pl.plot(x, y_d)
                y_lebels.append(y_d.name)
        y_bot = 0.024 * (len(self.sliders) + 0)
        plt.subplots_adjust(left=0.2, bottom=y_bot)
        self.ax_pl.legend(y_lebels, loc=pos)
        # Кнопка Reset
        resetax = plt.axes([0.05, 0.55, 0.1, 0.04])
        button = Button(resetax, 'Reset')
        button.on_clicked(self.reset)
        # Кнопка Print
        eject = plt.axes([0.05, 0.75, 0.1, 0.04])
        button2 = Button(eject, 'Print')
        button2.on_clicked(self.eject)

        plt.show()

    def plot_pl_one(self, x, y_fon, y_var, pos='upper right'):
        self.y_fon = y_fon
        self.graph, = self.ax_pl.plot(x, y_var)
        y_bot = 0.024 * (len(self.sliders) + 0)
        plt.subplots_adjust(left=0.2, bottom=y_bot)
        self.ax_pl.legend(y_var.name, loc=pos)
        # Кнопка Reset
        resetax = plt.axes([0.05, 0.55, 0.1, 0.04])
        button = Button(resetax, 'Reset')
        button.on_clicked(self.reset)
        # Кнопка Print
        eject = plt.axes([0.05, 0.75, 0.1, 0.04])
        button2 = Button(eject, 'Print')
        button2.on_clicked(self.eject)

        plt.show()
