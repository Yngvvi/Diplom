import pandas as pd
import matplotlib.pyplot as plt

# path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'
# path = 'src/stz_R_emi_nakoplenie_1573215120226000.csv'
path = 'src/stz_R_emi_nakoplenie_1573216498735000.csv'


df = pd.read_csv(path, sep=';')
df['Front_R'] = (df['Front_X']**2 + df['Front_Y']**2 + df['Front_Z']**2)**0.5
df['Back_R'] = (df['Back_X']**2 + df['Back_Y']**2 + df['Back_Z']**2)**0.5

print(df.columns) # Вывод названий столбцов

fig1_z = plt.figure()
plt.title('Front Z')
plt.scatter(df['Heading'], df['Front_Z'], s=1)
plt.xlabel('Heading')
plt.grid()

fig1_x = plt.figure()
plt.title('Front X')
plt.scatter(df['Heading'], df['Front_X'], s=1)
plt.xlabel('Heading')
plt.grid()

fig1_y = plt.figure()
plt.title('Front Y')
plt.scatter(df['Heading'], df['Front_Y'], s=1)
plt.xlabel('Heading')
plt.grid()


fig2_z = plt.figure()
plt.title('Back Z')
plt.scatter(df['Heading'], df['Back_Z'], s=1)
plt.xlabel('Heading')
plt.grid()

fig2_y = plt.figure()
plt.title('Back Y')
plt.scatter(df['Heading'], df['Back_Y'], s=1)
plt.xlabel('Heading')
plt.grid()

fig2_x = plt.figure()
plt.title('Back X')
plt.scatter(df['Heading'], df['Back_X'], s=1)
plt.xlabel('Heading')
plt.grid()


# fig2 = plt.figure()
# plt.title('Pitch')
# plt.scatter(df['Pitch'], df['Front_X'], s=1)
# plt.grid()
# fig3 = plt.figure()
# plt.title('Roll')
# plt.scatter(df['Roll'], df['Front_X'], s=1)
# plt.grid()


plt.show()