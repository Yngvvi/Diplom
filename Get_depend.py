import pandas as pd
import matplotlib.pyplot as plt


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


path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573216498735000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573215120226000.csv'

df = pd.read_csv(path, sep=';')
df['Bat50'] = df['Bat1_50_I'] + df['Bat2_50_I'] + df['Bat3_50_I'] + df['Bat4_50_I']
df['Front_R'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5
df['Back_R'] = (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5

print(df.columns) # Вывод названий столбцов

# multiScat(['Heading','Pitch', 'Roll'], ['X', 'Y', 'Z', 'R'], ['Front_'], df)
# multiScat(['Heading','Pitch', 'Roll'], ['Z'], ['Front_'], df)
multiScat(['Heading','Pitch', 'Roll', 'M_UP', 'M_Right', 'Bat50' ], ['X', 'Y', 'Z', 'R'], ['Front_'], df)

plt.show()