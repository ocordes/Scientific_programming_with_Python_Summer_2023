import numpy as np

import matplotlib.pyplot as plt

N = 101
x = np.linspace(-1,1,N)
y = np.linspace(-1,1,N)

X, Y = np.meshgrid(x,y)

Z = -(X**2+Y**2)

fig = plt.figure(figsize=(7,7))
ax = plt.axes(projection='3d')


ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax.set_title('Surface plot')

plt.show()
