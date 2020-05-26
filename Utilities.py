from datetime import datetime
import matplotlib.pyplot as plt


# Аналогично datenum из MatLab
def datenum (Y, M, D, H=0, Mi=0, S=0):
    return datetime.toordinal(datetime(Y, M, D, H, Mi, S)) + 366


# Устанавливает настройки для построения линейного графика
# на одном графике может быть несколько функций
# plt.show() должен быть один на несколько вызовов функции
# иначе один график будет появляться после закрытия окна другого
# y_lebels передаётся как список в [] даже для одной функции
def setGraph(start, end, y_lebels, x_lebel, tittle, x, *y):
    fig, ax = plt.subplots()
    ax.set_xlim([start, end])
    # Больше 2-х функций plot переварить не может, поэтому цикл
    for i in y:
        ax.plot(x, i)
    ax.set_title(tittle)
    ax.set_xlabel(x_lebel)
    # ax.legend(y_lebels, loc='lower right')
    ax.legend(y_lebels, loc='upper right')
    ax.grid()


def setGraph_new(tittle,  x, *y, pos='upper right'):
    fig, ax = plt.subplots()
    y_lebels = []
    if x.name is None:
        x_lebel = 'Index'
    else:
        x_lebel = x.name
    # Больше 2-х функций plot переварить не может, поэтому цикл
    for i in y:
        ax.plot(x, i)
        y_lebels.append(i.name)
    ax.set_title(tittle)
    ax.set_xlabel(x_lebel)
    ax.legend(y_lebels, loc=pos)
    ax.grid()


# Устанавливает настройки для построения точечного графика
def setPointGraph(start, end, y_lebels, x_lebel, tittle, x, *y):
    fig, ax = plt.subplots()
    # ax.set_xlim([start, end])
    for i in y:
        ax.scatter(x, i, s=1)
    ax.set_title(tittle)
    ax.set_xlabel(x_lebel)
    ax.legend(y_lebels, loc='lower right')
    ax.grid()


def setPointGraph_new(tittle, x, *y, pos='lower right'):
    fig, ax = plt.subplots()
    y_lebels = []
    if x.name is None:
        x_lebel = 'Index'
    else:
        x_lebel = x.name
    for i in y:
        ax.scatter(x, i, s=1)
        if i.name is not None:
            y_lebels.append(i.name)
        else:
            y_lebels.append('Model')
    ax.set_title(tittle)
    ax.set_xlabel(x_lebel)
    ax.legend(y_lebels, loc=pos)
    ax.grid()



def scatFig(x, y, xlabel=None):
    fig = plt.figure()
    plt.title(y.name)
    if xlabel is None:
        plt.xlabel(x.name)
    plt.scatter(x, y, s=1)
    plt.grid()


def plotFig(x, y, xlabel=None):
    fig = plt.figure()
    plt.title(y.name)
    if xlabel is None:
        plt.xlabel(x.name)
    plt.plot(x, y)
    plt.grid()


def multiScat(x, y, der, dff):
    for de in der:
        for xi in x:
            for yi in y:
                scatFig(dff[xi], dff[de+yi])