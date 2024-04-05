#!/bin/python3

from pyeda.inter import * # grabs us all of the functions and symbols from the pyeda library
from pyeda.boolalg.bdd import *

# Define boolean variables
x, y, z = map(exprvar, 'xyz')

# Define boolean expressions for BDDs
expr1 = (x & y) | (~x & z)
expr2 = (x & z) | (~x & y)

bdd1 = expr2bdd(expr1)
bdd2 = expr2bdd(expr2)
    
test_dict_1 = { 1 : 3 }
test_dict_2 = { 1 : 2 }

# print(compare_two_dicts(test_dict_1, test_dict_2))

# print(compare_two_BDDs(bdd1, bdd2))

print(bdd1.equivalent(bdd2))