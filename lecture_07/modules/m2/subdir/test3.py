# test3.py

"""
test3 module

This is a doc string .

"""

# written by: Oliver Cordes 2023-05-17
# changed by: Oliver Cordes 2023-05-17


# import existing submodule

import subdir.test



def some_function3(msg='A sample message.'):
    """
    some_functtion3
 
    prints a message.

    Example:

    test3.some_function2(msg='test')
    """
    subdir.test.some_function(msg)
