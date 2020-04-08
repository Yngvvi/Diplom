import pandas as pd
import matplotlib.pyplot as plt
import numpy as np # Нужен для cos и sin на столбец
from Utilities import setGraph

path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Timestamp'] = df['Timestamp'] *(10**(-15))
print(df.columns)

length = df.shape[0]

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_res'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5
df['Back_res'] = (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5

# Front
df['Front_comp'] = df['Front_res']


# setGraph(0, length, ['Front_res'], 'Index', 'Front_res', df.index, df['Front_res'])
setGraph(0, length, ['Front_res', 'Front_comp'], 'Index', 'Front_res', df.index, df['Front_res'], df['Front_comp'])

plt.show()
