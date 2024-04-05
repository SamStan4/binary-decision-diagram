#!/bin/python3

from pyeda.inter import * # grabs us all of the functions and symbols from the pyeda library
from pyeda.boolalg.bdd import *
import os # for clearing the terminal and pausing the terminal

x_variables = [bddvar('x{}'.format(i)) for i in range(1, 6)]     # this will create the boolean variables that we are going to want 
y_variables = [bddvar('y{}'.format(i)) for i in range(1, 6)]     # and format it in the form { x1, x2, ... , x6 } and { y1, y2, ... , y6 }
z_variables = [bddvar('z{}'.format(i)) for i in range(1, 6)]     # for .compose()

test_bdd = x_variables[0] & y_variables[0]

print(bdd2expr(test_bdd))

transition = { x_variables[0] : z_variables[0] }

test_bdd = test_bdd.compose(transition)

print(bdd2expr(test_bdd))