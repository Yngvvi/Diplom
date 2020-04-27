import pandas as pd
import matplotlib.pyplot as plt
import numpy as np # Нужен для cos и sin на столбец
from Classaes import LinGraph, Graph, PlotGraph
from Models import Model_X, Model_Y

path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

# Создаём список строк в которых аппарат ещё не движется
del_str = df.index[(df['VertForvUp'] == 0) & (df['VertForvDown'] == 0) &
                   (df['VertBackUp'] == 0) & (df['VertBackDown'] == 0)].tolist()
# или перемещается с использованием маневренных двигателей
del_str.extend(df.index[(df['VertForvUp'].abs() + df['VertForvDown'].abs()
                   + df['VertBackUp'].abs() + df['VertBackDown'].abs()) > 5])
# Количество строк в таблице
length = df.shape[0]
# Сортируем этот список по возрастанию
del_str.sort()
# Длина разрыва между пиками
core = 500
# Список для концов пиков
nums = []
for i in range(len(del_str)-1):
    if del_str[i] + core < del_str[i+1]:
        nums.extend(del_str[i:i+2])
# Доделать позже для для более 2-х значений
df_clean = df.iloc[nums[0]+1:nums[1]]
# Заново нумерует строки с 0
df_clean = df_clean.reset_index(drop=True)

df_clean['Bat50'] = df_clean['Bat1_50_I'] + df_clean['Bat2_50_I'] + df_clean['Bat3_50_I'] + df_clean['Bat4_50_I']

# Для файла 'stz_R_emi_nakoplenie_1573453938716000.csv'
p_x_front = [1460, -16570, -1160, -12, -11, 85, 13, 26207]

Mod_x_1 = Model_X([df_clean['Heading'], df_clean['Roll'], df_clean['M_UP'], df_clean['M_Right'], df_clean['Bat50'],
                   df_clean['Pitch']], p_x_front)
df_clean['X_Front_comp'] = df_clean['Front_X'] - Mod_x_1.y

# Gr1 = Graph(['Front_X', 'Test'], ['Heading','Index'])
# Gr1.auto_slider(Mod_x_1, 8, 'a')
# Gr1.plot_sc(df_clean['Heading'], df_clean['Front_X'], Mod_x_1.y, )
# Gr1.plot_pl(df_clean.index, df_clean['Front_X'], df_clean['X_Front_comp'])

# Для файла 'stz_R_emi_nakoplenie_1573453938716000.csv'
p_y_front = [-3575, 16240, 1750, 17930, 3, -2, 5, -15, 500]
Mod_y_1 = Model_Y([df_clean['Heading'], df_clean['Roll'], df_clean['M_UP'], df_clean['M_Right'], df_clean['Bat50'],
                   df_clean['Pitch']], p_y_front)
df_clean['Y_Front_comp'] = df_clean['Front_Y'] - Mod_y_1.y

Gr1 = Graph(['Front_Y', 'Test'], ['Heading','Index'])
Gr1.auto_slider(Mod_y_1, 8, 'a')
Gr1.plot_sc(df_clean['Heading'], df_clean['Front_Y'], Mod_y_1.y, )
Gr1.plot_pl(df_clean.index, df_clean['Front_Y'], df_clean['Y_Front_comp'])
