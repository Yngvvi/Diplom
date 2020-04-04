from datetime import datetime
import matplotlib.pyplot as plt

# Аналогично datenum из MAtLab
def datenum (Y, M, D, H = 0, Mi = 0, S = 0):
    return datetime.toordinal(datetime(Y, M, D, H, Mi, S)) + 366


# Устанавливает настройки для построения графика
# на одном графике может быть несколько функций
# plt.show() должен быть один на несколько вызовов функции
# иначе один график будет появляться после закрытия окна другого
# y_lebels передаётся как список в []
def setGraph(start, end, y_lebels, x_lebel, tittle, x, *y):
    fig, ax = plt.subplots()
    ax.set_xlim([start, end])
    ax.plot(x, *y)
    # ax.legend(y_lebel)
    ax.set_title(tittle)
    ax.set_xlabel(x_lebel)
    # ax.set_ylabel(y_lebel)
    ax.legend(y_lebels, loc='lower right')
    ax.grid()

