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
