import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

# fig, ax = plt.subplots()
# plt.subplots_adjust(left=0.25, bottom=0.25)
# t = np.arange(0.0, 1.0, 0.001)
# a0 = 5
# f0 = 3
# delta_f = 5.0
# s = a0 * np.sin(2 * np.pi * f0 * t)
# l, = plt.plot(t, s, lw=2)
# ax.margins(x=0)
#
# axcolor = 'lightgoldenrodyellow'
# axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
# axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
#
# sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0, valstep=delta_f)
# samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)
#
# def update(val):
#     amp = samp.val
#     freq = sfreq.val
#     l.set_ydata(amp*np.sin(2*np.pi*freq*t))
#     fig.canvas.draw_idle()
#
# sfreq.on_changed(update)
# samp.on_changed(update)
#
# resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
# button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
#
# def reset(event):
#     sfreq.reset()
#     samp.reset()
# button.on_clicked(reset)
#
# plt.show()
#

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
        ax_slider   = plt.axes([0.25, ybot, 0.50, 0.02], facecolor="w")
        slider      = Slider(ax_slider, name, limits[0], limits[1],
                             valinit=nominal)

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
    def __init__(self, name, x0, y0):
        self.name = name
        self.a = 1.0
        self.p = 1.0
        self.x0, self.y0 = x0, y0
        self.update()

    def update(self):
        self.x = self.a * self.x0
        self.y = self.y0**self.p
        self.xy = np.vstack((self.x, self.y))

    def set_a(self, val):
        self.a = val
        self.update()

    def set_p(self, val):
        self.p = val
        self.update()


x0 = np.linspace(0, 10., 11)
y1, y2 = [0.5 * (1.0 + f(x0)) for f in (np.cos, np.sin)]

d1, d2 = Data('hey', x0, y1), Data('wow', x0, y2) # data generating objects

p = Plot('hey')    # plot object

p.add_slider(d1, 'set_a', d1.a, (0.2, 1.0))
p.add_slider(d1, 'set_p', d1.p, (0.5, 2.0))
p.add_slider(d2, 'set_a', d2.a, (0.2, 1.0))
p.add_slider(d2, 'set_p', d2.p, (0.5, 2.0))

p.plotme((d1, d2))