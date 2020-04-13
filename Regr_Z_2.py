import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score


def update(val):
    a0 = sl_a.val
    b0 = sl_b.val
    d0 = sl_d.val
    e0 = sl_e.val
    f0 = sl_f.val
    g0 = sl_g.val
    h0 = sl_h.val
    st1 = sl_st_1.val
    st2 = sl_st_2.val
    st3 = sl_st_3.val
    st4 = sl_st_4.val
    st5 = sl_st_5.val
    st6 = sl_st_6.val
    st7 = sl_st_7.val
    Mod1 = a0 + b0 * np.cos(df['Heading'] * st1) + d0 * np.sin(st2 * df['Heading']) + e0 * np.sin(st3 * df['Heading'])**st4
    Mod1 = Mod1 + f0 * np.sin(df['Heading'] * st5) + g0 * np.cos(st6 * df['Heading']) + h0 * np.cos(df['Heading'] * st7)
    xx = np.vstack((df['Heading'], Mod1))
    graph.set_offsets(xx.T)
    fig.canvas.draw_idle()
    R2 =round(r2_score(Mod1, df['Front_Z']), 2)
    plt.title(R2, position=(0.2, 0.8))


def reset(event):
    sl_a.reset()
    sl_b.reset()
    sl_d.reset()
    sl_e.reset()
    sl_f.reset()
    sl_g.reset()
    sl_h.reset()
    sl_st_1.reset()
    sl_st_2.reset()
    sl_st_3.reset()
    sl_st_4.reset()
    sl_st_5.reset()
    sl_st_6.reset()
    sl_st_7.reset()


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.2, bottom=0.35)

a0 = -31700
b0 = -1600
d0 = -500
e0 = 800
f0 = -90
g0 = 240
h0 = -170
st1 = 1
st2 = 2
st3 = 2
st4 = 2
st5 = 1
st6 = 3
st7 = 1/3
Mod1 = a0 + b0*np.cos(df['Heading']*st1) + d0*np.sin(st2*df['Heading']) + e0*np.sin(st3 * df['Heading'])**st4
Mod1 = Mod1 + f0*np.sin(df['Heading']*st5) + g0*np.cos(st6*df['Heading']) + h0*np.cos(df['Heading']*st7)

graph = plt.scatter(df['Heading'], Mod1, s=1)
graph2 = ax.scatter(df['Heading'], df['Front_Z'], s=1)

a_sl = plt.axes([0.1, 0.26, 0.5, 0.02])
b_sl = plt.axes([0.1, 0.22, 0.5, 0.02])
d_sl = plt.axes([0.1, 0.18, 0.5, 0.02])
e_sl = plt.axes([0.1, 0.14, 0.5, 0.02])
f_sl = plt.axes([0.1, 0.10, 0.5, 0.02])
g_sl = plt.axes([0.1, 0.06, 0.5, 0.02])
h_sl = plt.axes([0.1, 0.02, 0.5, 0.02])

st_1 = plt.axes([0.75, 0.26, 0.2, 0.02])
st_2 = plt.axes([0.75, 0.22, 0.2, 0.02])
st_3 = plt.axes([0.75, 0.18, 0.2, 0.02])
st_4 = plt.axes([0.75, 0.14, 0.2, 0.02])
st_5 = plt.axes([0.75, 0.10, 0.2, 0.02])
st_6 = plt.axes([0.75, 0.06, 0.2, 0.02])
st_7 = plt.axes([0.75, 0.02, 0.2, 0.02])

sl_a = Slider(a_sl, 'a0', -35000, -25000, valinit=a0)
sl_b = Slider(b_sl, 'b0', -3000, 0, valinit=b0)
sl_d = Slider(d_sl, 'd0', -2000, 0, valinit=d0)
sl_e = Slider(e_sl, 'e0', 0, 2000, valinit=e0)
sl_f = Slider(f_sl, 'f0', -300, 100, valinit=f0)
sl_g = Slider(g_sl, 'g0', 0, 500, valinit=g0)
sl_h = Slider(h_sl, 'h0', -2000, 500, valinit=h0)

sl_st_1 = Slider(st_1, 'st1', 0, 4, valinit=st1)
sl_st_2 = Slider(st_2, 'st2', 0, 4, valinit=st2)
sl_st_3 = Slider(st_3, 'st3', 0, 4, valinit=st3)
sl_st_4 = Slider(st_4, 'st4', 0, 4, valinit=st4)
sl_st_5 = Slider(st_5, 'st5', 0, 4, valinit=st5)
sl_st_6 = Slider(st_6, 'st6', 1, 4, valinit=st6)
sl_st_7 = Slider(st_7, 'st7', -2, 4, valinit=st7)

sl_a.on_changed(update)
sl_b.on_changed(update)
sl_d.on_changed(update)
sl_e.on_changed(update)
sl_f.on_changed(update)
sl_g.on_changed(update)
sl_h.on_changed(update)
sl_st_1.on_changed(update)
sl_st_2.on_changed(update)
sl_st_3.on_changed(update)
sl_st_4.on_changed(update)
sl_st_5.on_changed(update)
sl_st_6.on_changed(update)
sl_st_7.on_changed(update)

# Кнопка Reset
resetax = plt.axes([0.01, 0.6, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')
button.on_clicked(reset)

ax.grid()
plt.show()
