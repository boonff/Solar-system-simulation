import matplotlib.pylab as plt
import numpy as np

def f(x, y):
    return -np.sin(x)

x = [0]
y = [1]

h = 1e-1
n = 1000

def foo():
    for i in range(n):
        k1 = f(x[-1], y[-1])
        k2 = f(x[-1] + 0.5 * h, y[-1] + 0.5 * k1)
        k3 = f(x[-1] + 0.5 * h, y[-1] + 0.5 * k2)
        k4 = f(x[-1] + h, y[-1] + h * k3)
        x.append(x[-1] + h)
        y.append(y[-1] + h/6*(k1 + 2*k2 + 2*k3 + k4))

def fooo():
    for i in range(n):
        x.append(x[-1] + h)
        y.append(y[-1] + h * f(x[-1], y[-1]))

fooo()

plt.plot(x, y)
plt.show()