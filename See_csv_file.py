import pandas as pd
import matplotlib.pyplot as plt

# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
path = 'src/stz_R_emi_nakoplenie_1573455126581000.csv'

df = pd.read_csv(path, sep=';')

plt.plot(df.index, df['VertForvUp'])
plt.plot(df.index, df['VertForvUp'])
plt.xlabel('Index')
plt.ylabel('VertForvUp')
plt.grid()
plt.show()
