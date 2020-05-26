import numpy as np


# Общая модель для осей x и y
class Model(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]) + args[2]*np.sin(x[0]) + args[3]*x[1]
        # Компенсация маршевых двигателей
        Mod = Mod + args[4]*x[2]*np.abs(np.cos(x[0]))*np.sin(x[0]/2)
        Mod = Mod + args[5]*x[3]*np.sin(x[0]/2)
        # Компенсация работы батарей 50В
        Mod = Mod + args[6]*(x[4] - args[7])*np.sin(x[0]/2)
        # Компенсация угла дифферента
        Mod = Mod + args[8] * x[5]
        return Mod

    def siple_regr_mod(self, args, x, y):
        # Компенсация курса и крена
        Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0]) + args[3] * x[1]
        # Компенсация угла дифферента
        Mod = Mod + args[8] * x[5]
        return Mod - y


class Model_Z(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]) + args[2]*np.sin(x[0]*2)
        Mod = Mod + +args[3]*np.sin(x[0]*2)**2
        Mod = Mod + args[4]*np.sin(0.81*x[0])
        Mod = Mod + args[5]* x[1] + args[6] * x[2]
        return Mod


class Model_Y(object):
    def __init__(self, x, args):
        self.x = x
        self.y = self.model(x, args)
        self.args = args

    def model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]) + args[2]*np.sin(x[0]) + args[3]*x[1]
        # Компенсация маршевых двигателей
        Mod = Mod + args[4]*x[2]*np.abs(np.cos(x[0]))*np.sin(x[0]/2)
        Mod = Mod + args[5]*x[3]*abs(np.sin(x[0]/2))
        # Компенсация работы батарей 50В
        Mod = Mod + args[6]*(x[4] - args[7])*np.sin(x[0]/2)
        # Компенсация угла дифферента
        Mod = Mod + args[8] * x[5]
        return Mod


class Model_X(object):
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


# Общая модель
class Model_new (object):
    def __init__(self, x, args, mod):
        self.x = x
        self.args = args
        if mod == 'L':
            self.y = self.model_light(x, args)
        elif mod == 'F':
            self.y = self.model(x, args)
        elif mod == 'Z':
            self.y = self.model_Z(x, args)

    def model(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]) + args[2]*np.sin(x[0]) + args[3]*x[1]
        # Компенсация маршевых двигателей
        Mod = Mod + args[4]*x[2]*np.abs(np.cos(x[0]))*np.sin(x[0]/2)
        Mod = Mod + args[5]*x[3]*np.sin(x[0]/2)
        # Компенсация работы батарей 50В
        Mod = Mod + args[6]*(x[4] - args[7])*np.sin(x[0]/2)
        # Компенсация угла дифферента
        Mod = Mod + args[8] * x[5]
        return Mod

    def model_light(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1]*np.cos(x[0]) + args[2]*np.sin(x[0]) + args[3]*x[1]
        # Компенсация угла дифферента
        Mod = Mod + args[4] * x[2]
        return Mod

    def model_Z(self, x, args):
        # Компенсация курса и крена
        Mod = args[0] + args[1] * np.cos(x[0]) + args[2] * np.sin(x[0] * 2)
        Mod = Mod + +args[3] * np.sin(x[0] * 2) ** 2
        Mod = Mod + args[4] * np.sin(0.81 * x[0])
        Mod = Mod + args[5] * x[1] + args[6] * x[2]
        return Mod