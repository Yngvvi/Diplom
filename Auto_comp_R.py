import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import least_squares
from sklearn.metrics import r2_score
from time import process_time  # Считает время работы
from Models import Model
from Utilities import setGraph_new, setPointGraph_new


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


t_start = process_time()

# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573219511080000.csv'

path = 'src/stz_R_emi_nakoplenie_1573215120226000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573215634542000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573216498735000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573218440056000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573218676053000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573219511080000.csv'  # Повтор
# path = 'src/stz_R_emi_nakoplenie_1573221654385000.csv' # Что в нём?
# path = 'src/stz_R_emi_nakoplenie_1573221850047000.csv' # Что в нём?
# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'  # Повтор
# path = 'src/stz_R_emi_nakoplenie_1573455126581000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573457751204000.csv'

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

df_clean['Front_R'] = (df_clean['Front_X']**2 + df_clean['Front_Y']**2 + df_clean['Front_Z']**2)**0.5
df_clean['Back_R'] = (df_clean['Back_X']**2 + df_clean['Back_Y']**2 + df_clean['Back_Z']**2)**0.5


p0 = np.ones(5)
x_data = [df_clean['Heading'], df_clean['Roll'], df_clean['M_Right'],
          df_clean['M_UP'], df_clean['Bat50'], df_clean['Pitch']]

# Расчёт коэффициентов для фронтального датчика
res_lsq_front = least_squares(siple_regr_mod, p0, args=([df_clean['Heading'], df_clean['Roll'],
                                                         df_clean['Pitch']], df_clean['Front_R']))
popt_front = getP(res_lsq_front.x)
Mod_front = Model(x_data, popt_front)
df_clean['R_Front_comp'] = df_clean['Front_R'] - Mod_front.y

# Расчёт коэффициентов для кормового датчика
res_lsq_back = least_squares(siple_regr_mod, p0, args=([df_clean['Heading'], df_clean['Roll'],
                                                         df_clean['Pitch']], df_clean['Back_R']))
popt_back = getP(res_lsq_back.x)
Mod_back = Model(x_data, popt_back)
df_clean['R_Back_comp'] = df_clean['Back_R'] - Mod_back.y

prec = 4
print('Коэффициенты для фронтального датчика:', np.round(res_lsq_front.x, 2))
print('Коэффициент детерминации', round(r2_score(df_clean['Front_R'], Mod_front.y), prec))

print('Коэффициенты для кормового датчика:', np.round(res_lsq_back.x, 2))
print('Коэффициент детерминации', round(r2_score(df_clean['Back_R'], Mod_back.y), prec))

# Линейные графики
setGraph_new('Compensation front', df_clean.index,
             df_clean['Front_R'], df_clean['R_Front_comp'], pos='lower right')
setGraph_new('Compensation front', df_clean.index, df_clean['R_Front_comp'], pos='lower right')
setGraph_new('Compensation back', df_clean.index, df_clean['R_Back_comp'], pos='lower right')

# Точечные графики
setPointGraph_new('Compensation front', df_clean['Heading'], df_clean['Front_R'], Mod_front.y)
setPointGraph_new('Compensation back', df_clean['Heading'], df_clean['Back_R'], Mod_back.y)

t_end = process_time()
print('Время работы {} c'.format(t_end - t_start))

plt.show()
