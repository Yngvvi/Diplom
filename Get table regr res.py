import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import least_squares
from sklearn.metrics import r2_score
from time import process_time  # Считает время работы
from Models import Model
import os.path


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


def getPoopt(y,  prec = 4):
    p0 = np.ones(5)
    x_data = [df_clean['Heading'], df_clean['Roll'], df_clean['M_Right'],
              df_clean['M_UP'], df_clean['Bat50'], df_clean['Pitch']]
    res_lsq = least_squares(siple_regr_mod, p0, args=([df_clean['Heading'], df_clean['Roll'],
                                                               df_clean['Pitch']], y))
    popt = getP(res_lsq.x)
    Mod = Model(x_data, popt)
    res = np.round(res_lsq.x, 2)
    R2 = round(r2_score(y, Mod.y), prec)
    return res, R2


def getRow(bloc, table):
    popt, r2 = getPoopt(df_clean[bloc])
    table[bloc+' R2'] = [r2]
    for i in range(len(popt)):
        spot = bloc + ' a' + str(i)
        table[spot] = [popt[i]]

def new_row(name, blocs):
    row = pd.DataFrame()
    row['name'] = [name]
    for bloc in blocs:
        getRow(bloc, row)
    return row


# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573219511080000.csv'

# path = 'src/stz_R_emi_nakoplenie_1573215120226000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573215634542000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573216498735000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573218440056000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573218676053000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573219511080000.csv'  # Повтор
# path = 'src/stz_R_emi_nakoplenie_1573221654385000.csv' # Что в нём?
# path = 'src/stz_R_emi_nakoplenie_1573221850047000.csv' # Что в нём?
# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'  # Повтор
# path = 'src/stz_R_emi_nakoplenie_1573455126581000.csv'
path = 'src/stz_R_emi_nakoplenie_1573457751204000.csv'

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

name = path.split('/')[1]
New_row = new_row(name, ['Front_X', 'Front_Y', 'Back_X', 'Back_Y'])

name_t = 'Работа регрессии.csv'

# Проверяем есть ли такой файл в папке с проектом
check_file = os.path.exists(name_t)
# Если нет, создаём его
if check_file is False:
    head = list(New_row)
    New_row.to_csv(name_t, header=head, index=False)
# Если есть, проверяем записывали ли в него данные об этом файле и дописываем
else:
    df_next = pd.read_csv(name_t)
    if name not in df_next['name']:
        New_row.to_csv(name_t, mode='a',  header=False, index=False)
print('Всё сделано!')
