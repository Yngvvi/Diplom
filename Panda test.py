import pandas as pd

df = pd.DataFrame({'country': ['Kazakhstan', 'Russia', 'Belarus', 'Ukraine'],
'population': [17.04, 143.5, 9.5, 45.5], 'square': [27, 17, 20, 60]})

# Выборка по условию
# req = df.loc[df['population'].abs() + df['square'].abs() > 50]
# print(req)

# Добавление нового столбца из комбинации старых
# df['smf'] = df['population'] + df['square']

# Поиск списка номеров строк по условию
# a = df.index[df['population'] > 20].tolist()
# print(a)

# Количество строк в таблице
# num = df['country'].count()
# Или
# num = df.shape[0]
# print(num)

# Удалить строки с a до b
# df = df.iloc[:2]

# Сохранение фрейма в csv файл
# df.to_csv('Clean.csv')

# Вывод названий столбцов
# print(df.columns)

# Вывод типов данных в столбцах
# print(df.dtypes)


print(df)


