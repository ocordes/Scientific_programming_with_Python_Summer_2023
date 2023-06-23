# simple demo script for basic multiprocessing
# parallelisation
import numpy as np
import multiprocessing

# simple script to test a list of numbers on the
# prime-number property:
def is_prime(n):
    """
    tests whether an integer is a prime number

    input: the number to be testes
    return: the number if it is a prime and -1 otherwise
    """

    if n != 2 and n%2 == 0:
        return -1
    else:
        for i in range(3, int(np.sqrt(n) + 1)):
            if n%i == 0:
                return -1

    return n


if __name__ == '__main__':
    # initialize a process pool;
    # just play with the number of processes to see
    # the time difference; note the method
    # multiprocessing.cpu_count() which gives you the
    # number of CPUs / cores of your machine:
    print("Your machine has {} CPUs / cores".format(multiprocessing.cpu_count()))


    with multiprocessing.Pool(processes = 4) as pool:

        # and perform prime-number testing in parallel:
        # The pool.map command takes a function and an iterable
        # (typically a list) of arguments which are considered
        # in parallel!
        # Note that pool-map returns a list, not an iterable!
        result = pool.map(is_prime, list(range(2, 5000000)))

    # print(result)
