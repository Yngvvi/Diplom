import pandas as pd
import numpy as np  # Нужен для cos и sin на столбец
from Classaes import LinGraph


class Model(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.sin(x[0]) + args[2]*x[1]
        # Компенсация маршевых двигателей
        Mod = Mod + args[3]*x[2]*np.abs(np.cos(x[0]))*np.sin(x[0]/2)
        Mod = Mod + args[4]*x[3]*np.sin(x[0]/2)
        # # Компенсация работы батарей 50В
        Mod = Mod + args[5]*(x[4] - args[6])*np.sin(x[0]/2)
        # # Компенсация угла дифферента
        Mod = Mod + args[7] * x[5]
        return Mod


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']

p_front = [1460, -16570, -1160, -12, -11, 85, 13, 26207]
p_back = [2700, -16420, 2110, -58, -19, -80, -56, 28220]

# Компенсация фронтального датчика
Mod1 = Model([df['Heading'], df['Roll'], df['M_UP'], df['M_Right'], df['Bat50'], df['Pitch']], p_front)
df['X_Front_comp'] = df['Front_X'] - Mod1.y
Mod2 = Model([df['Heading'], df['Roll'], df['M_UP'], df['M_Right'], df['Bat50'], df['Pitch']], p_back)
df['X_Back_comp'] = df['Back_X'] - Mod2.y

Gr = LinGraph('Test', 'Index')

# Для фронтального датчика

# Gr.add_slider(Mod1, 'a0', Mod1.args[0],(-100, 3000))
# Gr.add_slider(Mod1, 'a1', Mod1.args[1],(-20000, 50000))
# Gr.add_slider(Mod1, 'a2', Mod1.args[2],(-5000, 5000))
# Gr.add_slider(Mod1, 'a3', Mod1.args[3],(-50, 50))
# Gr.add_slider(Mod1, 'a4', Mod1.args[4],(-100, 100))
# Gr.add_slider(Mod1, 'a5', Mod1.args[5],(-500, 500))
# Gr.add_slider(Mod1, 'a6', Mod1.args[6],(-500, 500))
# Gr.add_slider(Mod1, 'a7', Mod1.args[7],(10000, 50000))

# Gr.auto_slider(Mod1, 8, 'a')
# Gr.plotme(df.index, df['Front_X'], df['X_Front_comp'], )

# Для кормового датчика

# Gr.add_slider(Mod2, 'a0', Mod2.args[0],(-100, 3000))
# Gr.add_slider(Mod2, 'a1', Mod2.args[1],(-20000, 50000))
# Gr.add_slider(Mod2, 'a2', Mod2.args[2],(-5000, 10000))
# Gr.add_slider(Mod2, 'a3', Mod2.args[3],(-1500, 500))
# Gr.add_slider(Mod2, 'a4', Mod2.args[4],(-100, 100))
# Gr.add_slider(Mod2, 'a5', Mod2.args[5],(-100, 100))
# Gr.add_slider(Mod2, 'a6', Mod2.args[6],(-100, 100))
# Gr.add_slider(Mod2, 'a7', Mod2.args[7],(10000, 35000))

Gr.auto_slider(Mod2, 8, 'a')

Gr.plotme(df.index, df['Back_X'], df['X_Back_comp'], )
