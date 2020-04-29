import pandas as pd
import matplotlib.pyplot as plt
import os

# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573455126581000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573457751204000.csv'

# path = 'src/stz_R_emi_nakoplenie_1573219511080000.csv'
path = 'src/stz_R_emi_nakoplenie_1573218440056000.csv'


# Для вывода всех графиков для всех файлов в папке

# directory = 'src'
# files = os.listdir(directory)
# for file in files:
#     path = directory + '/' + file
#     df = pd.read_csv(path, sep=';')
#     fig = plt.figure()
#     plt.plot(df.index, df['VertForvUp'])
#     plt.plot(df.index, df['VertForvUp'])
#     plt.title(file)
#     plt.xlabel('Index')
#     plt.ylabel('VertForvUp')
#     plt.grid()
#
# plt.show()

df = pd.read_csv(path, sep=';')
fig = plt.figure()
plt.plot(df.index, df['VertForvUp'])
plt.plot(df.index, df['VertForvUp'])
plt.xlabel('Index')
plt.ylabel('VertForvUp')
plt.grid()

plt.show()
