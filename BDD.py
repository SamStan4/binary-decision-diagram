#!/bin/python3

from pyeda.inter import * # grabs us all of the functions and symbols from the pyeda library
from pyeda.boolalg.bdd import *
import os # for clearing the terminal

# this is for changing the color of the terminal, these are the same escape sequences
# that I use when I am changing color in c/c++

class colors:
    F_BLACK = '\033[30m'
    F_RED = '\033[31m'
    F_GREEN = '\033[32m'
    F_YELLOW = '\033[33m'
    F_BLUE = '\033[34m'
    F_MAGENTA = '\033[35m'
    F_CYAN = '\033[36m'
    F_WHITE = '\033[37m'
    
    B_BLACK = '\033[40m'
    B_RED = '\033[41m'
    B_GREEN = '\033[42m'
    B_YELLOW = '\033[43m'
    B_BLUE = '\033[44m'
    B_MAGENTA = '\033[45m'
    B_CYAN = '\033[46m'
    B_WHITE = '\033[47m'
    
    RESET = '\033[0m'

x_variables = [exprvar('x{}'.format(i)) for i in range(1, 7)]     # this will create the boolean variables that we are going to want 
y_variables = [exprvar('y{}'.format(i)) for i in range(1, 7)]     # and format it in the form { x1, x2, ... , x6 } and { y1, y2, ... , y6 }

#*********************************************************************************************************************************************#
#   function name       : convert_int_to_binary_6_bit_array()
#   functional purpose  : this function will convert an integer into a 6 bit boolean array
#   inputs              : int
#   outputs             : boolean array
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def convert_int_to_binary_6_bit_array(target):
    
    boolean_list = [ False, False, False, False, False, False ] # 6 bits, initialize it to zero

    for i in range(5, -1, -1):
        
        if ((2 ** i) <= target):
            boolean_list[len(boolean_list) - i - 1] = True
            target -= 2 ** i
        else:
            boolean_list[len(boolean_list) - i - 1] = False

    
    if (target > 0):
        print(colors.B_RED + "overflow inside binary conversion function!" + colors.RESET)

    return boolean_list

#*********************************************************************************************************************************************#
#   function name       : make_edge_bool_formula()
#   functional purpose  : this function will create a boolean formula that represnets that there is an edge between two nodes in a graph
#   inputs              : two integer variables
#   outputs             : boolean formula
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def make_edge_bool_formula(x_node, y_node):
    #x1, x1, x3 = map()

    forumla_function = None

    x_node_list = convert_int_to_binary_6_bit_array(x_node)     # convert both of these into boolean arrays length 6
    y_node_list = convert_int_to_binary_6_bit_array(y_node)

    if (x_node_list[0]):           # initialize to be the first x variable
        forumla_function = x_variables[0]
    else:
        forumla_function = ~x_variables[0]

    for i in range (1, 6, 1):      # add the x variables
        if (x_node_list[i]):
            forumla_function &= x_variables[i]
        else:
            forumla_function &= ~x_variables[i]

    for i in range (0, 6, 1):     # add the y variables
        if (y_node_list[i]):
            forumla_function &= y_variables[i]
        else:
            forumla_function &= ~y_variables[i]

    return expr2bdd(forumla_function)

#*********************************************************************************************************************************************#
#   function name       : make_32_node_BDD()
#   functional purpose  : this function answers the question: (i + 3)%32 = j%32 or (i + 8)%32 = j%32.
#   inputs              : int, int
#   outputs             : boolean
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def edge_rule(x_node, y_node):
    if ((((x_node + 3) % 32) == (y_node % 32)) or (((x_node + 8) % 32) == (y_node % 32))):
        return True
    else:
        return False

#*********************************************************************************************************************************************#
#   function name       : make_32_node_BDD()
#   functional purpose  : this function will create a 32 (0 - 32) node BDD representation of a graph with edge rule: 
#                         there is an edge from node i to node j iff (i + 3)%32 = j%32 or (i + 8)%32 = j%32.
#   inputs              : int
#   outputs             : a boolean decision diagram
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def make_32_node_BDD():

    temp_boolean_formula = None
    local_boolean_formula = None

    for i in range(0, 32, 1):
        for j in range(0, 32, 1):
            if (edge_rule(i, j)):
                temp_boolean_formula = make_edge_bool_formula(i, j)
                if (local_boolean_formula == None):
                    local_boolean_formula = temp_boolean_formula
                else:
                    local_boolean_formula |= temp_boolean_formula

    return expr2bdd(local_boolean_formula)



#*********************************************************************************************************************************************#
#   function name       : clear_terminal()
#   functional purpose  : clears terminal like system("clear"); does in c/c++
#   inputs              : none
#   outputs             : none
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

#*********************************************************************************************************************************************#
#   function name       : main_menu()
#   functional purpose  : a menu for the user to select what they want to do from
#   inputs              : none
#   outputs             : int
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def main_menu():

    x = True
    list_decisions = { 1 }

    while (x):

        clear_terminal()

        print("---Main Menu---\n")

        print("enter '1' to build the BDD and run the program\n")

        try: # try block to that this input doesnt crash the program
            decision = int(input("Enter here: "))

            if decision in list_decisions:
                x = False
        except:
            x = True

    return decision

#*********************************************************************************************************************************************#
#   function name       : main()
#   functional purpose  : main routine, like in c/c++
#   inputs              : none
#   outputs             : none
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def main():
    decision = main_menu()

    if (decision == 1):
        test_BDD = make_32_node_BDD()

    #print(bdd2expr(test_BDD))

    smoothing_vars = test_BDD.smoothing()

    #print(bdd2expr(smoothing_vars))

    print("Smoothing Variables:", smoothing_vars)


    #esult = test_BDD.

    #my_formula = x_variables[0] & y_variables[0]

    #print(my_formula)
        
    #bool_for = make_edge_bool_formula(11, 6)

    #print(bool_for)





#*********************************************************************************************************************************************#

main()

