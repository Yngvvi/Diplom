import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Нужен для cos и sin на столбец
from scipy.optimize import least_squares
from sklearn.metrics import r2_score
from Models import Model_new
from Utilities import setPointGraph_new, setGraph_new

# Для постройки графиков для каждого воздействия


def mod_part(x, args):
    Mod = args[0] + args[1]*x[1]*np.abs(np.cos(x[0]))*np.sin(x[0]/2)
    return Mod


def regr(args, x, y):
    Mod = args[0] + args[1] * x[1] * np.abs(np.cos(x[0])) * np.sin(x[0] / 2)
    return Mod - y


path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

# Выделение коробки
df = df.iloc[4200:]
# Повторная нумерация
df = df.reset_index(drop=True)


df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_R'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5

y = 'Front_X'
x_lebel = 'M_UP'

p0 = np.ones(2)
x_data = [df['Heading'], df[x_lebel] ]
res_lsq = least_squares(regr, p0, args=(x_data, df[y]))
Mod = mod_part(x_data, res_lsq.x)

print('Коэффициент детерминации ', round(r2_score(df[y], Mod), 4))

fig, ax = plt.subplots()
y_lebels = [y, 'Model']

ax.scatter(df[x_lebel], df[y], s=1)
ax.scatter(df[x_lebel], Mod, s=1)

ax.set_title('Compensation ' + y)
ax.set_xlabel(x_lebel)
ax.legend(y_lebels, loc='lower right')
ax.grid()

plt.show()
