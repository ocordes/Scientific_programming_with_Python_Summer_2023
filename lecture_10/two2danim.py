# two2danim.py
#
# written by: Oliver Cordes 2023-04-10
# changed by: Oliver Cordes 2023-04-10

# The two2danimation object is a simple object to store for a
# specific time the x,y position of n objects. After all data
# are stored, the data can be seen as an animation.


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functools import partial


# two2danimation object
#
#
class two2danimation(object):
    # __init__
    #
    # initialize the object, with the number of objects
    def __init__(self, nrobjects=1, figsize=(5,5), xlimits=(-10,10), ylimits=(-10,10)):
        self._time = []
        self._nrobjects = nrobjects
        self._data = []
        self._figsize = figsize
        self._xlimits = xlimits
        self._ylimits = ylimits
        
        # initialize the data structure
        for i in range(nrobjects):
            self._data.append({'x': [], 'y': []})
            
    
    # clear 
    #
    # clear all the data
    def clear(self):
        self._time = []
        for i in range(self._nrobjects):
            self._data[i]['x'] = []
            self._data[i]['y'] = []
        
    
    # append
    #
    # appends the data, the first argument is always the time spot,
    # the next arguments are for each point, x and y floats are necessary!
    def append(self, time, *args):
        self._time.append(time)
        
        if len(args) < (self._nrobjects*2):
            raise ValueError('Too few arguments in append.')
        
        for i in range(self._nrobjects):
            self._data[i]['x'].append(args[(i*2)])
            self._data[i]['y'].append(args[(i*2)+1])                          

    
    # __repr__
    #
    # for printing the data content stored in the object
    def __repr__(self):
        return ','.join([f'time={self._time}', f'data={self._data}'])
    
    
    # _anim_setup
    #
    # internal function to setup the animation frame
    def _anim_setup(self):
        self._fig, self._ax = plt.subplots(figsize=self._figsize)
        self._points, = self._ax.plot([], [], 'r.')
        
    
    # _anim_init
    #
    # internal function for the initialisation of the animation
    # content can maybe also set in _anim_setup
    def _anim_init(self):
        self._ax.set_xlim(self._xlimits[0], self._xlimits[1])
        self._ax.set_ylim(self._ylimits[0], self._ylimits[1])
        return self._points,
    
    
    # _anim_update
    #
    # internal function for the animation is called every frame
    # of the animation. The frame is a somewhat time argument,
    # so we need some interpolation of the positional data
    # if the time is not fitting directly to the stored data
    def _anim_update(self, frame, points ):
        xa = []
        ya = []
        # interpolate the position for each object from the
        # stored data
        for i in range(self._nrobjects):
            x = np.interp(frame, self._time, self._data[i]['x'])
            y = np.interp(frame, self._time, self._data[i]['y'])
            xa.append(x)
            ya.append(y)
        points.set_data(xa, ya)
        return points,
    
    
    def animation(self, steps):
        self._anim_setup()
        
        if steps < len(self._time):
            steps = len(self._time)+1
        
        ani = FuncAnimation(
            self._fig, partial(self._anim_update, points=self._points),
            frames=np.linspace(0, self._time[-1], steps),
            #frames=np.arange(0,len(self._time)),
            init_func=self._anim_init, blit=True)
        
        plt.close(ani._fig)
        
        return ani
    