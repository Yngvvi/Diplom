import pandas as pd
import matplotlib.pyplot as plt
import numpy as np # Нужен для cos и sin на столбец
from Utilities import setGraph

path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Timestamp'] = df['Timestamp'] *(10**(-15))

length = df.shape[0]

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']

df['Z_Front_comp'] = df['Front_Z'] - 1800*np.sin(df['Heading'])




# setGraph(0, length, ['Front_Z', 'Z_Front_comp'], 'Index', 'Front_Z', df.index, df['Front_Z'], df['Z_Front_comp'])
setGraph(0, length, ['Front_Z', 'Heading'], 'Index', 'Front_Z', df.index, df['Front_Z'], 1000*df['Heading']-36000)
setGraph(0, length, ['Heading'], 'Index', 'Heading', df.index, df['Heading'])

plt.show()
