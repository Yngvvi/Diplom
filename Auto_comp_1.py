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

p0 = np.ones(5)
x_data = [df_clean['Heading'], df_clean['Roll'], df_clean['M_Right'],
          df_clean['M_UP'], df_clean['Bat50'], df_clean['Pitch']]

# Расчёт коэффициентов для фронтального датчика
# По оси X
res_lsq_front_X = least_squares(siple_regr_mod, p0, args=([df_clean['Heading'], df_clean['Roll'],
                                                         df_clean['Pitch']], df_clean['Front_X']))
popt_front_X = getP(res_lsq_front_X.x)
Mod_front_X = Model(x_data, popt_front_X)
df_clean['X_Front_comp'] = df_clean['Front_X'] - Mod_front_X.y
# По оси Y
res_lsq_front_Y = least_squares(siple_regr_mod, p0, args=([df_clean['Heading'], df_clean['Roll'],
                                                         df_clean['Pitch']], df_clean['Front_Y']))
popt_front_Y = getP(res_lsq_front_Y.x)
Mod_front_Y = Model(x_data, popt_front_Y)
df_clean['Y_Front_comp'] = df_clean['Front_Y'] - Mod_front_Y.y

# Расчёт коэффициентов для кормового датчика
# По оси X
res_lsq_back_X = least_squares(siple_regr_mod, p0, args=([df_clean['Heading'], df_clean['Roll'],
                                                         df_clean['Pitch']], df_clean['Back_X']))
popt_back_X = getP(res_lsq_back_X.x)
Mod_back_X = Model(x_data, popt_back_X)
df_clean['X_Back_comp'] = df_clean['Back_X'] - Mod_back_X.y
# По оси Y
res_lsq_back_Y = least_squares(siple_regr_mod, p0, args=([df_clean['Heading'], df_clean['Roll'],
                                                         df_clean['Pitch']], df_clean['Back_Y']))
popt_back_Y = getP(res_lsq_back_Y.x)
Mod_back_Y = Model(x_data, popt_back_Y)
df_clean['Y_Back_comp'] = df_clean['Back_Y'] - Mod_back_Y.y

prec = 4
print('Коэффициенты для фронтального датчика по оси х:', np.round(res_lsq_front_X.x, 2))
print('Коэффициент детерминации', round(r2_score(df_clean['Front_X'], Mod_front_X.y), prec))
print('Коэффициенты для фронтального датчика по оси у:', np.round(res_lsq_front_Y.x, 2))
print('Коэффициент детерминации', round(r2_score(df_clean['Front_Y'], Mod_front_Y.y), prec))

print('Коэффициенты для кормового датчика по оси х:', np.round(res_lsq_back_X.x, 2))
print('Коэффициент детерминации', round(r2_score(df_clean['Back_X'], Mod_back_X.y), prec))
print('Коэффициенты для кормового датчика по оси у:', np.round(res_lsq_back_Y.x, 2))
print('Коэффициент детерминации', round(r2_score(df_clean['Back_Y'], Mod_back_Y.y), prec))


# Линейные графики
setGraph_new('Compensation front X', df_clean.index,
             df_clean['Front_X'], df_clean['X_Front_comp'], pos='lower right')
setGraph_new('Compensation front Y', df_clean.index, df_clean['Front_Y'], df_clean['Y_Front_comp'])
setGraph_new('Compensation back X', df_clean.index,
             df_clean['Back_X'], df_clean['X_Back_comp'], pos='lower right')
setGraph_new('Compensation back Y', df_clean.index, df_clean['Back_Y'], df_clean['Y_Back_comp'])

# Точечные графики
setPointGraph_new('Compensation front X', df_clean['Heading'], df_clean['Front_X'], Mod_front_X.y)
setPointGraph_new('Compensation front Y', df_clean['Heading'], df_clean['Front_Y'], Mod_front_Y.y)
setPointGraph_new('Compensation back X', df_clean['Heading'], df_clean['Back_X'], Mod_back_X.y)
setPointGraph_new('Compensation back Y', df_clean['Heading'], df_clean['Back_Y'], Mod_back_Y.y)

t_end = process_time()
print('Время работы {} c'.format(t_end - t_start))

plt.show()
