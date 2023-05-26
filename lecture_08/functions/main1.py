# main1.py

# written by: Oliver Cordes 2023-05-23
# changed by: Oliver Cordes 2023-05-23


# demonstration of a procedural data reduction


import module1


# main program

# load the dataset
data = module1.load_data('pendulum1.dat')

# calculate g/gerr
g, gerr = module1.calculate_g(data[0], data[1], data[2])

# print the results
print(f'g={g.mean():.2f} +/- {gerr.std():.2f}')
print(f'gerr(min) = {gerr.min():.2f} gerr(max) = {gerr.max():.2f}')

# create a plot
module1.plot_data(data[0], data[1], data[2])
