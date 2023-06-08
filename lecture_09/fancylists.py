# fancylist.py
#
# written by: Oliver Cordes 2023-06-05
# changed by: Oliver Cordes 2023-06-05

"""
fancylist.py

implements a special fancy list class, which allows
fancy indexing on normal lists

The implementation is not complete and is only
an example how to use the class
"""

# define a fancy list class
class FList(object):
    def __init__(self, value):
        # copy values if possible
        if isinstance(value, (tuple,list)):
            self._value = value
        elif isinstance(value, FList):
            self._value = value._value
        else:
            # simplest reaction, can be changed
            raise TypeError('value must be of type list or tuple')
            
            
    # for representation    
    def __repr__(self):
        return f'FList({self._value})'
    
    # for printing
    def __str__(self):
        return str(self._value)
    
    # get the length of the list
    def __len__(self):
        return len(self._value)
    
    # append new items
    def append(self, newitem):
        self._value.append(newitem)
    
    # bulk test for comparison
    def __eq__(self, val):
        ret = [ val == item for item in self._value]
        return ret
    
    # fancy indexing and masking
    def __getitem__(self, index):
        #print(f'__getitem__({index})')   # have a look for all different types!
        if isinstance(index,int):
            return self._value[index]
        elif isinstance(index, (tuple,list)):
            if isinstance(index[0], bool):
                return FList([item for i,item in enumerate(self._value) if index[i]])
            elif isinstance(index[0], int):
                return FList([self._value[i] for i in index])
        else:
            return self._value.__getitem__(index)
            
            
    # substring masking
    def contains(self, value):
        ret = [ value in item for item in self._value]
        return ret
            