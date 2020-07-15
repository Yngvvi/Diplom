import pandas as pd
import numpy as np
import scipy.stats


def getRes(dff):
    df_corr = dff[['Heading', 'Pitch', 'Roll', 'M_UP', 'M_Right', 'Bat50']]
    res = df_corr.loc['Front_X': 'Back_R']
    return res


path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573219511080000.csv'

df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']

# Так проще выводить корреляцию, иначе столбцы вставляются в конец
df.insert(3,'Front_R',(df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5)
df.insert(7, 'Back_R', (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5)

# C = df[['Front_X', 'Front_Y', 'Front_Z', 'Heading', 'Pitch', 'Roll']]
# print(C.corr(method='spearman'))

cor_sp = df.corr(method='spearman')
cor_p = df.corr(method='pearson')
cor_k = df.corr(method='kendall')


print('Корреляция Спирмена \n', getRes(cor_sp))
# print('Корреляция Пирсона \n', getRes(cor_p))
print('Корреляция Кендалла \n', getRes(cor_k))

# Корреляция Пирсона через numpy
# от pandas не отличается
# print(np.corrcoef(df['Front_Y'], df['Heading'])[0, 1])

# Корреляция Спирмена через scipy
# от pandas не отличается
# print(scipy.stats.spearmanr(df['Front_Y'], df['Heading']))
