#!/bin/python3
from pyeda.inter import * # grabs us all of the functions and symbols from the pyeda library
from pyeda.boolalg.bdd import *

x_variables = [exprvar('x{}'.format(i)) for i in range(1, 5)]     # this will create the boolean variables that we are going to want 
y_variables = [exprvar('y{}'.format(i)) for i in range(1, 5)]     # and format it in the form { x1, x2, ... , x6 } and { y1, y2, ... , y6 }

def compare_two_dictionaies(dict_one, dict_two):
    if (len(dict_one) != len(dict_two)):
        return False
    for i in dict_one:
        if i not in dict_two:
            return False
        elif (dict_one[i] != dict_two[i]):
            return False
    return True

def is_dict_in_list_dict(tdict, list_dict):
    for i in list_dict:
        if not compare_two_dictionaies(tdict, i):
            return False
    return True

my_exp = x_variables[0] & ~x_variables[1] & y_variables[0] & y_variables[1] 
my_BDD = expr2bdd(my_exp)
my_test = {x_variables[0] : 1, x_variables[1] : 0, y_variables[0] : 1, y_variables[1] : 1}
my_BDD.compose({x_variables[0] : x_variables[2], x_variables[1] : x_variables[3], y_variables[0] : y_variables[2], y_variables[1] : y_variables[3]})