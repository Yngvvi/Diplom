import pandas as pd
import matplotlib.pyplot as plt
from Utilities import datenum


emiPath = 'Clean/stz_R_emi_nakoplenie_1573453938716000_clean.csv'
# emiPath = 'stz_R_emi_nakoplenie_1573453938716000.csv'

df = pd.read_csv(emiPath, sep=';')

# print(df.columns) # Вывод названий столбцов

# timeStmpBeg = (datenum(2000, 7, 3, 7, 50, 00) - datenum(1970, 1, 1)) * 24 * 60 * 60 * 10**6

timeStmpBeg = 9.6261*(10e14)
x_front_head_amp = -16500
x_front_pitch_amp = 28000
shift = 250

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']


# df.to_csv('test.csv')

plt.plot(df.index, df['Pitch'])
# plt.plot(df['Timestamp'], df['VertForvUp'])
# plt.plot(df_clean['Timestamp'], df_clean['VertForvUp'], color='red')
plt.xlabel('Index')
plt.ylabel('VertForvUp')
plt.grid()
plt.show()

