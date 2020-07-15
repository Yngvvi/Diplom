import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score
from scipy.optimize import least_squares
from Utilities import plotFig, scatFig, setPointGraph_new, setGraph_new
from Classaes import Graph, PlotGraph, LinGraph

# Интерполяция сплайнами
# деление на 4 части


class Model_1(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        Mod = model_part_1(x, args)
        return Mod


def model_part_1(x, args):
    Mod = args[0] + args[1] * x[0] + args[2] * (x[0] + args[3])**2 + args[4] * (x[0])**3
    Mod = Mod + args[5] * (x[0]+ args[6])**4 + args[7] * np.sin(x[0] * args[8])
    return Mod


def regr_part_1(args, x, y):
    Mod = model_part_1(x, args)
    return Mod - y


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')
# Выделение коробки
df = df.iloc[10400:]
# Крайняя граница для деления на участки
max_heading = max(df['Heading'])

data_1 = df.loc[df['Heading'] <= max_heading/4]
data_1 = data_1.reset_index(drop=True)
# data_1 = data_1.sort_values(by='Heading')

# data_2 = df.loc[df['Heading'] > max_heading/2]
# p0 = [-32857.12, -2433.29, 3238.14, 0.05]
# p0 = np.ones(4)
# res_lsq_1 = least_squares(regr_part_1, p0, args=(data_1['Heading'], data_1['Front_Z']))
# Mod_1 = Model_1([data_1['Heading']], res_lsq_1.x)

# prec = 4
# print('Коэффициенты для фронтального датчика:', res_lsq_1.x)
# print('Коэффициент детерминации', round(r2_score(data_1['Front_Z'], Mod_1.y), prec))


a_opt_1 = [-32857.12, -2433.29, 3238.14, 0.05, -1037.04, -189.16, -0.87, -19.79, 1, ]

Mod_hand_1 = Model_1([data_1['Heading']], a_opt_1)
data_1['Z_Front_comp'] = data_1['Front_Z'] - Mod_hand_1.y

Gr = PlotGraph('Test', 'Heading')
Gr.auto_slider(Mod_hand_1, len(a_opt_1), 'a')
Gr.plotme(data_1['Heading'], data_1['Front_Z'], Mod_hand_1.y)

# Gr = Graph(['Front_Z', 'Test'], ['Heading','Index'])
# Gr.auto_slider(Mod_hand_1, len(a_opt_1), 'a')
# Gr.plot_sc(data_1['Heading'], data_1['Front_Z'], Mod_hand_1.y )
# Gr.plot_pl_one(data_1.index, data_1['Front_Z'], data_1['Z_Front_comp'])
