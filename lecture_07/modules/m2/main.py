# main.py

# written by: Oliver Cordes 2023-05-17
# changed by: Oliver Cordes 2023-05-17



import subdir.test

import subdir.test as test

# main program
print(subdir.test.some_data)
print(test.some_data)

subdir.test.some_function('test2')
test.some_function(msg='test2')
