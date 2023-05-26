# module1.py
#
#
# written by: Oliver Cordes 2023-05-23
# changed by: Oliver Cordes 2023-05-23

"""
module1.py


This demonstrate the usage of functions for data handling.

"""

import numpy as np

import matplotlib.pyplot as plt


def load_data(filename):
    """
    loads a data set from file
    
    l, T, Terr
    
    T and Terr are measurements for 10*T_real, so the values need 
    to be adjusted
    """
    data = np.loadtxt(filename)
    
    return data[:,0], data[:,1]/10, data[:,2]/10



def calculate_g(l, T, Terr):
    """
    calculate g and g_err
    
    from given values
    """
    g = 4 * (np.pi**2)*l/(T**2)
    gerr = g * 2 * Terr/T
    
    return g, gerr


def plot_data(l, T, Terr):
    """
    create a simple data plot
    """
    fig, ax = plt.subplots()
    
    ax.errorbar(np.sqrt(l),T,yerr=Terr, capsize=2)
    ax.set_xlabel(r'$\sqrt{l}$')
    ax.set_ylabel(r'$T$')
    
    plt.show()
    
    