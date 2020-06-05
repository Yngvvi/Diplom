import numpy as np
import matplotlib.pyplot as plt


def furCikl(n, arg, x):
    if n == 0:
        return arg[0]
    else:
        return arg[2*n]*np.cos(n*x) + arg[2*n-1]*np.sin(n*x) + furCikl(n-1, arg, x)


def Test(arg, x):
    Mod = arg[0] + arg[1]*np.sin(x) + arg[2]*np.cos(x) + arg[3]*np.sin(2*x) + arg[4]*np.cos(2*x)
    Mod = Mod + arg[5]*np.sin(3*x) + arg[6]*np.cos(3*x)
    return Mod


def regr(args, x, y):
    Mod = furCikl(n, args, x)
    return Mod - y

n = 5

X = np.arange(50)
YY = np.random.sample(50)
args = np.ones(2*n + 1)
Y = furCikl(n, args, X)

R = regr(args, X, YY)

plt.plot(X, Y)
plt.plot(X, R)
# plt.plot(X, Test(args, X))
plt.grid()
plt.show()