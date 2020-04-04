import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Utilities import setGraph

path = 'stz_R_emi_nakoplenie_1573453938716000.csv'

df = pd.read_csv(path, sep=';')

# print(df.columns) # Вывод названий столбцов
# print(df.dtypes) # Вывод типов данных в столбцах

df['Timestamp'] = df['Timestamp'] *(10**(-15))


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

timeStmpBeg = 9.6261*(10e14)
x_front_head_amp = -16500
x_front_pitch_amp = 28000
shift = 250

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_comp'] = df['Front_X'] - x_front_head_amp*np.sin(df['Heading'])

df['SinH'] = df['Pitch']*28000*((3+np.cos(df['Heading']-3*np.pi/2)+np.cos(df['Heading']))**(1/8))
df['SinH'] = df['SinH'] + 2600
df['SinH'] = df['SinH'] - 3500 * np.sin(df['Heading']/2)
df['SinH'] = df['SinH'] + 700*np.abs(np.sin(df['Heading']))
df['SinH'] = df['SinH'] + 200*np.sin(df['Heading'])
df['SinH'] = (np.cos(df['Heading']-3*np.pi/2)+np.cos(df['Heading']))/3


# Устанавливает настройки для построения графика (пока без цвета)
# setGraph(start, end, y_lebels, x_lebel, tittle, x, *y)
setGraph(0, length, ['Pitch', 'SinH'], 'Index', 'Pitch', df.index, df['Pitch'], df['SinH'])
setGraph(0, length, ['Heading'], 'Index', 'Heading', df.index, df['Heading'])
setGraph(0, length, ['Front_X'], 'Index', 'Front_X', df.index, df['Front_X'])
setGraph(0, length, ['Front_X', 'SinH', 'Bat50'], 'Index', 'Model', df.index, df['Front_X'], df['SinH'], df['Bat50'])

plt.show()
