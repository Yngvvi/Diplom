import matplotlib.pyplot as plt
import numpy as np


x = np.array([1, 5, 10, 15, 20])

y1 = 2 * x
y2 = 3 * x
y3 = 5 * x

y = [y1, y2, y3]
y_lebels = ['y1', 'y2', 'y3']

fig, ax = plt.subplots()
for i in y:
    ax.plot(x, i)
# ax.plot(x, y1)
# ax.plot(x, y2)
# ax.plot(x, y3)

ax.set_xlabel('x')
ax.legend(y_lebels, loc='lower right')
ax.grid()

plt.show()

print(y1)