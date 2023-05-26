# module1.py
#
#
# written by: Oliver Cordes 2023-05-23
# changed by: Oliver Cordes 2023-05-23

"""
module1.py


This demonstrate the usage of classes for data handling.

"""

import numpy as np

import matplotlib.pyplot as plt



class Pendulum(object):
    def __init__(self, filename):

       self.__filename = filename


       self.__load_data()


    def filename(self):
       """
       returns the filename of the dataset
       """
       return self.__filename


    def __load_data(self):
       """
       loads a data set from file
    
       l, T, Terr
    
       T and Terr are measurements for 10*T_real, so the values need 
       to be adjusted
       """
       data = np.loadtxt(self.__filename)

       if (data.ndim > 1) and  (data.shape[1] == 3) and (data.shape[0] > 0):
    
          self.__l = data[:,0]
          self.__T = data[:,1]/10
          self.__Terr = data[:,2]/10

       else:
          # error handling
          raise ValueError(f'Data in file {self.__filename} are not valid!')


    def calculate_g(self):
       """
       calculate g and g_err
    
       from given values
       """
       g = 4 * (np.pi**2)*self.__l/(self.__T**2)
       gerr = g * 2 * self.__Terr/self.__T
    
       return g, gerr


    def plot_data(self):
       """
       create a simple data plot
       """
       fig, ax = plt.subplots()
    
       ax.errorbar(np.sqrt(self.__l),self.__T,yerr=self.__Terr, capsize=2)
       ax.set_xlabel(r'$\sqrt{l}$')
       ax.set_ylabel(r'$T$')
    
       plt.show()
    
    
