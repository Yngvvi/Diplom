import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.fftpack import fft, rfft

path = 'src/stz_R_emi_nakoplenie_1573453938716000.csv'

df = pd.read_csv(path, sep=';')

# F = fft(df['Front_Z'])

RF = rfft(df['Front_Z'])

GP = []
for i in RF:
    if abs(i) > 5000000:
        GP.append(i)

# plt.plot(df.index, RF)
print(RF)
print(GP)
X = np.arange(len(GP))
print(X)

plt.plot(X, np.abs(GP))
plt.grid()
plt.show()
