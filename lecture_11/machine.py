import numpy as np

from twodanim import twodanimation

def vector(x, y):
    return np.array([x,y], np.float64)
    

class Update(object):
    def update(self, T, deltaT):
        pass
    
    
class Force(Update):
    def calculate(self, x, v, mass):
        return vector(0,0)
    
    
class Wall(Update):
    def calculate(self, x, v, mass):
        return x, v
    
    
class System(object):
    def __init__(self, maxT, deltaT, 
                     figsize=(5,5),
                     xlimits=(-10,10), 
                     ylimits=(-10,10)):
        self._maxT = maxT
        self._deltaT = deltaT
        self._forces = []
        self._walls = []
        
        self._particles = []
        
        # for the simulation
        self._figsize = figsize
        self._xlimits = xlimits
        self._ylimits = ylimits
        
        
        
    def add_particle(self, p):
        self._particles.append(p)
        
    def add_force(self, f):
        self._forces.append(f)
        
    def add_wall(self, w):
        self._walls.append(w)
        
    def additional_graphics(self, ax):
        pass
    
    def analyze(self, T):
        pass
    
    def simulate(self):
        # at this point the number of particles
        # are set
        
        anim = twodanimation(nrobjects=len(self._particles), figsize=self._figsize,
                                 xlimits=self._xlimits, ylimits=self._ylimits, callback=self.additional_graphics)
        
        
        for p in self._particles:
            p.set_forces(self._forces)
            p.set_walls(self._walls)
            
        T = 0
        while T < self._maxT:
            
            for p in self._particles:
                p.update(T, self._deltaT)
            for f in self._forces:
                f.update(T, self._deltaT)
            for w in self._walls:
                w.update(T, self._deltaT)
                              
            positions = [p.get_position() for p in self._particles]
            anim.append(T, positions)
            
            # room for analyzing data
            self.analyze(T)
            
            T += self._deltaT
            
                              
        return anim.animation(int(T//self._deltaT))
    
    
class Particle(Update):
    def __init__(self, x, v, mass):
        self._x = x
        self._v = v
        self._mass = mass
        self._forces = []
        self._walls = []
    
    def set_forces(self, forces):
        self._forces = forces
        
    def set_walls(self, walls):
        self._walls = walls
        
    def get_position(self):
        return self._x
    
    def get_velocity(self):
        return self._v
    
    def update(self, T, deltaT):
        return