import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np  # Нужен для cos и sin на столбец
from sklearn.metrics import r2_score
from scipy.optimize import least_squares
from Utilities import plotFig, scatFig, setPointGraph_new, setGraph_new
from Classaes import Graph, PlotGraph, LinGraph

# Интерполяция сплайнами
# деление на 2 части

class Model_1(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        Mod = model_part_1(x, args)
        return Mod


def model_part_1(x, args):
    Mod = args[0] + args[1] * np.sin(x[0]*args[2] + args[3]) + args[4] * np.sin(x[0])**2
    Mod = Mod + args[5] * np.sin(x[0]*2)**2
    Mod = Mod + args[6] * np.cos(x[0]*args[7])*np.sin(x[0]*args[8])
    return Mod

def regr_part_1(x, args, y):
    Mod = model_part_1(x, args)
    return Mod - y


# def model_part_2(x, args):
#     Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0])
#     return Mod
#
#
# def regr_part_2(x, args, y):
#     Mod = model_part_2(x, args)
#     return Mod - y


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

max_heading = max(df['Heading'])

data_1 = df.loc[df['Heading'] <= max_heading/2]
data_1 = data_1.reset_index(drop=True)

data_2 = df.loc[df['Heading'] > max_heading/2]

p0 = np.ones(3)

# res_lsq_1 = least_squares(regr_part_1, p0, args=(data_1['Heading'], data_1['Front_Z']))
# Mod_1 = Model_1([data_1['Heading']], res_lsq_1.x)
Mod_hand = Model_1([data_1['Heading']], [-31285.0, -2040.76, 1.56, 1.24, -1999.45, 473.67, 2000, 1,1])
data_1['Z_Front_comp'] = data_1['Front_Z'] - Mod_hand.y
# -31285.0, -1978.0, 1.66, 0.72, -747.0, 100
# setGraph_new('Compensation ' , dff.index, dff[y + '_comp'], pos=pos)
# setPointGraph_new('Compensation ', data_1['Heading'], [data_1['Front_Z'], Mod_1.y])
# setPointGraph_new('Compensation ', data_1['Heading'], [data_1['Front_Z'], Mod_hand.y])

prec = 4
# print('Коэффициенты для фронтального датчика:', res_lsq_1.x)
# print('Коэффициент детерминации', round(r2_score(data_1['Front_Z'], Mod_1.y), prec))

# plt.show()

# Gr = PlotGraph('Test', 'Heading')
# Gr.auto_slider(Mod_hand, 6, 'a')
# Gr.plotme(data_1['Heading'], data_1['Front_Z'], Mod_hand.y)

Gr = Graph(['Front_Z', 'Test'], ['Heading','Index'])
Gr.auto_slider(Mod_hand, 9, 'a')
Gr.plot_sc(data_1['Heading'], data_1['Front_Z'], Mod_hand.y )
Gr.plot_pl_one(data_1.index, data_1['Front_Z'], data_1['Z_Front_comp'])

