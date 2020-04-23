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
        # Mod = Mod + args[3]*x[2]*np.abs(np.cos(x[0]))*np.sin(x[0]/2)
        # Mod = Mod + args[4]*x[3]*np.sin(x[0]/2)
        # # # Компенсация работы батарей 50В
        # Mod = Mod + args[5]*(x[4] - args[6])*np.sin(x[0]/2)
        # # # Компенсация угла дифферента
        # Mod = Mod + args[7] * x[5]
        return Mod


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_res'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5
df['Back_res'] = (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5

p_front = [1460, -16570, -1160, -12, -11, 85, 13, 26207]
# p_back = [2700, -16420, 2110, -58, -19, -80, -56, 28220]
