import numpy as np
import matplotlib.pyplot as plt

# load the data and split into variables
data = np.loadtxt('data/pg1605_16.05.2001.dat')
times = data[:,0]
mmags = data[:,1]

# mask unwanted data points
mask = (mmags < 600) & (mmags > 0.)
times = times[mask]
mmags = mmags[mask]

# calculate some information
mmags_mean = mmags.mean()

# setup the plot
fig, ax = plt.subplots(figsize=[10,2])

# plot the data
ax.plot(times-times[0], mmags-mmags_mean, 'r-')
ax.set_title('Lightcurve of a variable star')
ax.set_ylabel(r'$R$ [mmag]')
ax.set_xlabel(r'$t$ [s]');

plt.savefig('lightcurve.png')
