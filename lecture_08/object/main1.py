# main1.py

# written by: Oliver Cordes 2023-05-23
# changed by: Oliver Cordes 2023-05-23


# demonstration of a module  data reduction


from module1 import Pendulum


# main program

# load the datasets

filenames = ['pendulum1.dat', 'pendulum2.dat']
#filenames = ['pendulum1.dat', 'pendulum2.dat', 'pendulum3.dat']

try:
  datalist = [Pendulum(filename) for filename in filenames]
except ValueError as msg:
  print(msg)
  print('Continue with an empty list.')
  datalist = []


# executed if not empty!
for data in datalist:
   # calculate g/gerr
   g, gerr = data.calculate_g()

   # print the results
   print(f'data={data.filename()}:')
   print(f'g={g.mean():.2f} +/- {gerr.std():.2f}')
   print(f'gerr(min) = {gerr.min():.2f} gerr(max) = {gerr.max():.2f}')
   print()

   # create a plot
   #data.plot_data()
