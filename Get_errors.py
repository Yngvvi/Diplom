import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import least_squares
from sklearn.metrics import r2_score
from Models import Model
from Utilities import setGraph_new, setPointGraph_new
from Classaes import Graph, LinGraph, PlotGraph


def siple_regr_mod(args, x, y):
    # Компенсация курса и крена
    Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
    # Компенсация угла дифферента
    Mod = Mod + args[4] * x[2]
    return Mod - y


# Если сразу использовать p0 длиной 9 появляется огромное a4, которое портит модель
def getP(res, num=9):
    popt = np.zeros(num)
    popt[:4] = res[:4]
    popt[-1] = res[-1]
    return popt


def getPopt(y):
    p0 = np.ones(5)
    res_lsq = least_squares(siple_regr_mod, p0, args=([df_clean['Heading'], df_clean['Roll'],
                                                               df_clean['Pitch']], y))
    popt = getP(res_lsq.x)
    return popt

# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573219511080000.csv'

path = 'src/stz_R_emi_nakoplenie_1573215120226000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573215634542000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573216498735000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573218440056000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573218676053000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573219511080000.csv'  # Повтор
# path = 'src/stz_R_emi_nakoplenie_1573221654385000.csv' # Что в нём?
# path = 'src/stz_R_emi_nakoplenie_1573221850047000.csv' # Что в нём?
# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'  # Повтор
# path = 'src/stz_R_emi_nakoplenie_1573455126581000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573457751204000.csv'

df = pd.read_csv(path, sep=';')
df['Timestamp'] = df['Timestamp'] *(10**(-15))

# Удаление строк в которых аппарат ещё не движется
df_clean = df.drop(df.index[(df['VertForvUp'] == 0) & (df['VertForvDown'] == 0) &
                   (df['VertBackUp'] == 0) & (df['VertBackDown'] == 0)])
# или перемещается с использованием маневренных двигателей
df_clean = df_clean.drop(df.index[(df['VertForvUp'].abs() + df['VertForvDown'].abs()
                   + df['VertBackUp'].abs() + df['VertBackDown'].abs()) > 0.15])

df_clean['Bat50'] = df_clean['Bat1_50_I'] + df_clean['Bat2_50_I'] + \
                    df_clean['Bat3_50_I'] + df_clean['Bat4_50_I']

df_clean['Front_R'] = (df_clean['Front_X']**2 + df_clean['Front_Y']**2 + df_clean['Front_Z']**2)**0.5
df_clean['Back_R'] = (df_clean['Back_X']**2 + df_clean['Back_Y']**2 + df_clean['Back_Z']**2)**0.5


x_data = [df_clean['Heading'], df_clean['Roll'], df_clean['M_Right'],
              df_clean['M_UP'], df_clean['Bat50'], df_clean['Pitch']]

# Для фронтального датчика

# # Первичный расчёт коэффициентов
# Mod_front = Model(x_data, getPopt(df_clean['Front_R']))
# df_clean['R_Front_comp'] = df_clean['Front_R'] - Mod_front.y
#
# # Построение линейного графика
# Gr = LinGraph('Test', 'Index')
# Gr.auto_slider(Mod_front, 9, 'a')
# # Строит два графика
# Gr.plotme(df_clean.index, df_clean['Front_R'], df_clean['R_Front_comp'], )
# # Для случаев с большим смещением между графиками, строит только компенсированный
# # Gr.plot_one(df_clean.index, df_clean['Front_R'], df_clean['R_Front_comp'], )

# Для кормового датчика
# Первичный расчёт коэффициентов
Mod_back = Model(x_data, getPopt(df_clean['Back_R']))
df_clean['R_Back_comp'] = df_clean['Back_R'] - Mod_back.y

# Построение линейного графика
# Gr = LinGraph('Test', 'Index')
# Gr.auto_slider(Mod_back, 9, 'a')
# # Строит два графика
# # Gr.plotme(df_clean.index, df_clean['Back_R'], df_clean['R_Back_comp'], )
# # Для случаев с большим смещением между графиками, строит только компенсированный
# Gr.plot_one(df_clean.index, df_clean['Back_R'], df_clean['R_Back_comp'], )

# Построение сдвоенного графика
Gr = Graph(['Front_R', ''], ['Heading','Index'])
Gr.auto_slider(Mod_back, 9, 'a')
Gr.plot_sc(df_clean['Heading'], df_clean['Front_R'], Mod_back.y, )
# Для случаев с большим смещением между графиками, строит только компенсированный
Gr.plot_pl_one(df_clean.index, df_clean['Back_R'], df_clean['R_Back_comp'], )
