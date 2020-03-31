from functools import reduce
from math import gcd
from sympy import *

def get_denominators(smatrix):
    row_denominators = [list(set([val.denominator for val in row])) for row in smatrix]
    mulipliers = [reduce(lambda x, y: x * y, sublist) for sublist in row_denominators]
    return mulipliers


def get_int_smatrix(smatrix, greatest_denominators):
    int_smatrix = []
    i = 0
    for row in smatrix:
        new_row = []
        for val in row:
            new_val = val * greatest_denominators[i]
            new_row.append(int(new_val))
        int_smatrix.append(new_row)
        i += 1
    return int_smatrix

def get_min_smatrix(int_smatrix):
    min_smatrix = []
    for row in int_smatrix:
        greates_divisor = reduce(gcd, row)
        if greates_divisor > 1:
            new_row = [int(val / greates_divisor) for val in row]
            min_smatrix.append(new_row)
        else:
            min_smatrix.append(row)
    min_sympy_smatrix = Matrix(min_smatrix)
    return min_sympy_smatrix

def run(smatrix):
    greatest_denominators = get_denominators(smatrix)
    int_smatrix = get_int_smatrix(smatrix, greatest_denominators)
    min_smatrix = get_min_smatrix(int_smatrix)
    return min_smatrix
