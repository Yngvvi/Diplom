import pandas as pd
import matplotlib.pyplot as plt
import numpy as np # Нужен для cos и sin на столбец
from Utilities import setGraph

path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Timestamp'] = df['Timestamp'] *(10**(-15))
print(df.columns)
# Это неизменные параметры?
# x_front_head_amp = -16500
y_front_head_amp = 18000

# x_front_pitch_amp = 28000
# y_front_pitch_amp = 30000

length = df.shape[0]

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
# Компенсация курса (Heading)
df['Y_Front_comp'] = df['Front_Y'] - 16500*np.cos(df['Heading']) + 2400 - 2000*np.sin(df['Heading'])
# Компенсация крена (Roll)
df['Y_Front_comp'] = df['Y_Front_comp'] + 22000*df['Roll'] - 1500
# Компенсация работы маршевых двигателей
df['Y_Front_comp'] = df['Y_Front_comp'] - 10*df['M_UP']*(np.abs(np.sin(df['Heading'])) - np.cos(df['Heading']))
df['Y_Front_comp'] = df['Y_Front_comp'] + 12*df['M_Right']*(np.abs(np.sin(df['Heading'])))\
                      - 10*df['M_Right']*np.cos(df['Heading'])
# Компенсация работы батарей 50В
df['Y_Front_comp1'] = df['Y_Front_comp'] - 10*df['Bat50']*(np.cos(df['Heading'])+np.sin(df['Heading']))


# setGraph(0, length, ['Front_Y', 'Y_Front_comp'], 'Index', 'Front_Y', df.index, df['Front_Y'], df['Y_Front_comp'])
setGraph(0, length, ['Front_Y', 'Y_Front_comp', 'Y_Front_comp1'], 'Index', 'Front_Y', df.index,
         df['Front_Y'], df['Y_Front_comp'], df['Y_Front_comp1'])

# setGraph(0, length, ['funq'], 'Index', 'Function', df.index, df['Bat50'])

# setGraph(0, length, ['Heading'], 'Index', 'Heading', df.index, df['Heading'])
# setGraph(0, length, ['Y_Front_comp', 'SinH', 'Bat50'], 'Index', 'Model', df.index,
#          df['Y_Front_comp'], df['SinH'], 250*df['Bat50'])

plt.show()