import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn import linear_model
from Classaes import Graph, PlotGraph, LinGraph


class Model(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        Mod = args[0] + args[1] * x
        return Mod


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_R'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5
df['Back_R'] = (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5

# Выделение коробки
df = df.iloc[4200:]

a_opt = [-10, 100000]
x_name = 'Roll'
y_name = 'Front_X'
comp_name = y_name + '_comp'
x_data = df[x_name]
Mod_front = Model(x_data, a_opt)
df[comp_name] = df[x_name] - Mod_front.y

# Один график

Gr = PlotGraph('Test', x_name)
Gr.auto_slider(Mod_front, 2, 'a')
Gr.plotme(df[x_name], df[y_name], Mod_front.y)

# Два графика

# Gr = Graph([y_name, 'Test'], [x_name,'Index'])
#
# Gr.auto_slider(Mod_front, 2, 'a')
# Gr.plot_sc(df[x_name], df[y_name], Mod_front.y )
# Gr.plot_pl_one(df.index, df[y_name], df[comp_name])

