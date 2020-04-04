# Доделать и засунуть в Utilities
import pandas as pd
import matplotlib.pyplot as plt

path = 'stz_R_emi_nakoplenie_1573453938716000.csv'

df = pd.read_csv(path, sep=';')
head = list(df)
df['Timestamp'] = df['Timestamp'] *(10**(-15))

# Создаём список строк в которых аппарат ещё не движется
del_str = df.index[(df['VertForvUp'] == 0) & (df['VertForvDown'] == 0) &
                   (df['VertBackUp'] == 0) & (df['VertBackDown'] == 0)].tolist()
# или перемещается с использованием маневренных двигателей
del_str.extend(df.index[(df['VertForvUp'].abs() + df['VertForvDown'].abs()
                   + df['VertBackUp'].abs() + df['VertBackDown'].abs()) > 5])
# Количество строк в таблице
length = df.shape[0]
# Сортируем этот список по возрастанию
del_str.sort()
# Длина разрыва между пиками
core = 500
# Список для концов пиков
nums = []
for i in range(len(del_str)-1):
    if del_str[i] + core < del_str[i+1]:
        nums.extend(del_str[i:i+2])
# Доделать позже для для более 2-х значений
df_clean = df.iloc[nums[0]+1:nums[1]]
# Заново нумерует строки с 0
df_clean = df_clean.reset_index(drop=True)

# Имя нового файла
name = 'Clean/' + path.split('.')[0] + '_clean.csv'
df_clean.to_csv(name, header=head, index=False, sep=';')
# print(head)

# plt.plot(df['Timestamp'], df['VertForvUp'])
# plt.plot(df_clean['Timestamp'], df_clean['VertForvUp'])
# plt.xlabel('Timestamp')
# plt.ylabel('VertForvUp')
# plt.grid()
# plt.show()

