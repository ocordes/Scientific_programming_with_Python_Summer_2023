import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# font size of labels etc,
#matplotlib.rcParams['font.size'] = 18
# line width of coordinate axes
#matplotlib.rcParams['axes.linewidth'] = 2.0

# matplotlib plots numpy-arrays:
x = np.linspace(-np.pi, np.pi, 50)
c = np.cos(x)
s = np.sin(x)

# Create a figure of size 8x6 inches, 80 dots per inch, 2 plots in 2 rows
fig, ax = plt.subplots(2,1,figsize=(8,10))

# add padding between the two lines of plots
fig.tight_layout(pad=4.0)

# Plot cosine with a blue continuous line of width 1 (pixels)
ax[0].plot(x, c, color="blue", linestyle="-", linewidth=2.0, label=r"$\cos(x)$")

# Plot sine with a green dashed line of width 1 (pixels)
ax[0].plot(x, s, 'g--', linewidth=2.0, label=r"$\sin(x)$")

# the labels only appear if you directly call plt.legend()
# locate the legend on the upper left part of the plot
ax[0].legend(loc='upper left')

# x- and y-labels
ax[0].set_xlabel(r'$x$')
ax[0].set_ylabel(r'$y$')

# Set x limits (fixed limits)
ax[0].set_xlim(-np.pi, np.pi)

# Set x ticks
ax[0].set_xticks(np.linspace(-np.pi, np.pi, 9, endpoint=True))

# nicer x-ticks with LaTeX labels!
#plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
#          [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

# Set y limits (get limits from data)
ax[0].set_ylim(c.min(), c.max())

# Set y ticks
ax[0].set_yticks(np.linspace(-1, 1, 5, endpoint=True))

# Set a title
ax[0].set_title("trigonometric functions", y=1.02)


# read some data
data = np.loadtxt('data/pendulum.dat')
x1 = data[:,0]
y1 = data[:,1]
e1 = data[:,2]

ax[1].set_title('Pendulum measurements')
ax[1].errorbar(x1, y1, yerr=e1,fmt='.', capsize=5 )
ax[1].plot(x1, y1, 'r--')
ax[1].set_xlabel(r'length $l$')
ax[1].set_ylabel(r'time $t$')

# Save figure as pdf or png
#plt.savefig("complex.pdf")
plt.savefig("complex.png")