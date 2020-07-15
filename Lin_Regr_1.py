import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn import linear_model


# Линейная регрессия для одной пары х и у
def make_lin_regr(x, y, dff):
    x_data = dff[x].values.reshape(-1, 1)
    y_data = dff[y].values.reshape(-1, 1)
    regr = linear_model.LinearRegression().fit(x_data, y_data)
    y_predict = regr.predict(x_data)
    R2 = round(r2_score(y_data, y_predict), 4)
    print(f'{y}({x}) R2 = {R2}')
    if regr.intercept_[0] >= 0:
        print(f'{y}({x}) = {round(regr.coef_[0][0],2)}*x + {round(regr.intercept_[0],2)}')
    else:
        print(f'{y}({x}) = {round(regr.coef_[0][0],2)}*x - {abs(round(regr.intercept_[0],2))}')
    fig = plt.figure()
    plt.title(y)
    plt.scatter( dff[x], dff[y], label=y, s=1)
    plt.plot(dff[x], y_predict, 'r', label='Модель')
    plt.legend()
    plt.grid()


# Регрессия нескольких зависимостей
def make_multi_regr(xs, ys, der, dff):
    for de in der:
        for xi in xs:
            for yi in ys:
                make_lin_regr(xi, de+yi, dff)


path = 'stz_R_emi_nakoplenie_1573453938716000.csv'
df = pd.read_csv(path, sep=';')

df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_R'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5
df['Back_R'] = (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5

# Выделение коробки
df = df.iloc[4200:]
# Повторная нумерация
df = df.reset_index(drop=True)

make_multi_regr(['M_UP', 'M_Right'], ['X'], ['Front_'], df)
# make_multi_regr(['Heading','Pitch', 'Roll', 'M_UP', 'M_Right', 'Bat50'],
#                 ['X', 'Y', 'Z', 'R'], ['Front_', 'Back_'], df)

plt.show()


